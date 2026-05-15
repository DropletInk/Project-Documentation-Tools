<a id="app2.ocr"></a>

# app2.ocr

<a id="app2.ocr.main"></a>

#### main

```python
def main()
```

Hello from documentation-tutorial!

<a id="app2.ocr.OcrBlockCollection"></a>

## OcrBlockCollection Objects

```python
@dataclass
class OcrBlockCollection(Sized)
```

Represents a collection of OCR blocks for paragraph,lines and words.

This class stores the OCR  results  in a structured  format using Numpy Arrays.

**Attributes**:

- `parent_ids` _IntVector_ - Parent id for the ocr block.
- `texts` _StrVector_ - Extracted Text content.
- `bboxes` _Array2D_ - Bounding box for the text.

<a id="app2.ocr.OcrBlockCollection.__post_init__"></a>

#### \_\_post\_init\_\_

```python
def __post_init__() -> None
```

Initializes indices for paragraph , lines , words 

Splits OCR blocks into :
- Paragraph ids
- Line ids
- word ids

<a id="app2.ocr.OcrBlockCollection.__len__"></a>

#### \_\_len\_\_

```python
def __len__() -> int
```

Returns the number of items.

<a id="app2.ocr.OcrBlockCollection.count"></a>

#### count

```python
def count() -> int
```

Returns the calculated size of the text content.

<a id="app2.ocr.OcrBlockCollection.__getitem__"></a>

#### \_\_getitem\_\_

```python
def __getitem__(levels: int
                | MultiIndexer
                | tuple[Indexer]
                | tuple[Indexer, Indexer]
                | tuple[Indexer, Indexer, Indexer],
                paragraph) -> TextBlockCollection
```

Generates OCR blocks

indexing is in form:
object[para(0)],
object[para(0),line(1)],
object[para(0),line(1),word(2)],

**Returns**:

  WordCollection, LineCollection, ParaCollection depending on the indexing.

<a id="app2.ocr.OcrBlockCollection.pick_indices"></a>

#### pick\_indices

```python
def pick_indices(indexer: MultiIndexer) -> OcrBlockCollection
```

Returns OcrBlockCollection with the selected indices

This Method filters the current collection based on the provided indexer and returns a new object with corresponding parent_id , texts and bboxes

**Arguments**:

- `indexer` _MultiIndexer_ - Index , Slice , List , Boolean vector to select element from collections.
  

**Returns**:

- `OcrBlockCollection` - Collection of the filtered items.
  

**Raises**:

- `TypeError` - If the indexer is None.

<a id="app2.ocr.OcrBlockCollection.item"></a>

#### item

```python
def item() -> OcrBlock
```

Returns Single OcrBlock from Collection.

This Method checks whether the collection contains only one elemenet or not
ifmore than one is present then it raises error.

**Returns**:

- `OcrBlock` - The Single OCR Block in the collection.
  

**Raises**:

- `ValueError` - If the collection contains more than one element.

<a id="app2.ocr.OcrBlockCollection.first"></a>

#### first

```python
def first() -> OcrBlock
```

Returns the first OCR blcok In collection.

<a id="app2.ocr.OcrBlockCollection.last"></a>

#### last

```python
def last() -> OcrBlock
```

Returns the Last OCR blcok In collection.

<a id="app2.ocr.OcrBlockCollection.at"></a>

#### at

```python
def at(index: int) -> OcrBlock
```

Returns Ocr Block at specific index.

**Arguments**:

- `index` _int_ - Position of the element.
  

**Returns**:

- `OcrBlock` - The selected Ocr Block.

<a id="app2.ocr.OcrBlockCollection.lines_by_para"></a>

#### lines\_by\_para

```python
def lines_by_para(
        para_indexer: MultiIndexer | None = None) -> Iterator[LineCollection]
```

Yield lines from paragraph

**Arguments**:

- `para_indexer` _MultiIndexer,optional_ - index to filter paragraph.
  

**Yields**:

  Collection of Lines from the paragraph.

<a id="app2.ocr.OcrBlockCollection.words_by_para"></a>

#### words\_by\_para

```python
def words_by_para(
        para_indexer: MultiIndexer | None = None) -> Iterator[WordCollection]
```

Yield words from paragraph

**Arguments**:

- `para_indexer` _MultiIndexer,optional_ - index to filter paragraph.
  

**Yields**:

  Collection of words from the paragraph.

