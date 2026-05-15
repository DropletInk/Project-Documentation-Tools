def main():
    """
    Hello from documentation-tutorial!
    """
    print("Hello from documentation-tutorial!")



from __future__ import annotations   

from abc import ABC, abstractmethod   
from collections.abc import Iterator, Sequence, Sized   

from dataclasses import dataclass  
from pathlib import Path
from typing import (
    Annotated,     
    Any,          
    Final,         
    Literal,       
    NamedTuple,    
    NewType,      
    Self,          
    overload,      
)

import numpy as np
from msgspec import Meta, Struct, field  
type Shape[*Ts] = tuple[*Ts]  

type ArrayND[S: Shape[*tuple[int, ...]], T: Any] = np.ndarray[S, np.dtype[T]] 
type StrArray[S: Shape[*tuple[int, ...]]] = np.ndarray[S, np.dtype[np.str_]] 

type Vector[S: Shape[int], T: Any] = ArrayND[S, T]                  
type Array2D[S: Shape[int, int], T: Any] = ArrayND[S, T]            
type Array3D[S: Shape[int, int, int], T: Any] = ArrayND[S, T]       
type Array4D[S: Shape[int, int, int, int], T: Any] = ArrayND[S, T]  


type IntVector = Vector[Shape[int], np.int_]      
type BoolVector = Vector[Shape[int], np.bool_]    
type StrVector = Vector[Shape[int], np.str_]      

type MultiIndexer = slice | Sequence[int] | IntVector | BoolVector
type Indexer = int | MultiIndexer | None

type BBox = Annotated[list[int], Meta(min_length=4, max_length=4)]  


FilePath = NewType("FilePath", Path)
DirPath = NewType("DirPath", Path)


WORD_SEP: Final[Literal[" "]] = " "
LINE_SEP: Final[Literal["\n"]] = "\n"
PARA_SEP: Final[Literal["\n\n"]] = "\n\n"


def _get_multiindexer(indexer: Indexer) -> MultiIndexer:
    """
        Returns the slice function with the provided indexer value. 
        
        Args:
            Indexer (int/slice/Sequence/IntVector/BoolVector). 
        Returns: 
            slice (indexer) if Indexer is None.
            slice (indexer,stop) if Index is integer. 
            indexer if indexer  is slice or sequence or numpyArray.
            raises error else.
    """
    if indexer is None:
        return slice(indexer)
    elif isinstance(indexer, int):
        stop = None if indexer == -1 else indexer + 1
        return slice(indexer, stop)
    elif isinstance(indexer, slice | Sequence | np.ndarray):
        return indexer
    else:
        raise TypeError(
            f"Expected type indexer to be one of int, slice, None; found={type(indexer)}"
        )


def _is_contiguous_slice(*args: MultiIndexer) -> bool:
    """
        Finds if the slice is continuous or not means step size should be 1.

        Args:
            slice (start,stop,step) | Sequence[int] | IntVector | BoolVector.
        
        Returns:
            True if slice is contiguous (step == 1 or step == -1).
            False if slice is not contiguous ( step == 2 ) or not a slice a function.
    """
    return all(
        isinstance(arg, slice) and (arg.step is None or abs(arg.step) == 1)
        for arg in args
    )


