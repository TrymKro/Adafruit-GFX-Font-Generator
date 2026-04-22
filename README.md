# Adafruit GFX Font Generator

A Python-based utility to convert system fonts into Adafruit GFX compatible bitmaps, specifically optimized for E-Paper Displays (EPD) and European characters (ÆØÅ).

## Requirements
- Python 3.14
- [ImageMagick v7+](https://imagemagick.org)

## Usage
1. Run the generator:
   ```bash
   python generator.py --size 32 --name MyCustomFont --out MyFont.h
   ```
2. Copy `MyFont.h` to your Arduino project.
3. Use the `fixEncoding()` function in your sketch to handle UTF-8 characters.

## Features
- Full ASCII range support (32-255).
- Auto-filler for missing characters to maintain ASCII mapping.
- Detailed comments in the header file with ASCII codes.
