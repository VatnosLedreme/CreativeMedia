import io
import base64
from PIL import Image, ImageDraw

def create_original_icon():
    print("Drawing original icon...")
    
    # 1. Create a 256x256 transparent canvas
    size = 256
    img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # 2. Draw the background: A sleek dark circular badge
    # Bounding box leaves a small margin for aesthetics
    draw.ellipse([(16, 16), (240, 240)], fill="#2b2d30")

    # 3. Draw the foreground: A vibrant "Launch/Play" triangle
    # Coordinates for a perfectly centered right-pointing triangle
    triangle_points = [(100, 80), (100, 176), (175, 128)]
    draw.polygon(triangle_points, fill="#40d97b")

    # 4. Save as a fully formatted, multi-resolution Windows .ico file
    icon_filename = "app_icon.ico"
    img.save(
        icon_filename, 
        format="ICO", 
        sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]
    )
    print(f"✅ Success! '{icon_filename}' created in your folder.")

    # 5. Generate the proper Base64 string for Tkinter
    # We resize it to 32x32 for the Tkinter window title bar
    buffer = io.BytesIO()
    img_small = img.resize((32, 32), Image.Resampling.LANCZOS)
    img_small.save(buffer, format="PNG")
    
    b64_string = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    print("\n" + "="*50)
    print("Replace the ICON_BASE64 variable in your main Tkinter script with this:\n")
    print(f'ICON_BASE64 = """\n{b64_string}\n"""')
    print("="*50 + "\n")

if __name__ == "__main__":
    create_original_icon()