@dataclass
class OcrBlockCollection(Sized):
    """
    Represents a collection of OCR blocks for paragraph,lines and words.

    This class stores the OCR  results  in a structured  format using Numpy Arrays.

    Attributes:
        parent_ids (IntVector): Parent id for the ocr block.
        texts (StrVector): Extracted Text content. 
        bboxes (Array2D): Bounding box for the text.

    """
    parent_ids: IntVector
    texts: StrVector
    bboxes: Array2D[Shape[int, Literal[4]], np.int_]

    def __post_init__(self) -> None:
        """
        Initializes indices for paragraph , lines , words 

        Splits OCR blocks into :
        - Paragraph ids
        - Line ids
        - word ids

        """
        self.para_ids = np.flatnonzero(self.parent_ids == -1)
        self.line_ids = np.flatnonzero(
            (self.parent_ids >= 0) & (self.parent_ids < self.para_ids.size)
        )
        self.word_ids = np.flatnonzero(
            (self.parent_ids >= self.para_ids.size)
            & (self.parent_ids < (self.para_ids.size + self.line_ids.size))
        )

    def __len__(self) -> int:
        """
            Returns the number of items.
        """
        return self.count()

    def count(self) -> int:
        """
            Returns the calculated size of the text content. 
        """
        return self.texts.size

    @overload
    def __getitem__(
        self,
        levels: int
        | MultiIndexer
        | tuple[int | MultiIndexer]
        | tuple[int | MultiIndexer, None]
        | tuple[int | MultiIndexer, None, None],
    ) -> ParaCollection: ...
    @overload
    def __getitem__(
        self,
        levels: tuple[Indexer, int | MultiIndexer]
        | tuple[Indexer, int | MultiIndexer, None],
    ) -> LineCollection: ...
    @overload
    def __getitem__(
        self,
        levels: tuple[Indexer, Indexer, int | MultiIndexer]
        | tuple[None]
        | tuple[None, None]
        | tuple[None, None, None],
    ) -> WordCollection: ...
    @overload
    def __getitem__(
        self, levels: tuple[Indexer, Indexer, Indexer]
    ) -> TextBlockCollection: ...
    def __getitem__(
        self,
        levels: int
        | MultiIndexer
        | tuple[Indexer]
        | tuple[Indexer, Indexer]
        | tuple[Indexer, Indexer, Indexer],paragraph
    ) -> TextBlockCollection:
        """
            Generates OCR blocks

            indexing is in form:
                object[para(0)],
                object[para(0),line(1)],
                object[para(0),line(1),word(2)],

            Returns:
                WordCollection, LineCollection, ParaCollection depending on the indexing.
        """
        match levels:
            case (p,) | int(p) | (slice(start=_, stop=_, step=_) as p):
                para, line, word = p, None, None
            case (p, l):
                para, line, word = p, l, None
            case (p, l, w):
                para, line, word = p, l, w
            case _:
                raise IndexError(f"Too many indexers. Expected=3, got={len(levels)}")

        para_indexer, line_indexer, word_indexer = map(
            _get_multiindexer, (para, line, word)
        )
        para_ids_picked = self.para_ids[para_indexer]
        line_ids_picked = self.line_ids[line_indexer]
        word_ids_picked = self.word_ids[word_indexer]

        fast_path_possible = _is_contiguous_slice(
            para_indexer, line_indexer, word_indexer
        )
        match (para, line, word):
            case (None, None, _):
                return WordCollection.from_ocr(
                    self.pick_indices(self.word_ids[word_indexer])
                )
            case (None, _, None):
                return LineCollection.from_ocr(
                    self.pick_indices(self.line_ids[line_indexer])
                )
            case (_, None, None):
                return ParaCollection.from_ocr(
                    self.pick_indices(self.para_ids[para_indexer])
                )
            case (None, _, _):
                if fast_path_possible:
                    word_parent_ids = self.parent_ids[word_ids_picked]
                    in_range_mask = ((word_parent_ids >= line_ids_picked[0])
                        & (word_parent_ids < line_ids_picked[-1] + 1))  # fmt: skip
                    return WordCollection(
                        parent_ids=word_parent_ids[in_range_mask],
                        texts=self.texts[word_ids_picked][in_range_mask],
                        bboxes=self.bboxes[word_ids_picked][in_range_mask],
                    )
                unique_line_ids = np.unique(line_ids_picked)
                relevant_ids = np.flatnonzero(np.isin(self.parent_ids, unique_line_ids))
                return WordCollection.from_ocr(
                    self.pick_indices(relevant_ids[word_indexer])
                )
            case (_, _, None):
                if fast_path_possible:
                    line_parent_ids = self.parent_ids[line_ids_picked]
                    in_range_mask = ((line_parent_ids >= para_ids_picked[0])
                        & (line_parent_ids < para_ids_picked[-1] + 1))  # fmt: skip
                    return LineCollection(
                        parent_ids=line_parent_ids[in_range_mask],
                        texts=self.texts[line_ids_picked][in_range_mask],
                        bboxes=self.bboxes[line_ids_picked][in_range_mask],
                    )
                unique_para_ids = np.unique(para_ids_picked)
                relevant_ids = np.flatnonzero(np.isin(self.parent_ids, unique_para_ids))
                return LineCollection.from_ocr(
                    self.pick_indices(relevant_ids[line_indexer])
                )
            case _:
                if fast_path_possible:
                    line_parent_ids = self.parent_ids[line_ids_picked]
                    relevant_line_ids = line_ids_picked[
                        (line_parent_ids >= para_ids_picked[0])
                        & (line_parent_ids < para_ids_picked[-1] + 1)
                    ]
                    word_parent_ids = self.parent_ids[word_ids_picked]
                    in_range_mask = (word_parent_ids >= relevant_line_ids[0]) & (
                        word_parent_ids < relevant_line_ids[-1] + 1
                    )
                    return WordCollection(
                        parent_ids=word_parent_ids[in_range_mask],
                        texts=self.texts[word_ids_picked][in_range_mask],
                        bboxes=self.bboxes[word_ids_picked][in_range_mask],
                    )
                unique_para_ids = np.unique(para_ids_picked)
                relevant_line_ids = np.flatnonzero(
                    np.isin(self.parent_ids, unique_para_ids)
                )
                unique_line_ids = np.unique(relevant_line_ids[line_indexer])
                relevant_ids = np.flatnonzero(np.isin(self.parent_ids, unique_line_ids))
                return WordCollection.from_ocr(
                    self.pick_indices(relevant_ids[word_indexer])
                )

    # def get_level(
    #     self,
    #     *,
    #     para: Indexer = None,
    #     line: Indexer = None,
    #     word: Indexer = None,
    # ) -> TextBlockCollection:
    #     return self[para, line, word]

    def pick_indices(
        self,
        indexer: MultiIndexer,
    ) -> OcrBlockCollection:
        """
            Returns OcrBlockCollection with the selected indices

            This Method filters the current collection based on the provided indexer and returns a new object with corresponding parent_id , texts and bboxes 

            Args:
                indexer (MultiIndexer): Index , Slice , List , Boolean vector to select element from collections.

            Returns:
                OcrBlockCollection: Collection of the filtered items. 

            Raises:
                TypeError: If the indexer is None.   
        """
        if indexer is None:
            raise TypeError(f"{type(indexer)} is not a valid indexer type")
        return OcrBlockCollection(
            parent_ids=self.parent_ids[indexer],
            texts=self.texts[indexer],
            bboxes=self.bboxes[indexer],
        )

    def item(self) -> OcrBlock:
        """
            Returns Single OcrBlock from Collection.

            This Method checks whether the collection contains only one elemenet or not 
            ifmore than one is present then it raises error.  

            Returns:
                OcrBlock: The Single OCR Block in the collection. 

            Raises:
                ValueError: If the collection contains more than one element.   
        """
        if self.parent_ids.size != 1:
            raise ValueError("Too many items in OcrResult")
        return OcrBlock(
            parent_id=self.parent_ids[0],
            text=self.texts[0],
            bbox=self.bboxes[0],
        )

    def first(self) -> OcrBlock:
        """
        Returns the first OCR blcok In collection.
        """
        return self.at(0)

    def last(self) -> OcrBlock:
        """
        Returns the Last OCR blcok In collection.
        """
        return self.at(-1)

    def at(self, index: int) -> OcrBlock:
        """
        Returns Ocr Block at specific index. 

        Args:
            index (int): Position of the element.

        Returns:
            OcrBlock: The selected Ocr Block.
        """
        return self.pick_indices([index]).item()

    def lines_by_para(
        self, para_indexer: MultiIndexer | None = None
    ) -> Iterator[LineCollection]:
        """
        Yield lines from paragraph 

        Args:
            para_indexer (MultiIndexer,optional): index to filter paragraph. 
        
        Yields:
            Collection of Lines from the paragraph. 
        """
        match para_indexer:
            case None:
                yield from (self[i, slice(None)] for i in self.para_ids)
            case _:
                yield from (self[i, slice(None)] for i in self.para_ids[para_indexer])

    def words_by_para(
        self, para_indexer: MultiIndexer | None = None
    ) -> Iterator[WordCollection]:
        """
        Yield words from paragraph 

        Args:
            para_indexer (MultiIndexer,optional): index to filter paragraph.
        
        Yields:
            Collection of words from the paragraph.
        
        """    
        match para_indexer:
            case None:
                yield from (self[i, None, slice(None)] for i in self.para_ids)
            case _:
                yield from (
                    self[i, None, slice(None)] for i in self.para_ids[para_indexer]
                )

    def words_by_line(
        self, line_indexer: MultiIndexer | None = None
    ) -> Iterator[WordCollection]:
        """
        Yield words from lines.

        Args:
            line_indexer (MultiIndexer,optional): index to filter line. 
        
        Yields:
            Collection of words from line.
        """
        match line_indexer:
            case None:
                yield from (self[i, None, slice(None)] for i in self.para_ids)
            case _:
                yield from (
                    self[None, i, slice(None)] for i in self.line_ids[line_indexer]
                )


