from PIL import Image

def process_logo(input_path, output_path):
    try:
        img = Image.open(input_path)
        img = img.convert("RGBA")
        datas = img.getdata()
        
        newData = []
        for item in datas:
            # Change all white (also shades of whites)
            # to transparent
            if item[0] > 200 and item[1] > 200 and item[2] > 200:
                # To prevent harsh edges, we could use alpha based on darkness, but simple threshold is okay
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
                
        img.putdata(newData)
        
        # Crop the image to exactly the logo bounds
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)
            
        img.save(output_path, "PNG")
        print("Success")
    except Exception as e:
        print(f"Error: {e}")

process_logo(r"c:\Users\Ayaan\Desktop\Iconic Kitchen\static\favicon.png", r"c:\Users\Ayaan\Desktop\Iconic Kitchen\static\logo_transparent.png")
