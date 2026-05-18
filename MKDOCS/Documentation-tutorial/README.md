# MkDocs Documentation Tutorial

This is a set up a MkDocs documentation site. It also covers how to add Python docs, TypeScript API docs, and OpenAPI documentation into the same project.

## 1. Set Up MkDocs

Start by creating a Python project. If you are using `uv`, install MkDocs and the Material theme:

```bash
uv add mkdocs mkdocs-material
```

Now create a new MkDocs project in the current folder:

```bash
mkdocs new .
```

This creates a `docs` folder. Inside that folder, you will find an `index.md` file, which is the first page of your documentation site.

Run the local development server to preview the site:

```bash
mkdocs serve --livereload
```

You can customize the site from the `mkdocs.yml` file. This is where you add the theme, navigation, plugins, and other styling options.

## 2. Add Python Documentation

To show documentation from Python docstrings, add the Python file or function reference inside a Markdown file.

For example, if `main.py` is the file name:

```md
::: main
```

If you only want to document the `add` function inside `main.py`, use:

```md
::: main.add
```

This keeps the documentation close to the real code, so updates are easier to manage.

## 3. Add TypeScript Documentation

For TypeScript, first set up a basic TypeScript project:

```bash
npm init -y
npm install typescript --save-dev
npx tsc --init
```

Put your TypeScript files inside a `src` folder.

Update `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES6",
    "module": "commonjs",
    "rootDir": "./src",
    "outDir": "./dist",
    "strict": true
  }
}
```

Install TypeDoc:

```bash
npm install --save-dev typedoc
```

Then create a `typedoc.json` file:

```json
{
  "entryPoints": ["src/index.ts"],
  "out": "docs/api-generated",
  "excludePrivate": true,
  "excludeProtected": true,
  "includeVersion": true,
  "name": "Task Manager API Documentation"
}
```

Generate the documentation:

```bash
npx typedoc
```

This will generate the API documentation inside:

```text
docs/api-generated/
```

## 4. Generate Markdown API Docs from TypeScript

If you want the TypeScript API documentation as Markdown files, install the TypeDoc Markdown plugin:

```bash
npm install typedoc typedoc-plugin-markdown --save-dev
```

Update `typedoc.json`:

```json
{
  "entryPoints": ["src/index.ts"],
  "out": "docs/api",
  "plugin": ["typedoc-plugin-markdown"],
  "excludePrivate": true,
  "excludeProtected": true,
  "name": "Task Manager API"
}
```

Run TypeDoc again:

```bash
npx typedoc
```

After that, start MkDocs again:

```bash
mkdocs serve --livereload
```

## 5. Add OpenAPI Documentation

To show OpenAPI documentation inside MkDocs, install the Swagger UI tag plugin:

```bash
pip install mkdocs-swagger-ui-tag
```

Add the required JavaScript and CSS files to `mkdocs.yml`:

```yaml
extra_javascript:
  - https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js
  - https://unpkg.com/swagger-ui-dist/swagger-ui-standalone-preset.js

extra_css:
  - https://unpkg.com/swagger-ui-dist/swagger-ui.css
```

Create an `api.md` file inside the `docs` folder and add the OpenAPI viewer.

Make sure the `spec-url` points to the correct OpenAPI JSON file:

```html
<redoc spec-url="openapi.json"></redoc>

<script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
```

## Final 

Once everything is done , run:

```bash
mkdocs serve --livereload
```

Open the local MkDocs site in your browser and check that the normal pages, Python docs, TypeScript docs, and OpenAPI docs are all loading proper