class BBoxSchema(Struct):
    """
    Schema Representing OCR data with Bounding Box. 

    This class is used to store OCR results in  Numpy Array.

    Attributes:
        parent_ids (list[int]): parent id for the OCR blocks. 
        texts (list[str]): Extracted text content.
        bboxes (list[BBox]): Bounding box for the text.
    """
    parent_ids: list[int] = field(name="parentIDs")
    texts: list[str]
    bboxes: list[BBox]

    def to_python(self) -> OcrBlockCollection:
        """
        Convert the BBox Schema data into OcrBlockCollections.

        This method converts the data into into numpy arrays and returns them into the OcrBlock Collection.

        Returns :
            OcrBlockCollection: Collection containing parent_ids, texts  and bounding boxes as numpy arrays.
        """
        return OcrBlockCollection(
            parent_ids=np.array(self.parent_ids, dtype=int),
            texts=np.array(self.texts, dtype=str),
            bboxes=np.array(self.bboxes, dtype=int),
        )


class OcrBlock(NamedTuple):
    """
        Represents a single OCR block.

        This class stores information for one detected text element ,including its parent relationship ,text content and bounding box

        Attributes :
            parent_id (int): parent id for OCR block
            text (str): Extracted text content 
            bbox (Vector[Shape[Literal[4]], np.int_]): bounding box coordinates in format [x1,y1,x2,y2].

    """
    parent_id: int
    text: str
    bbox: Vector[Shape[Literal[4]], np.int_]

    def as_textbox(self) -> TextBlock:
        """
            Converts OCR data into Textblock. 

            Returns: 
                TextBlock: Object containing text and bounding box coordinates.  
        """
        return TextBlock(text=self.text, bbox=self.bbox)


