# Beginner's Guide to SVG

SVG stands for Scalable Vector Graphics. It's an XML-based vector image format for two-dimensional graphics, with support for interactivity and animation. In this primer, we'll go through the basics of SVG.

## Table of Contents
- [Understanding SVG](#understanding-svg)
- [SVG Elements](#svg-elements)
  - [The `<svg>` Element](#the-svg-element)
  - [The `<rect>` Element](#the-rect-element)
  - [The `<circle>` Element](#the-circle-element)
  - [The `<ellipse>` Element](#the-ellipse-element)
  - [The `<line>` Element](#the-line-element)
  - [The `<polyline>` Element](#the-polyline-element)
  - [The `<polygon>` Element](#the-polygon-element)
  - [The `<path>` Element](#the-path-element)
- [SVG Text](#svg-text)
- [SVG Styles and Colors](#svg-styles-and-colors)

## Understanding SVG

SVG images are defined in XML text files, which means they can be searched, indexed, scripted, and compressed. Also, SVG images do not lose any quality if they are zoomed or resized.

## SVG Elements

SVG has several shape elements. All SVG shapes are specified in the SVG coordinate system.

### The `<svg>` Element

The `<svg>` element is the root SVG element that contains all the other SVG elements. It can take two attributes: `width` and `height`, to define the width and the height of the SVG area.

```html
<svg width="500" height="500">
</svg>
```

### The `<rect>` Element

The `<rect>` element is used to create a rectangle. The `x` and `y` attributes define the left-top corner of the rectangle. The `width` and `height` attributes define the width and height of the rectangle.

```html
<svg width="500" height="500">
  <rect x="50" y="50" width="200" height="100" />
</svg>
```

### The `<circle>` Element

The `<circle>` element is used to create a circle. The `cx` and `cy` attributes define the x and y coordinates of the center of the circle. The `r` attribute defines the radius of the circle.

```html
<svg width="500" height="500">
  <circle cx="250" cy="250" r="200" />
</svg>
```

### The `<ellipse>` Element

The `<ellipse>` element is used to create an ellipse. The `cx` and `cy` attributes define the x and y coordinates of the center of the ellipse. The `rx` and `ry` attributes define the radii of the ellipse.

```html
<svg width="500" height="500">
  <ellipse cx="250" cy="250" rx="200" ry="100" />
</svg>
```

### The `<line>` Element

The `<line>` element is used to create a line. The `x1`, `y1`, `x2`, and `y2` attributes define the start and end points of the line.

```html
<svg width="500" height="500">
  <line x1="50" y1="50" x2="450" y2="450" />
</svg>
```

### The `<polyline>` Element

The `<polyline>` element is used to create any shape that consists of only straight lines. The `points` attribute defines the list of points in the shape.

```html
<svg width="500" height="500

">
  <polyline points="50,50 200,50 200,200 50,200" />
</svg>
```

### The `<polygon>` Element

The `<polygon>` element is similar to the `<polyline>` element. The difference is that the `<polygon>` element automatically adds a straight line from the last point to the first point.

```html
<svg width="500" height="500">
  <polygon points="50,50 200,50 200,200 50,200" />
</svg>
```

### The `<path>` Element

The `<path>` element is used to define a path. The `d` attribute defines the shape of the path. This is a more complex element that can create curves and arcs.

```html
<svg width="500" height="500">
  <path d="M50 50 Q100 150 200 50" />
</svg>
```

## SVG Text

The `<text>` element is used to create text.

```html
<svg width="500" height="500">
  <text x="50" y="50">Hello, SVG!</text>
</svg>
```

## SVG Styles and Colors

SVG uses similar styling to CSS. You can set `fill` and `stroke` properties to define the inside color and the border color of a shape.

```html
<svg width="500" height="500">
  <circle cx="250" cy="250" r="200" fill="blue" stroke="black" stroke-width="3" />
</svg>
```

