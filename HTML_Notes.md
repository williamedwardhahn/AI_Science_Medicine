
# Beginner's Guide to HTML

HTML stands for HyperText Markup Language. It's the standard markup language used to create web pages. In this primer, we'll go through the basics of HTML.

## Table of Contents
- [Understanding HTML](#understanding-html)
- [HTML Tags](#html-tags)
- [Creating a Basic HTML Document](#creating-a-basic-html-document)
- [HTML Elements](#html-elements)
- [HTML Attributes](#html-attributes)
- [HTML Links and Images](#html-links-and-images)

## Understanding HTML

HTML is a markup language that uses `tags` to define `elements` on the page. These elements include headings, paragraphs, links, images, and more.

## HTML Tags

Tags are used to define HTML elements. They are surrounded by angle brackets `< >`. Most HTML tags come in pairs: an opening tag `<tag>` and a closing tag `</tag>`. The content goes between these two tags.

```html
<tag>Content goes here...</tag>
```

## Creating a Basic HTML Document

Let's start by creating a very basic HTML document.

```html
<!DOCTYPE html>
<html>
  <head>
    <title>My First Web Page</title>
  </head>
  <body>
    <h1>Hello, World!</h1>
  </body>
</html>
```

In the above example:

- `<!DOCTYPE html>` is the document type declaration and is used to tell the browser that this is an HTML5 document.
- `<html>` is the root element of an HTML page.
- `<head>` contains meta-information about the document such as its title.
- `<title>` defines the title of the document.
- `<body>` contains the content that will be visible on the page.
- `<h1>` defines a top-level heading.

## HTML Elements

HTML elements are defined by tags. Here are a few basic ones:

- Headings: HTML headings are defined with the `<h1>` to `<h6>` tags.

```html
<h1>This is a heading 1</h1>
<h2>This is a heading 2</h2>
```

- Paragraphs: HTML paragraphs are defined with the `<p>` tag.

```html
<p>This is a paragraph.</p>
<p>This is another paragraph.</p>
```

- Links: HTML links are defined with the `<a>` tag.

```html
<a href="https://www.example.com">This is a link</a>
```

## HTML Attributes

HTML attributes are used to provide additional information about HTML elements. They are always specified in the start tag.

- The `<a>` tag can have an `href` attribute that provides the URL of the page the link goes to.

```html
<a href="https://www.example.com">This is a link</a>
```

- The `<img>` tag can have `src` (source) and `alt` (alternative text) attributes.

```html
<img src="image.jpg" alt="A beautiful view">
```

## HTML Links and Images

Here is a more complex example combining links and images:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>My First Web Page</title>
  </head>
  <body>
    <h1>My First Web Page</h1>
    <p>Welcome to my first web page. Here's a fun image and a link:</p>
    <img src="fun.jpg" alt="A fun image">
    <p>Want to learn more? <a href="https://www.example.com">Click here!</a></p>
  </body>
</html>
```

In this example, we've added a paragraph of text, an image, and a link inside another paragraph.
