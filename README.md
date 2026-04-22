# Adafruit GFX Font Generator (EPD Edition)

A Python-based utility to convert system fonts into Adafruit_GFX compatible bitmap headers. This tool is designed for E-Paper Displays (EPD) and solves common issues with UTF-8 encoding, missing character gaps, and bit-order alignment.

## Key Features

- **All Mode**: Type "All" at the prompt to generate a complete font covering the full range of ASCII 32 to 255.
- **Automatic Filler Logic**: Ensures the generated font has no index gaps, meaning Arduino `display.print()` calls will always index the correct glyph.
- **Readable Header Files**: Includes detailed comments for every character, showing both Decimal and Hexadecimal ASCII codes for easy debugging.
- **EPD Optimization**: Designed to be used with `GFXcanvas1` for rendering on e-paper.

## Prerequisites

1. **ImageMagick v7+**: The script uses the `magick` command.
2. **Python 3.x**: Ensure Python is installed and added to your system PATH.

## How to Use

1. **Run the script**:
   ```bash
   python generator.py --size 32 --name MyCustomFont --out MyFont.h
   ```
      --size 32: Sets the font height (px). Instead of the default 24pt, it tells ImageMagick to render the characters at 32 pixels tall.
      --name MyCustomFont: Sets the name of the font structure inside the .h file. In Arduino, you would refer to this as canvas.setFont(&MyCustomFont).
      --out MyFont.h: Specifies the name of the file to be created. It saves the resulting code into MyFont.h in your current folder.
2. **Choose your characters**:
   - Enter specific characters: `ABCabc123æøå`
   - OR type `All` to generate the entire standard and extended ASCII set (32-255).
3. **Integration**:
   - Move the generated `MyFont.h` into your Arduino project folder.
   - Include it in your sketch: `#include "MyFont.h"`
   - Set the font: `canvas.setFont(&MyCustomFont);`

## Handling Extended ASCII Characters (Arduino)

Arduino encodes strings in UTF-8 (2 bytes), while this font uses Extended ASCII (1 byte). Use this helper function in your sketch to map them correctly:

```cpp
String fixEncoding(String text) {
  text.replace("Æ", String((char)198)); text.replace("æ", String((char)230));
  text.replace("Ø", String((char)216)); text.replace("ø", String((char)248));
  text.replace("Å", String((char)197)); text.replace("å", String((char)229));
  text.replace("°", String((char)176));
  return text;
}

// Usage:
canvas.print(fixEncoding("Bilær og båtær som tutær og bråkær"));
```

## Troubleshooting

- **Gibberish on Screen**: Ensure your `GFXcanvas1` dimensions match your EPD driver exactly. Some displays also require a Bit-Reversal loop (MSB to LSB) before calling `EPD_WhiteScreen_ALL`.
- **Command Not Found**: If you get an error about `magick`, ensure ImageMagick is installed and that you can run `magick -version` in your terminal.

## License

This project is open-source. Feel free to use it for your own projects.