<a id="app2.ocr.OcrBlockCollection.words_by_line"></a>

#### words\_by\_line

```python
def words_by_line(
        line_indexer: MultiIndexer | None = None) -> Iterator[WordCollection]
```

Yield words from lines.

**Arguments**:

- `line_indexer` _MultiIndexer,optional_ - index to filter line.
  

**Yields**:

  Collection of words from line.

<a id="app2.ocr.BBoxSchema"></a>

## BBoxSchema Objects

```python
class BBoxSchema(Struct)
```

Schema Representing OCR data with Bounding Box.

This class is used to store OCR results in  Numpy Array.

**Attributes**:

- `parent_ids` _list[int]_ - parent id for the OCR blocks.
- `texts` _list[str]_ - Extracted text content.
- `bboxes` _list[BBox]_ - Bounding box for the text.

<a id="app2.ocr.BBoxSchema.to_python"></a>

#### to\_python

```python
def to_python() -> OcrBlockCollection
```

Convert the BBox Schema data into OcrBlockCollections.

This method converts the data into into numpy arrays and returns them into the OcrBlock Collection.

Returns :
    OcrBlockCollection: Collection containing parent_ids, texts  and bounding boxes as numpy arrays.

<a id="app2.ocr.OcrBlock"></a>

## OcrBlock Objects

```python
class OcrBlock(NamedTuple)
```

Represents a single OCR block.

This class stores information for one detected text element ,including its parent relationship ,text content and bounding box

Attributes :
    parent_id (int): parent id for OCR block
    text (str): Extracted text content 
    bbox (Vector[Shape[Literal[4]], np.int_]): bounding box coordinates in format [x1,y1,x2,y2].

<a id="app2.ocr.OcrBlock.as_textbox"></a>

#### as\_textbox

```python
def as_textbox() -> TextBlock
```

Converts OCR data into Textblock.

**Returns**:

- `TextBlock` - Object containing text and bounding box coordinates.

<a id="app2.ocr.TextBlock"></a>

## TextBlock Objects

```python
class TextBlock(NamedTuple)
```

Represents a Text Block.

This class stores text and its corresponding Bounding box in Text Block.

**Attributes**:

- `text` _str_ - the extracted text content.
- `bbox` _Vector[Shape[Literal[4]], np.int_]_ - vector containing four coordinates of the bounding box.

<a id="app2.ocr.TextBlockCollection"></a>

## TextBlockCollection Objects

```python
@dataclass
class TextBlockCollection(Sized, ABC)
```

Abstract Dataclass representing a collection of text blocks.
This class defines an interface for the collection of OCR text elements (paragraph , lines , words).
It stores text data amd bounding boxes.


**Attributes**:

- `parent_id` _IntVector_ - Parent id for the text block.
- `texts` _StrVector_ - Array of text vector.
- `bboxes` _Array2D_ - Bounding Box for text element in format [x1,y1,x2,y2].
  
  This is the abstract class , so the subclasses must implement indexing and colection-specific behavior.

<a id="app2.ocr.TextBlockCollection.item"></a>

#### item

```python
@abstractmethod
def item() -> OcrBlock
```

Returns a single OcrBlock from collection.

This method expects  the collection to contain exactly one element.
Error is raised if there is more than one element.

**Returns**:

- `OcrBlock` - Single OCR block.
  

**Raises**:

- `ValueError` - if collection contains more than one element.

<a id="app2.ocr.TextBlockCollection.as_block"></a>

#### as\_block

```python
@abstractmethod
def as_block() -> TextBlock
```

Combine multiple text elements into single TextBlock.

This method merges all text entries into a single string seperated by paragraph seperators and calculates the bounding box for each text element.

**Returns**:

- `TextBlock` - Aggregated text block with combined bounding box.

<a id="app2.ocr.TextBlockCollection.__len__"></a>

#### \_\_len\_\_

```python
@abstractmethod
def __len__() -> int
```

Returns the number of elements in that collection.

**Returns**:

- `int` - Total number of text elements.

<a id="app2.ocr.TextBlockCollection.count"></a>

#### count

```python
@abstractmethod
def count() -> int
```

Returns the total number of text element in the collections.

**Returns**:

- `int` - Size of the text elemens in the collections.

<a id="app2.ocr.TextBlockCollection.first"></a>

#### first

```python
@abstractmethod
def first() -> OcrBlock
```

Returns the First OcrBlock from the collections.

