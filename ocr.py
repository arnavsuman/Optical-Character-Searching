import streamlit as st
from PIL import Image
import easyocr
import numpy as np

# Function to perform OCR on the uploaded image
def perform_ocr(image):
    image_np = np.array(image)  # Convert PIL image to NumPy array
    reader = easyocr.Reader(['hi', 'en'])
    result = reader.readtext(image_np)
    string = ' '.join([text[1] for text in result])
    return string

# KMP search with text highlighting
def KMP_search_and_highlight(extracted_text, search_string):
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0  # length of the previous longest prefix suffix
        i = 1

        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    # Convert both strings to lowercase for case-insensitive search
    extracted_text_lower = extracted_text.lower()
    search_string_lower = search_string.lower()

    n = len(extracted_text_lower)
    m = len(search_string_lower)
    
    lps = compute_lps(search_string_lower)
    i = 0  # index for text
    j = 0  # index for pattern
    indices = []  # to store the starting indices of found patterns

    while i < n:
        if search_string_lower[j] == extracted_text_lower[i]:
            i += 1
            j += 1

        if j == m:
            indices.append(i - j)
            j = lps[j - 1]
        elif i < n and search_string_lower[j] != extracted_text_lower[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    # Highlight the search string in the extracted text
    highlighted_text = extracted_text
    if indices:
        offset = 0  # Keep track of added tags so we adjust the positions accordingly
        for index in indices:
            start = index + offset
            end = start + len(search_string)
            highlighted_text = highlighted_text[:start] + f'<mark>{highlighted_text[start:end]}</mark>' + highlighted_text[end:]
            offset += len('<mark></mark>')  # Account for added tags

        return highlighted_text, True  # Return highlighted text and success
    else:
        return "Pattern not found.", False  # Return failure message and status

# Streamlit UI
st.title("OCR Image Upload and Document Search App")
st.write("Upload an image to extract text using OCR, then search for any string in the extracted text.")
st.write("Made by Arnav Suman for IIT-Roorkee")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Initialize session state for extracted text if not already done
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Image Uploaded by you.', use_column_width=True)
    st.write("")
    
    if st.button("Scan Image"):
        with st.spinner("Extracting text..."):
            extracted_text = perform_ocr(image)

            st.success("Text extracted successfully!")
            st.text_area("Extracted Text", extracted_text, height=300, disabled=True, key="extracted_text_area")

            # Store extracted text in session state
            st.session_state.extracted_text = extracted_text

    # Show search input and button only after OCR is done
    if st.session_state.extracted_text:
        search_string = st.text_input("Enter string to search:")
        if st.button("Search"):
            highlighted_text, found = KMP_search_and_highlight(st.session_state.extracted_text, search_string)

            if found:
                st.success(f"Pattern '{search_string}' found!")  # Display success message
                st.markdown(f"<p>{highlighted_text}</p>", unsafe_allow_html=True)  # Display highlighted text
            else:
                st.error(highlighted_text)

# To run the app, use the command: python3 -m streamlit run ocr.py