class TextBlock(NamedTuple):
    """
        Represents a Text Block.

        This class stores text and its corresponding Bounding box in Text Block. 

        Attributes:
            text (str): the extracted text content. 
            bbox (Vector[Shape[Literal[4]], np.int_]): vector containing four coordinates of the bounding box. 

    """
    text: str
    bbox: Vector[Shape[Literal[4]], np.int_]


Para = NewType("Para", OcrBlock)
Line = NewType("Line", OcrBlock)
Word = NewType("Word", OcrBlock)

@dataclass
class TextBlockCollection(Sized, ABC):
    """
    Abstract Dataclass representing a collection of text blocks.
    This class defines an interface for the collection of OCR text elements (paragraph , lines , words).
    It stores text data amd bounding boxes.


    Attributes: 
        parent_id (IntVector): Parent id for the text block.
        texts (StrVector): Array of text vector.
        bboxes (Array2D): Bounding Box for text element in format [x1,y1,x2,y2].
    
    This is the abstract class , so the subclasses must implement indexing and colection-specific behavior.

    """
    parent_ids: IntVector
    texts: StrVector
    bboxes: Array2D[Shape[int, Literal[4]], np.int_]

    @abstractmethod
    def item(self) -> OcrBlock:
        """
        Returns a single OcrBlock from collection. 

        This method expects  the collection to contain exactly one element. 
        Error is raised if there is more than one element.

        Returns: 
            OcrBlock: Single OCR block. 

        Raises:
            ValueError: if collection contains more than one element. 
        """
        if self.texts.size != 1:
            raise ValueError("Too many items in OcrResult")
        return OcrBlock(
            parent_id=self.parent_ids[0],
            text=self.texts[0],
            bbox=self.bboxes[0],
        )

    @abstractmethod
    def as_block(self) -> TextBlock:
        """
        Combine multiple text elements into single TextBlock. 

        This method merges all text entries into a single string seperated by paragraph seperators and calculates the bounding box for each text element.

        Returns:
            TextBlock: Aggregated text block with combined bounding box. 

        """
        bbox_min = self.bboxes.min(axis=0)
        bbox_max = self.bboxes.max(axis=0)
        bbox = np.r_[bbox_min[:2], bbox_max[2:]]
        return TextBlock(text=PARA_SEP.join(self.texts), bbox=bbox)

    @abstractmethod
    def __len__(self) -> int:
        """
        Returns the number of elements in that collection. 
        Returns:
            int: Total number of text elements. 
        """
        return self.count()

    @abstractmethod
    def count(self) -> int:
        """
        Returns the total number of text element in the collections.

        Returns: 
            int: Size of the text elemens in the collections. 
        """
        return self.texts.size

    @abstractmethod
    def first(self) -> OcrBlock:
        """
        Returns the First OcrBlock from the collections.

        Returns:                
            OcrBlock: First Element. 
        """
        return self.at(0)

    @abstractmethod
    def last(self) -> OcrBlock:
        """
        Returns the last OcrBlock from the collections.

        Returns:                
            OcrBlock: Last Element. 
        """
        return self.at(-1)

    @abstractmethod
    def at(self, index: int) -> OcrBlock:
        """
        Return the Ocr Block at a specific index. 

        Args:
            index (int): index for the OcrBlock.
        
        Returns:
            OcrBlock: Selected element.
        """
        return self[index]

    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> OcrBlock: ...

    @overload
    @abstractmethod
    def __getitem__(self, index: MultiIndexer | None) -> TextBlockCollection: ...

    @abstractmethod
    def __getitem__(self, index: Indexer) -> TextBlockCollection | OcrBlock: ...

    @classmethod
    def from_ocr(cls, ocr_collection: OcrBlockCollection) -> Self:
        """
        Creates the Text Collectionblock from the ocr block collection. 

        Args:
            ocr_collection (OcrBlockCollection): Source OCR data.

        Returns:
            TextBlockCollection: New Collection with copeid data.
        """
        return cls(
            parent_ids=ocr_collection.parent_ids,
            texts=ocr_collection.texts,
            bboxes=ocr_collection.bboxes,
        )


