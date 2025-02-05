# Steganography Tool - Hide Files in Images

A Flask-based web application that allows you to encode files into images (steganography) and decode them back. Supports various file types and customizable LSB (Least Significant Bit) embedding.


## Features

- **Encode Files**: Hide any file (PDF, TXT, PNG, etc.) within an image using LSB steganography.
- **Decode Files**: Extract hidden files from encoded images.
- **Customizable Bit**: Choose which LSB (0-7) to use for embedding data.
- **Web Interface**: User-friendly web UI for easy interaction.
- **File Type Detection**: Automatically detects the type of hidden file during decoding.
- **Error Handling**: Checks for image size limits, valid bit ranges, and corrupted data.

## Installation

1. **Clone the repository**:
   
         git clone https://github.com/yourusername/your-repo-name.git
         cd your-repo-name
   
3. **Install dependencies**:

         pip install -r requirements.txt

## Usage
   **Running the Application**:

      python app.py   
   Access the web interface at http://localhost:5000.
  
   **Encoding a File**:

   1. Go to the Encode page.

   2. Upload a cover image (PNG/JPG) and the file to hide.

   3. Select the target LSB (0 = least significant, 7 = most noticeable).

   4. Click "Encode" to download the modified image.

   **Decoding a File**:
   1. Go to the Decode page.

   2. Upload an encoded image.

   3. Click "Decode" to download the hidden file (automatically detects file type).


## Supported File Types

   - Images: PNG, JPG

   - Documents: PDF, DOC, TXT

   - Archives: ZIP
   
   - Executables: EXE
   
   - Audio: MP3
   
   - *More types can be added by extending the decode_file_from_image function.*

## Example
   **Encode a Secret Message:**
   
   1. Encode secret.txt into cat.png using LSB bit 0.
   
   2. Download encoded_image.png.
   
   **Decode the Message:**
   
   1. Upload encoded_image.png to the Decode page.
   
   2. The app extracts secret.txt automatically.

## Notes
- Higher LSB bits (e.g., bit 7) may cause visible artifacts in the image.

- The first pixel stores the target bit value (0-7) in its red channel.
