from PIL import Image
import numpy as np

# Load image
img = Image.open('static/new_logo.png').convert('RGBA')
data = np.array(img)

# The background is off-white (around 235-245).
# Let's say anything where R > 180, G > 180, B > 180 and max-min < 30 is background
r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
max_c = np.maximum(np.maximum(r, g), b)
min_c = np.minimum(np.minimum(r, g), b)

# Create a mask for background
bg_mask = (r > 150) & (g > 150) & (b > 150) & ((max_c - min_c) < 40)

# Also pure white or close to it
bg_mask_2 = (r > 200) & (g > 200) & (b > 200)

mask = bg_mask | bg_mask_2

# Make background transparent
data[mask, 3] = 0

# For anti-aliasing / soft edges, we could do a distance-based alpha, but hard threshold might be okay for now.
# Let's add a bit of softness:
# If a pixel is somewhat close to background, reduce its alpha
diff = np.abs(r.astype(int) - g.astype(int)) + np.abs(r.astype(int) - b.astype(int))
# Gold usually has higher R and G, lower B. So r-b will be large.
# If r-b is small, it's grayish.
grayish = diff < 30
light = r > 100
data[grayish & light, 3] = 0

new_img = Image.fromarray(data)
new_img.save('static/logo_transparent.png')

# Also create favicon
# Find bounding box of non-transparent pixels
alpha = data[:,:,3]
coords = np.argwhere(alpha > 0)
y0, x0 = coords.min(axis=0)
y1, x1 = coords.max(axis=0) + 1
cropped = new_img.crop((x0, y0, x1, y1))

# resize to 32x32 for favicon
favicon = cropped.resize((32, 32), Image.Resampling.LANCZOS)
favicon.save('static/favicon.png')
print("Done")