class ParaCollection(TextBlockCollection):
    """
    Represents a collection of paragraphs 

    This class provides operations for paragraph collections,
    extending TextBlockCollection . It returns Para Objects for single elements 
    and suports indexing, slicing and aggregation at the paragraph level
    
    Attributes:
        parent_id (IntVector): Parent id for the text block.
        texts (StrVector): Array of text vector.
        bboxes (Array2D): Bounding Box for text element in format [x1,y1,x2,y2].
    """
    parent_ids: IntVector
    texts: StrVector
    bboxes: Array2D[Shape[int, Literal[4]], np.int_]

    def item(self) -> Para:
        """
        Return a single paragraph as a Para Object.

        Returns:
            Para: Single Paragraph element. 
        
        Raises:
            ValueError: if collection contains more than one element.
        """
        return Para(super().item())

    def as_block(self) -> TextBlock:
        """
        Combine all paragraphs into a single TextBlock.
        
        Merges all paragraphs texts using paragraph seperators and computes bounding box.

        Returns: 
            TextBlock: Aggregated paragraph block.
        """
        bbox_min = self.bboxes.min(axis=0)
        bbox_max = self.bboxes.max(axis=0)
        bbox = np.r_[bbox_min[:2], bbox_max[2:]]
        return TextBlock(text=PARA_SEP.join(self.texts), bbox=bbox)

    def __len__(self) -> int:
        """
        Returns the number of paragraphs in the collections. 

        Returns:
            int: Total number of paragraphs.

        """
        return super().count()

    def count(self) -> int:
        """
        Returns the total nuber of paragraphs.

        Returns:
            int: Total number of paragraphs.
        """
        return super().count()

    def first(self) -> Para:
        """
        Returns the first paragraph from Collection.

        Returns:
            Para : first paragraph element.
        """
        return Para(super().first())

    def last(self) -> Para:
        """
        Returns the last paragraph from collection. 

        Returns:
            Para: last paragraph element.
        """
        return Para(super().last())

    def at(self, index: int) -> Para:
        """
        Returns the paragraph at a specified index.

        Args:
            index (int): Position of the paragraph.

        Returns: 
            Para: paragraph at specified index.  
        
        """
        return Para(super().at(index))

    @overload
    def __getitem__(self, index: int) -> Para: ...

    @overload
    def __getitem__(self, index: MultiIndexer | None) -> ParaCollection: ...

    def __getitem__(self, index: Indexer) -> ParaCollection | Para:
        """
        Retrives paragraph by indexing.
        
        if index is int then
            Returns: Para object.
        else (for multiIndexer)
            Returns: ParaCollection.

        Args: 
            index (Indexer): Index or Indexing sequence.

        Returns: 
            Para or ParaCollection: Based on index type. 
        
        """
        if isinstance(index, int):
            return Para(
                OcrBlock(
                    parent_id=self.parent_ids[index],
                    text=self.texts[index],
                    bbox=self.bboxes[index],
                )
            )
        return ParaCollection(
            parent_ids=self.parent_ids[index],
            texts=self.texts[index],
            bboxes=self.bboxes[index],
        )