**Returns**:

- `OcrBlock` - First Element.

<a id="app2.ocr.TextBlockCollection.last"></a>

#### last

```python
@abstractmethod
def last() -> OcrBlock
```

Returns the last OcrBlock from the collections.

**Returns**:

- `OcrBlock` - Last Element.

<a id="app2.ocr.TextBlockCollection.at"></a>

#### at

```python
@abstractmethod
def at(index: int) -> OcrBlock
```

Return the Ocr Block at a specific index.

**Arguments**:

- `index` _int_ - index for the OcrBlock.
  

**Returns**:

- `OcrBlock` - Selected element.

<a id="app2.ocr.TextBlockCollection.from_ocr"></a>

#### from\_ocr

```python
@classmethod
def from_ocr(cls, ocr_collection: OcrBlockCollection) -> Self
```

Creates the Text Collectionblock from the ocr block collection.

**Arguments**:

- `ocr_collection` _OcrBlockCollection_ - Source OCR data.
  

**Returns**:

- `TextBlockCollection` - New Collection with copeid data.

<a id="app2.ocr.ParaCollection"></a>

## ParaCollection Objects

```python
class ParaCollection(TextBlockCollection)
```

Represents a collection of paragraphs

This class provides operations for paragraph collections,
extending TextBlockCollection . It returns Para Objects for single elements
and suports indexing, slicing and aggregation at the paragraph level

**Attributes**:

- `parent_id` _IntVector_ - Parent id for the text block.
- `texts` _StrVector_ - Array of text vector.
- `bboxes` _Array2D_ - Bounding Box for text element in format [x1,y1,x2,y2].

<a id="app2.ocr.ParaCollection.item"></a>

#### item

```python
def item() -> Para
```

Return a single paragraph as a Para Object.

**Returns**:

- `Para` - Single Paragraph element.
  

**Raises**:

- `ValueError` - if collection contains more than one element.

<a id="app2.ocr.ParaCollection.as_block"></a>

#### as\_block

```python
def as_block() -> TextBlock
```

Combine all paragraphs into a single TextBlock.

Merges all paragraphs texts using paragraph seperators and computes bounding box.

**Returns**:

- `TextBlock` - Aggregated paragraph block.

<a id="app2.ocr.ParaCollection.__len__"></a>

#### \_\_len\_\_

```python
def __len__() -> int
```

Returns the number of paragraphs in the collections.

**Returns**:

- `int` - Total number of paragraphs.

<a id="app2.ocr.ParaCollection.count"></a>

#### count

```python
def count() -> int
```

Returns the total nuber of paragraphs.

**Returns**:

- `int` - Total number of paragraphs.

<a id="app2.ocr.ParaCollection.first"></a>

#### first

```python
def first() -> Para
```

Returns the first paragraph from Collection.

**Returns**:

  Para : first paragraph element.

<a id="app2.ocr.ParaCollection.last"></a>

#### last

```python
def last() -> Para
```

Returns the last paragraph from collection.

**Returns**:

- `Para` - last paragraph element.

<a id="app2.ocr.ParaCollection.at"></a>

#### at

```python
def at(index: int) -> Para
```

Returns the paragraph at a specified index.

**Arguments**:

- `index` _int_ - Position of the paragraph.
  

**Returns**:

- `Para` - paragraph at specified index.

<a id="app2.ocr.ParaCollection.__getitem__"></a>

#### \_\_getitem\_\_

```python
def __getitem__(index: Indexer) -> ParaCollection | Para
```

Retrives paragraph by indexing.

if index is int then
Returns: Para object.
else (for multiIndexer)
Returns: ParaCollection.

**Arguments**:

- `index` _Indexer_ - Index or Indexing sequence.
  

**Returns**:

  Para or ParaCollection: Based on index type.

<a id="app2.ocr.LineCollection"></a>

## LineCollection Objects

```python
class LineCollection(TextBlockCollection)
```

Represents a collection of Lines. 

This class provides operations for line collections,
extending TextBlockCollection . It returns Line Objects for single elements 
and suports indexing, slicing and aggregation at the Line

Attributes :
    parent_id (IntVector): Parent id for the text block.
    texts (StrVector): Array of text vector.
    bboxes (Array2D): Bounding Box for text element in format [x1,y1,x2,y2].

<a id="app2.ocr.LineCollection.item"></a>

#### item

```python
def item() -> Line
```

