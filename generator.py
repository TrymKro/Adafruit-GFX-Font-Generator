import subprocess
import re

def generate_adafruit_font_file(symbols, font_name="MyFont", pt_size=24):
    bitmaps = []
    glyphs = []
    current_offset = 0
    
    # Filter out control characters (0-31) and get unique symbols
    symbol_list = [c for c in symbols if ord(c) >= 32]
    symbol_set = set(symbol_list)
    
    if not symbol_list:
        return "Error: No valid printable symbols provided."

    ascii_values = [ord(c) for c in symbol_list]
    first_ascii = min(ascii_values)
    last_ascii = max(ascii_values)

    print(f"Generating font: {first_ascii} to {last_ascii}...")

    for code in range(first_ascii, last_ascii + 1):
        char = chr(code)
        
        # Clean char for C++ comments and identify non-printables
        display_char = char.replace('\\', '\\\\').replace('\'', '\\\'')
        if code < 32 or code == 127: 
            display_char = "CONTROL"
        elif code > 127:
            # For extended ASCII, just show the symbol safely
            display_char = char

        # 1. HANDLE SPACE
        if char == " ":
            space_width = pt_size // 3
            glyphs.append(f"    {{ {current_offset}, 0, 0, {space_width}, 0, 0 }}, // ASCII {code:3} (0x{code:02X}) '{display_char}'")
            continue

        # 2. PROCESS ACTUAL SYMBOLS (Including ÆØÅ)
        if char in symbol_set:
            try:
                # Use Popen to feed UTF-8 character via stdin
                process = subprocess.Popen(
                    ["magick", "-font", "Liberation-Serif", "-pointsize", str(pt_size), "label:@-", "txt:-"],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                stdout, _ = process.communicate(input=char.encode('utf-8'))
                output = stdout.decode('utf-8').splitlines()
                
                header = output[0]
                w, h = map(int, re.search(r'(\d+),(\d+)', header).groups())

                pixel_bits = [0] * (w * h)
                for line in output[1:]:
                    if '#' in line:
                        parts = re.split(r'[,: ]+', line.strip())
                        x, y = int(parts[0]), int(parts[1])
                        if "white" not in line.lower() and "#FFFFFF" not in line.upper():
                            pixel_bits[y * w + x] = 1

                char_hex = []
                for i in range(0, len(pixel_bits), 8):
                    chunk = pixel_bits[i : i + 8]
                    val = 0
                    for bit in chunk:
                        val = (val << 1) | bit
                    if len(chunk) < 8: val <<= (8 - len(chunk))
                    char_hex.append(f"0x{val:02X}")

                glyphs.append(f"    {{ {current_offset}, {w}, {h}, {w+2}, 0, -{h} }}, // ASCII {code:3} (0x{code:02X}) '{display_char}'")
                bitmaps.extend(char_hex)
                current_offset += len(char_hex)
            except Exception as e:
                glyphs.append(f"    {{ {current_offset}, 0, 0, {pt_size//2}, 0, 0 }}, // ASCII {code:3} (0x{code:02X}) '{display_char}' (fail)")
        else:
            # 3. FILLER FOR MISSING CHARS IN RANGE
            glyphs.append(f"    {{ {current_offset}, 0, 0, {pt_size//2}, 0, 0 }}, // ASCII {code:3} (0x{code:02X}) '{display_char}' (filler)")

    # Build the .h file string
    return f"""#include <Adafruit_GFX.h>

const uint8_t {font_name}Bitmaps[] PROGMEM = {{
    {", ".join(bitmaps)}
}};

const GFXglyph {font_name}Glyphs[] PROGMEM = {{
{"\n".join(glyphs)}
}};

const GFXfont {font_name} PROGMEM = {{
    (uint8_t  *){font_name}Bitmaps,
    (GFXglyph *){font_name}Glyphs,
    0x{first_ascii:02X}, 0x{last_ascii:02X}, {pt_size + 4}
}};"""

# Execution
symbols = str(input("The symbols you want in your Adafruit-GFX-font:\n"))
output_file = "MyFont.h"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(generate_adafruit_font_file(symbols))

#print(f"Success! '{output_file}' generated.")
