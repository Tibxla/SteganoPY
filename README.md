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

  python app.py\n
  Access the web interface at http://localhost:5000.
