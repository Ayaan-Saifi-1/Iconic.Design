from PIL import Image, ImageDraw
import numpy as np

def apply_balanced_gold_gradient(image_path, output_path):
    img = Image.open(image_path).convert("RGBA")
    
    # Create a gradient image of the same size
    width, height = img.size
    gradient = Image.new('RGBA', (width, height), color=0)
    draw = ImageDraw.Draw(gradient)
    
    # Balanced gold with a soft shine in the middle, not overly bright
    colors = [
        (184, 134, 11),   # #B8860B - Matte Gold (edges)
        (230, 195, 95),   # Soft, elegant metallic shine in the middle
        (184, 134, 11)    # #B8860B - Matte Gold (edges)
    ]
    
    # Draw a diagonal gradient
    for y in range(height):
        for x in range(width):
            # Calculate position in gradient (0 to 1)
            pos = (x / width + y / height) / 2
            
            # Find the two colors to interpolate between
            color_idx = pos * (len(colors) - 1)
            idx1 = int(color_idx)
            idx2 = min(idx1 + 1, len(colors) - 1)
            
            # Interpolation factor
            f = color_idx - idx1
            
            # Interpolate
            r = int(colors[idx1][0] * (1 - f) + colors[idx2][0] * f)
            g = int(colors[idx1][1] * (1 - f) + colors[idx2][1] * f)
            b = int(colors[idx1][2] * (1 - f) + colors[idx2][2] * f)
            
            draw.point((x, y), fill=(r, g, b, 255))
            
    # Apply the gradient to the original image's alpha mask
    img_data = np.array(img)
    grad_data = np.array(gradient)
    
    # Use the original alpha channel
    alpha = img_data[:, :, 3]
    
    # Replace the RGB channels with the gradient where alpha > 0
    result_data = np.zeros_like(img_data)
    result_data[:, :, 0] = grad_data[:, :, 0]
    result_data[:, :, 1] = grad_data[:, :, 1]
    result_data[:, :, 2] = grad_data[:, :, 2]
    result_data[:, :, 3] = alpha
    
    result = Image.fromarray(result_data)
    result.save(output_path)

apply_balanced_gold_gradient('static/logo_transparent.png', 'static/logo_transparent.png')
apply_balanced_gold_gradient('static/favicon.png', 'static/favicon.png')
print("Applied balanced gold gradient successfully.")
