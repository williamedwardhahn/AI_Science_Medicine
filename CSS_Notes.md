# Beginner's Guide to CSS

CSS stands for Cascading Style Sheets. It's used to define styles for your web pages, including the design, layout, and variations in display for different devices and screen sizes. In this primer, we'll go through the basics of CSS.

## Table of Contents
- [Understanding CSS](#understanding-css)
- [How to Include CSS](#how-to-include-css)
- [CSS Syntax](#css-syntax)
- [CSS Selectors](#css-selectors)
- [CSS Colors](#css-colors)
- [CSS Fonts](#css-fonts)
- [CSS Box Model](#css-box-model)
- [CSS Positioning](#css-positioning)

## Understanding CSS

CSS is used to control the style and layout of multiple web pages all at once. External stylesheets are stored in CSS files. CSS works hand in hand with HTML; HTML files link to CSS files to apply the styles defined in the CSS file.

## How to Include CSS

There are three ways to include CSS in your HTML files:

1. Inline - by using the `style` attribute inside HTML elements.
2. Internal - by using a `<style>` block in the `<head>` section.
3. External - by linking to an external CSS file.

```html
<!-- Inline CSS -->
<p style="color:red;">This is an example of inline CSS.</p>

<!-- Internal CSS -->
<head>
<style>
  p {
    color: blue;
  }
</style>
</head>

<!-- External CSS -->
<head>
  <link rel="stylesheet" href="styles.css">
</head>
```

## CSS Syntax

A CSS rule-set consists of a selector and a declaration block. The selector points to the HTML element you want to style. The declaration block contains one or more declarations separated by semicolons.

```css
selector {
  property: value;
}
```

## CSS Selectors

CSS selectors are used to find the HTML elements you want to style.

- The element selector selects elements based on the element name.
- The `#id` selector selects the element with a specific id.
- The `.class` selector selects elements with a specific class attribute.

```css
/* Element Selector */
p {
  text-align: center;
  color: red;
}

/* ID Selector */
#myID {
  background-color: lightblue;
}

/* Class Selector */
.myClass {
  font-size: 25px;
}
```

## CSS Colors

CSS supports a wide variety of colors. These can be provided:

- By name: `red`, `green`, `blue`, etc.
- As RGB values: `rgb(255,0,0)`, `rgb(0,255,0)`, `rgb(0,0,255)`
- As HEX values: `#FF0000`, `#00FF00`, `#0000FF`

```css
p {
  color: red;
}

#myID {
  color: rgb(255,0,0);
}

.myClass {
  color: #FF0000;
}
```

## CSS Fonts

The CSS `font-family` property is used to specify the typeface that will be used by the browser.

```css
body {
  font-family: Arial, sans-serif;
}
```

## CSS Box Model

All HTML elements can be considered as boxes. The CSS box model is essentially a box that wraps around every HTML element. It consists of: margins, borders, padding, and the actual content.

```css
div {
  width: 300px;
  border: 25px solid green;
  padding: 25px;
  margin: 25px;
}
```

## CSS Positioning

CSS positioning

 properties allow you to position an element.

- `static`: HTML elements are positioned static by default. Static positioned elements are not affected by the top, bottom, left, and right properties.
- `relative`: A relative positioned element is positioned relative to its normal position.
- `fixed`: A fixed positioned element is positioned relative to the viewport.
- `absolute`: An absolute positioned element is positioned relative to the nearest positioned ancestor (instead of positioned relative to the viewport).

```css
#myID {
  position: absolute;
  top: 80px;
  right: 0;
  width: 200px;
  height: 100px;
}
```