Return a single Line as a line Object.

**Returns**:

- `Line` - Single Line element.
  

**Raises**:

- `ValueError` - if collection contains more than one element.

<a id="app2.ocr.LineCollection.as_block"></a>

#### as\_block

```python
def as_block() -> TextBlock
```

Combine all lines into a single TextBlock.

Merges all line text using line seperators along with  bounding box computations.

**Returns**:

- `TextBlock` - Aggregated line block.

<a id="app2.ocr.LineCollection.__len__"></a>

#### \_\_len\_\_

```python
def __len__() -> int
```

Returns the number of lines in the collections.

**Returns**:

- `int` - Total number of lines.

<a id="app2.ocr.LineCollection.count"></a>

#### count

```python
def count() -> int
```

Returns the total nuber of lines.

**Returns**:

- `int` - Total number of lines.

<a id="app2.ocr.LineCollection.first"></a>

#### first

```python
def first() -> Line
```

Returns the first line from Collection.

**Returns**:

- `Line` - first line element.

<a id="app2.ocr.LineCollection.last"></a>

#### last

```python
def last() -> Line
```

Returns the last line from Collection.

**Returns**:

- `Line` - last line element.

<a id="app2.ocr.LineCollection.at"></a>

#### at

```python
def at(index: int) -> Line
```

Returns the line at a specified index.

**Arguments**:

- `index` _int_ - Position of the line.
  

**Returns**:

- `Line` - line at specified index.

<a id="app2.ocr.LineCollection.__getitem__"></a>

#### \_\_getitem\_\_

```python
def __getitem__(index: Indexer) -> LineCollection | Line
```

Retrives line by indexing

if index is int  then
Returns: Line object.
else (for multiIndexer)
Returns: LineCollection.

**Arguments**:

- `index` _Indexer_ - Index or Indexing sequence.
  

**Returns**:

  Line or LineCollection:  Based on index type.

<a id="app2.ocr.WordCollection"></a>

## WordCollection Objects

```python
class WordCollection(TextBlockCollection)
```

Represents a collection of words.

This class provides operations for word collections,
extending TextBlockCollection . It returns Word Objects for single elements
and suports indexing, slicing and aggregation at the word level

**Attributes**:

- `parent_id` _IntVector_ - Parent id for the text block.
- `texts` _StrVector_ - Array of text vector.
- `bboxes` _Array2D_ - Bounding Box for text element in format [x1,y1,x2,y2].

<a id="app2.ocr.WordCollection.item"></a>

#### item

```python
def item() -> Word
```

Return a single word as a Word Object.

**Returns**:

- `Line` - Single Word element.
  

**Raises**:

- `ValueError` - if collection contains more than one element.

<a id="app2.ocr.WordCollection.as_block"></a>

#### as\_block

```python
def as_block() -> TextBlock
```

Combine all words into a single TextBlock.

Merges all words text using word seperators along with  bounding box computations.

**Returns**:

- `TextBlock` - Aggregated word block.

<a id="app2.ocr.WordCollection.__len__"></a>

#### \_\_len\_\_

```python
def __len__() -> int
```

Returns the number of words in the collections.

**Returns**:

- `int` - Total number of words.

<a id="app2.ocr.WordCollection.count"></a>

#### count

```python
def count() -> int
```

Returns the total nuber of words.

**Returns**:

- `int` - Total number of words.

<a id="app2.ocr.WordCollection.first"></a>

#### first

```python
def first() -> Word
```

Returns the first word from Collection.

**Returns**:

- `Word` - first word element.

<a id="app2.ocr.WordCollection.last"></a>

#### last

```python
def last() -> Word
```

Returns the last word from Collection

**Returns**:

- `Word` - last word element.

<a id="app2.ocr.WordCollection.at"></a>

#### at

```python
def at(index: int) -> Word
```

Returns the word at a specified index.

**Arguments**:

- `index` _int_ - Position of the word.
  

**Returns**:

- `Word` - word at specified index.

<a id="app2.ocr.WordCollection.__getitem__"></a>

#### \_\_getitem\_\_

```python
def __getitem__(index: Indexer) -> WordCollection | Word
```

Retrives word by indexing

if index is int  then
Returns: word object.
else (for multiIndexer)
Returns: WordCollection.

**Arguments**:

- `index` _Indexer_ - Index or Indexing sequence.
  

**Returns**:

  Word or WordCollection: Based on index type.