class LineCollection(TextBlockCollection):
    """
    Represents a collection of Lines. 

    This class provides operations for line collections,
    extending TextBlockCollection . It returns Line Objects for single elements 
    and suports indexing, slicing and aggregation at the Line
    
    Attributes :
        parent_id (IntVector): Parent id for the text block.
        texts (StrVector): Array of text vector.
        bboxes (Array2D): Bounding Box for text element in format [x1,y1,x2,y2].
    """
    parent_ids: IntVector
    texts: StrVector
    bboxes: Array2D[Shape[int, Literal[4]], np.int_]

    def item(self) -> Line:
        """
        Return a single Line as a line Object.

        Returns:
            Line: Single Line element. 
        
        Raises:
            ValueError: if collection contains more than one element.
        """
        return Line(super().item())

    def as_block(self) -> TextBlock:
        """
        Combine all lines into a single TextBlock.
        
        Merges all line text using line seperators along with  bounding box computations.

        Returns: 
            TextBlock: Aggregated line block.
        """
        bbox_min = self.bboxes.min(axis=0)
        bbox_max = self.bboxes.max(axis=0)
        bbox = np.r_[bbox_min[:2], bbox_max[2:]]
        return TextBlock(text=LINE_SEP.join(self.texts), bbox=bbox)

    def __len__(self) -> int:
        """
        Returns the number of lines in the collections.

        Returns:
            int: Total number of lines.

        """
        return super().count()

    def count(self) -> int:
        """
        Returns the total nuber of lines.

        Returns:
            int: Total number of lines.
        """
        return super().count()

    def first(self) -> Line:
        """
        Returns the first line from Collection.

        Returns:
            Line: first line element.
        """
        return Line(super().first())

    def last(self) -> Line:
        """
        Returns the last line from Collection.

        Returns:
            Line: last line element.
        """
        return Line(super().last())

    def at(self, index: int) -> Line:
        """
        Returns the line at a specified index.

        Args:
            index (int): Position of the line.

        Returns: 
            Line: line at specified index.  
        
        """
        return Line(super().at(index))

    @overload
    def __getitem__(self, index: int) -> Line: ...

    @overload
    def __getitem__(self, index: MultiIndexer | None) -> LineCollection: ...

    def __getitem__(self, index: Indexer) -> LineCollection | Line:
        """
        Retrives line by indexing
        
        if index is int  then
            Returns: Line object.
        else (for multiIndexer)
            Returns: LineCollection. 

        Args: 
            index (Indexer):  Index or Indexing sequence.

        Returns: 
            Line or LineCollection:  Based on index type. 
        """
        if isinstance(index, int):
            return Line(
                OcrBlock(
                    parent_id=self.parent_ids[index],
                    text=self.texts[index],
                    bbox=self.bboxes[index],
                )
            )
        return LineCollection(
            parent_ids=self.parent_ids[index],
            texts=self.texts[index],
            bboxes=self.bboxes[index],
        )


