import base64
from PIL import Image
import io

def convert_image_to_base64(image_path):
    # Open the image file
    with Image.open(image_path) as image:
        # Convert the image to RGB format to ensure compatibility
        rgb_image = image.convert('RGB')
        # Create a bytes buffer for the image
        buffered = io.BytesIO()
        # Save the image to the buffer in JPEG format
        rgb_image.save(buffered, format="JPEG")
        # Convert the buffer content into bytes
        img_byte = buffered.getvalue()
        # Encode the bytes to base64
        img_base64 = base64.b64encode(img_byte)
        # Convert bytes to string
        img_base64_str = img_base64.decode('utf-8')
        return img_base64_str

# Replace 'path/to/your/image.png' with the actual path to your PNG image
image_path = r"C:\Users\ethan\Desktop\work\What_and_where\feed_images\dogs.jpg"
base64_string = convert_image_to_base64(image_path)

# Specify the output text file path``
output_file_path = 'output_base64.txt'

# Write the base64 string to a text file
with open(output_file_path, 'w') as file:
    file.write(base64_string)

print(f"Base64 encoded string has been written to {output_file_path}")
