import streamlit as st
import pytesseract
import pyttsx3
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

from PIL import Image
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag

# Set up NLTK
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Function to extract text from image using OCR
def extract_text_from_image(image):
    img = Image.open(image)
    text = pytesseract.image_to_string(img)
    return text

# Function to apply color to parts of speech
def apply_pos_color(text):
    tagged_words = pos_tag(word_tokenize(text))
    colored_text = []
    for word, tag in tagged_words:
        colored_text.append(f'<span style="color:{"red" if tag.startswith("NN") else "blue" if tag.startswith("VB") else "black"}">{word}</span>')
    colored_text = ' '.join(colored_text)
    return colored_text

# Function to convert text to speech
def convert_to_speech(text):
    engine = pyttsx3.init()  # Initialize pyttsx3 engine
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # Stop the engine after speech conversion

# Streamlit app
def main():
    # List of background colors
    background_colors = {
        "Light Blue": "#F0F8FF",
        "Light Green": "#90EE90",
        "Light Pink": "#FFB6C1",
        "Light Yellow": "#FFFFE0",
    }

    # Select background color
    background_color = st.sidebar.selectbox("Select Background Color", list(background_colors.keys()))

    # Add custom CSS styles
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {background_colors[background_color]};
        }}
        .st-ba {{
            background-color: #ADD8E6;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
        }}
        .st-fy {{
            font-weight: bold;
            color: #FFFFFF;
            text-align: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Set background color for the app
    st.markdown('<div class="stApp">', unsafe_allow_html=True)

    st.title("Comic Storyteller :)")
    st.subheader("Upload an image")

    # Image upload
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        # Display uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Extract text from image
        extracted_text = extract_text_from_image(uploaded_image)

        # Apply color to parts of speech
        colored_text = apply_pos_color(extracted_text)

        # Display extracted text with colored parts of speech
        st.markdown(f'<div class="st-ba"><div class="st-fy">{colored_text}</div></div>', unsafe_allow_html=True)

        # Button to convert text to speech
        if st.button("Convert to Speech"):
            convert_to_speech(extracted_text)

    # Close the background color div
    st.markdown('</div>', unsafe_allow_html=True)

    # Display bubbles
    st.balloons()


if __name__ == '__main__':
    main()
