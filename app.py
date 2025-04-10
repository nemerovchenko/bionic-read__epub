import streamlit as st
import tempfile
import os
from pathlib import Path
from tqdm import tqdm

from bionic_converter import convert_epub_to_bionic

def main():
    st.set_page_config(
        page_title="Bionic Converter EPUB",
        page_icon="📚",
        layout="centered",
        initial_sidebar_state="auto",
    )
    
    # Add custom CSS styles for the dark theme
    st.markdown("""
    <style>
    /* Improve contrast in a dark theme */
    @media (prefers-color-scheme: dark) {
        .stApp {
            background-color: #121212;
        }
        
        .css-1avcm0n, .css-145kmo2 {
            border-color: #333 !important;
        }
        
        .stButton button {
            background-color: #90caf9 !important;
            color: #121212 !important;
        }
        
        .stDownloadButton button {
            background-color: #90caf9 !important;
            color: #121212 !important;
        }
        
        h1, h2, h3, p, .stMarkdown {
            color: #f0f0f0 !important;
        }
    }
    
    /* Enhancing styles for bionic text */
    .bionic-example {
        font-size: 1.2rem;
        line-height: 1.6;
        margin: 20px 0;
        padding: 15px;
        border-radius: 5px;
        background-color: rgba(144, 202, 249, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Заголовок и описание
    st.title("EPUB to Bionic Converter")
    st.markdown("""
    Convert your EPUB books to bionic format to speed up reading and improve reading comprehension.
    
    An example of a bionic text:
    """)
    
    # Showing an example of bionic text
    st.markdown('<div class="bionic-example"><p>Эт<b>о</b> пр<b>име</b>р би<b>онич</b>еского те<b>кст</b>а, гд<b>е</b> пе<b>рва</b>я по<b>лови</b>на ка<b>ждо</b>го сл<b>ов</b>а вы<b>деле</b>на жи<b>рны</b>м шр<b>ифт</b>ом.</p></div>', unsafe_allow_html=True)
    
    # File upload
    uploaded_file = st.file_uploader("Download EPUB file", type=["epub"], accept_multiple_files=False)
    
    # Option for dark theme
    dark_theme = st.checkbox("Add support for dark theme", value=True, help="Adds CSS styles for better contrast in dark mode")
    
    if uploaded_file is not None:
        # Save the file to a temporary directory
        with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_file_path = tmp_file.name
        
        # Save the original file name
        original_filename = uploaded_file.name
        
        # Button to start conversion
        if st.button("Convert to bionic format"):
            with st.spinner("File processing..."):
                # Create a temporary file for the output file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as output_tmp:
                    output_path = output_tmp.name
                
                # Add a progress bar
                progress_bar = st.progress(0)
                
                # Function to update progress (used as a colback)
                def update_progress(current, total):
                    if total > 0:
                        progress_bar.progress(current / total)
                
                try:
                    # Start the conversion
                    convert_epub_to_bionic(tmp_file_path, output_path, add_dark_theme=dark_theme)
                    
                    # Read the converted file
                    with open(output_path, "rb") as file:
                        converted_data = file.read()
                    
                    # Create a name for the output file
                    name, ext = os.path.splitext(original_filename)
                    output_filename = f"Bionic_{name}{ext}"
                    
                    # Display a success message
                    st.success("Conversion successfully completed!")
                    
                    # Add a download button
                    st.download_button(
                        label="Download the converted book",
                        data=converted_data,
                        file_name=output_filename,
                        mime="application/epub+zip"
                    )
                except Exception as e:
                    st.error(f"Conversion error: {str(e)}")
                finally:
                    # Deleting temporary files
                    try:
                        os.unlink(tmp_file_path)
                        os.unlink(output_path)
                    except:
                        pass
    
    # Add project information to the sidebar
    st.sidebar.title("About the project")
    st.sidebar.markdown("""
    **Bionic Converter EPUB** - a tool for converting e-books into a format that enhances text comprehension.
    
    ### How it works
    
    Bionic Reading highlights the first half of each word in bold, which helps:
    - Increase reading speed
    - Improve focus of attention
    - Reduce eye fatigue
    - Increase memorisation of information
    
    ### Features
    - Maintains the structure of the book
    - Supports Cyrillic alphabet
    - Adds support for dark theme
    
    ### Source code
    [GitHub](https://github.com/nemerovchenko/bionic-read__epub)
    """)

if __name__ == "__main__":
    main() 