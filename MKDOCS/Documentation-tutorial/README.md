
===
## Steps to Set up the MkDocs 

first Setup your python project using uv
then

uv add mkdocs mkdocs-material

now 

mkdocs new .

This Creates the docs folder and under that there is a file  called index.md

now 
mkdocs serve --livereload



add some features in mkdocs.yml to add the style in the markdown files 


To add the python file containing doc string 

main is the name of the file in that folder

::: main                        

add is the function name under the main file

::: main.add 



for typescript file 

set up your typescript project 

npm init -y

npm install typescript --save-dev

npx tsc --init


add you ts file in src folder  

and then add this section in your tsconfig.json

{
  "compilerOptions": {
    "target": "ES6",
    "module": "commonjs",
    "rootDir": "./src",
    "outDir": "./dist",
    "strict": true
  }
}


then 

install 
npm install --save-dev typedoc

create typedoc.json

and add 
{
  "entryPoints": ["src/index.ts"],
  "out": "docs/api-generated",
  "excludePrivate": true,
  "excludeProtected": true,
  "includeVersion": true,
  "name": "Task Manager API Documentation"
}


To generate documentation 

npx typedoc

This creates 
docs/api-generated/



Now  add 
npm install typedoc-plugin-markdown --save-dev

Update typedoc.json

{
  "entryPoints": ["src/index.ts"],
  "out": "docs/api",
  "plugin": ["typedoc-plugin-markdown"]
}

again 
run 

npx typedoc

finally 

npm install typedoc typedoc-plugin-markdown --save-dev

update  typedoc.json

{
  "entryPoints": ["src/index.ts"],
  "out": "docs/api",
  "plugin": ["typedoc-plugin-markdown"],
  "excludePrivate": true,
  "excludeProtected": true,
  "name": "Task Manager API"
}

npx typedoc


mkdocs serve --livereload



### FOR OPEN API  json 
install

pip install mkdocs-swagger-ui-tag


add this in you mkdocs.yml

extra_javascript:
  - https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js
  - https://unpkg.com/swagger-ui-dist/swagger-ui-standalone-preset.js

extra_css:
  - https://unpkg.com/swagger-ui-dist/swagger-ui.css


create  a api.md file inside docs folder 

                    here give the correct path 
<redoc spec-url='openapi.json'></redoc>

<script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>