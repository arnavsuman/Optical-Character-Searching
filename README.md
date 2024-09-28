# OCR Image Upload and Document Search App

This is a Streamlit-based web application that allows users to upload an image, extract text from the image using Optical Character Recognition (OCR), and then search for a specific pattern given by user to search within the extracted text. The app leverages the `easyocr` library for OCR and implements the Knuth-Morris-Pratt (KMP) algorithm for efficient string searching.

## Features
- **Upload Images:** Upload images in `.jpg`, `.jpeg`, or `.png` formats.
- **Text Extraction:** Extract text from the uploaded image using OCR (supports both English and Hindi).
- **String Patterm:** Search for a specific string in the extracted text using the KMP search algorithm.
- **Real-Time Feedback:** The app provides feedback on whether the search string was found and its position(s) in the text.

## Technologies Used
- **Streamlit:** For building the interactive user interface.
- **PIL (Pillow):** For handling and processing images.
- **easyocr:** To perform Optical Character Recognition (OCR) on the uploaded image.
- **NumPy:** For array operations and converting images.
- **KMP Algorithm:** To search for patterns efficiently in the extracted text.

## How to Run the App

### Prerequisites
1. **Python 3.x** installed on your machine.
2. Install the required Python packages by running the following command:
   ```bash
   pip3 install streamlit easyocr Pillow numpy
