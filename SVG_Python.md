# Beginners Guide: Using Python F-string to Generate SVG Images

This guide will demonstrate how to dynamically generate SVG images using Python's f-strings. 

First, let's understand what an f-string is in Python.

## F-Strings

F-strings, introduced in Python 3.6 as Literal String Interpolation, are a new way of formatting strings in Python. They are prefixed with an `f` character and use curly braces `{}` as placeholders for variables.

```python
name = "Alice"
print(f"Hello, {name}")
```
This will output: `Hello, Alice`

Now, let's explore how we can use f-strings to generate SVG images dynamically.

## SVG (Scalable Vector Graphics)

SVG is an XML-based vector graphic format, used to display a variety of graphics on the Web and other environments. Since SVG are defined in XML, every SVG element is appended to the DOM which can be manipulated using a combination of JavaScript and CSS.

Here is a basic example of an SVG image:

```xml
<svg width="100" height="100">
  <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
</svg>
```

This will generate a circle of radius 40, centered at (50,50).

## Using Python F-Strings with SVG

We can dynamically generate SVG using Python f-strings. The variables inside the `{}` will be replaced with their values.

Here are some use cases:

### Example 1: Updating Text in SVG

This example shows how to change the text in an SVG using Python f-strings. In the example, we create an SVG of a circle, with a text in the middle that can be changed dynamically.

```python
coin_text = "Heads"
svg_image = f'''
    <svg width="200" height="200" viewBox="0 0 200 200">
        <a href="/toggle">
            <circle style="fill:#F0E68C" cx="100" cy="100" r="90"/>
            <text x="50%" y="50%" font-size="24" text-anchor="middle" dy=".3em">{coin_text}</text>
        </a>
    </svg>
'''

print(svg_image)
```

The `{coin_text}` in the f-string will be replaced with the value of the `coin_text` variable.

### Example 2: Generating SVG for Dice Faces

This example demonstrates generating SVGs for dice faces. We first define the SVGs for the faces of a dice, then dynamically select which face to display based on the value of `dice_faces`.

```python
dice_faces_svg = {
        1: '''
            <circle cx="100" cy="100" r="10" fill="black" />
        ''',
        2: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        ''',
        3: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="100" cy="100" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        ''',
        4: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="150" cy="50" r="10" fill="black" />
            <circle cx="50" cy="150" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        ''',
        5: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="150" cy="50" r="10" fill="black" />
            <circle cx="100" cy="100" r="10" fill="black" />
            <circle cx="50" cy="150" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        ''',
        6: '''
            <circle cx="50" cy="50" r="10" fill="black" />
            <circle cx="150" cy="50" r="10" fill="black" />
            <circle cx="50" cy="100" r="10" fill="black" />
            <circle cx="150" cy="100" r="10" fill="black" />
            <circle cx="50" cy="150" r="10" fill="black" />
            <circle cx="150" cy="150" r="10" fill="black" />
        '''
    }


dice_faces = [1, 2, 3, 4, 5, 6] # replace with actual dice faces
dice_svgs = ''
for i in range(len(dice_faces)):
    x_offset = 220 * i
    dice_svgs += f'''
        <svg x="{x_offset}" width="200" height="200" viewBox="0 0 200 200">
            <rect x="10" y="10" width="180" height="180" rx="20" ry="20" fill="#{background_colors[i]}" />
            {dice

_faces_svg[dice_faces[i]]}
        </svg>
    '''

print(dice_svgs)
```

In this example, the `{x_offset}` in the SVG is replaced with the value of `x_offset`, and `{dice_faces_svg[dice_faces[i]]}` is replaced with the SVG string corresponding to the face of the dice.

### Example 3: Changing SVG Fill Color

This example shows how to change the fill color of SVG elements. We use a list of colors and toggle the fill color of the circles in the SVG.

```python
reds     = ["853737","ff6465"]
yellows  = ["907A4A","ffd782"]
greens   = ["4E7039","a5eb78"]

lights = [0, 1, 0]  # replace with actual values

red     = reds[lights[0]]
yellow  = yellows[lights[1]]
green   = greens[lights[2]]

svg_image = f'''
    <svg width="100" height="100" viewBox="0 0 512 512">
      <path style="fill:#515262" d="M324.683 41.53H187.317c-28.304 0-51.249 22.946-51.249 51.249V460.75c0 28.305 22.946 51.249 51.249 51.249h137.366c28.304 0 51.249-22.946 51.249-51.249V92.779c0-28.303-22.945-51.249-51.249-51.249z"/>
      <a href="/toggle/0">
          <circle style="fill:#{red}" cx="255.995" cy="133.818" r="48.281"/>
      </a>
      <a href="/toggle/1">
          <circle style="fill:#{yellow}" cx="255.995" cy="276.765" r="48.281"/>
      </a>
      <a href="/toggle/2">
          <circle style="fill:#{green}" cx="255.995" cy="419.712" r="48.281"/>
      </a>
    </svg>
'''

print(svg_image)
```

Here, the `{red}`, `{yellow}`, and `{green}` in the SVG are replaced with their corresponding color codes.