class WordCollection(TextBlockCollection):
    """
    Represents a collection of words. 

    This class provides operations for word collections,
    extending TextBlockCollection . It returns Word Objects for single elements 
    and suports indexing, slicing and aggregation at the word level
    
    Attributes:
        parent_id (IntVector): Parent id for the text block.
        texts (StrVector): Array of text vector.
        bboxes (Array2D): Bounding Box for text element in format [x1,y1,x2,y2].
    """
    parent_ids: IntVector
    texts: StrVector
    bboxes: Array2D[Shape[int, Literal[4]], np.int_]

    def item(self) -> Word:
        """
        Return a single word as a Word Object.

        Returns:
            Line: Single Word element. 
        
        Raises:
            ValueError: if collection contains more than one element.
        """
        return Word(super().item())

    def as_block(self) -> TextBlock:
        """
        Combine all words into a single TextBlock.
        
        Merges all words text using word seperators along with  bounding box computations.

        Returns: 
            TextBlock: Aggregated word block.
        """
        bbox_min = self.bboxes.min(axis=0)
        bbox_max = self.bboxes.max(axis=0)
        bbox = np.r_[bbox_min[:2], bbox_max[2:]]
        return TextBlock(text=WORD_SEP.join(self.texts), bbox=bbox)

    def __len__(self) -> int:
        """
        Returns the number of words in the collections.

        Returns:
            int: Total number of words.
    
        """
        return len(super())

    def count(self) -> int:
        """
        Returns the total nuber of words.

        Returns:
            int: Total number of words.
        """
        return super().count()

    def first(self) -> Word:
        """
        Returns the first word from Collection.

        Returns:
            Word: first word element.
        """
        return Word(super().first())

    def last(self) -> Word:
        """
        Returns the last word from Collection

        Returns:
            Word: last word element.
        """
        return Word(super().last())

    def at(self, index: int) -> Word:
        """
        Returns the word at a specified index.

        Args:
            index (int): Position of the word.

        Returns: 
            Word: word at specified index.  
        
        """
        return Word(super().at(index))

    @overload
    def __getitem__(self, index: int) -> Word: ...

    @overload
    def __getitem__(self, index: MultiIndexer | None) -> WordCollection: ...

    def __getitem__(self, index: Indexer) -> WordCollection | Word:
        """
        Retrives word by indexing
        
        if index is int  then
            Returns: word object.
        else (for multiIndexer)
            Returns: WordCollection.

        Args: 
            index (Indexer): Index or Indexing sequence.

        Returns: 
            Word or WordCollection: Based on index type. 
        """
        if isinstance(index, int):
            return Word(
                OcrBlock(
                    parent_id=self.parent_ids[index],
                    text=self.texts[index],
                    bbox=self.bboxes[index],
                )
            )
        return WordCollection(
            parent_ids=self.parent_ids[index],
            texts=self.texts[index],
            bboxes=self.bboxes[index],
        )

if __name__ == "__main__":
    main()
