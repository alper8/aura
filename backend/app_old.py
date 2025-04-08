import streamlit as st
import os
from AddDesc import main, print_header
import tempfile
import time

# Set page config
st.set_page_config(
    page_title="AURA - Automated Universal Row Augmenter",
    page_icon="✨",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
        .header {
            color: #2ecc71;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .subheader {
            color: #3498db;
            font-size: 18px;
            margin-bottom: 10px;
        }
        .success {
            color: #2ecc71;
            font-weight: bold;
        }
        .progress-container {
            margin-top: 20px;
            margin-bottom: 20px;
        }
        .file-input {
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Display header
st.markdown("""
    <div class="header">
        Welcome to AURA - Automated Universal Row Augmenter
    </div>
    <div class="subheader">
        v1.0a - Created by Alper Baykara
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    **Pre-Configured for adding Turkish descriptions for database attributes**
    
    Example:
    ```
    Customer ID
    Customer Name
    
    ↓
    
    Customer ID: Müşteri Tekil Anahtarı
    Customer Name: Müşteri Adı
    ```
""")

# Sidebar for advanced options
with st.sidebar:
    st.header("Advanced Options")
    debug_mode = st.checkbox("Enable Debug Mode", False)
    
    if debug_mode:
        model = st.text_input("Model", "gpt-4o-mini")
        prompt = st.text_area("Prompt", """Sen bir veri modelleme uzmanısın, ingilizce gördüğün attribute alanlarının karşısına türkçe bir açıklama yaz. sadece 2-3 kelimelik bir cümle olarak. ID kelimesini veya ingilizce kelimeler kullanma. PK veya FK lar için Tekil anahtarı veya Dış Anahtarı tabirini kullan örnek: Customer ID -> Müşteri Tekil Anahtarı. Bayrak yerine bilgisi de, örnek: KVKK Flag -> KVKK bilgisi.  Accepted Commission Amount: Kabul Edilen Komisyon Tutarı""")
        chunk_size = st.number_input("Chunk Size", min_value=1, max_value=500, value=100)
    else:
        model = "gpt-4o-mini"
        prompt = """Sen bir veri modelleme uzmanısın, ingilizce gördüğün attribute alanlarının karşısına türkçe bir açıklama yaz. sadece 2-3 kelimelik bir cümle olarak. ID kelimesini veya ingilizce kelimeler kullanma. PK veya FK lar için Tekil anahtarı veya Dış Anahtarı tabirini kullan örnek: Customer ID -> Müşteri Tekil Anahtarı. Bayrak yerine bilgisi de, örnek: KVKK Flag -> KVKK bilgisi.  Accepted Commission Amount: Kabul Edilen Komisyon Tutarı"""
        chunk_size = 100

# File upload section
st.markdown('<div class="file-input">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload your input file with attributes", type=["txt"])
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    # Create temporary files
    with tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8", suffix=".txt") as input_temp:
        input_temp.write(uploaded_file.read().decode("utf-8"))
        input_file_path = input_temp.name
    
    with tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8", suffix=".txt") as output_temp:
        output_file_path = output_temp.name
    
    if st.button("Generate Descriptions"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Run the main function
            status_text.text("Processing...")
            
            # We'll simulate progress since the actual progress happens in the backend
            for i in range(100):
                time.sleep(0.02)  # Simulate processing time
                progress_bar.progress(i + 1)
            
            # Call the main function
            main(input_file_path, output_file_path, model, prompt, chunk_size)
            
            # Read the output file
            with open(output_file_path, "r", encoding="utf-8") as f:
                results = f.read()
            
            # Display results
            st.markdown('<div class="success">Descriptions generated successfully!</div>', unsafe_allow_html=True)
            st.text_area("Generated Descriptions", results, height=300)
            
            # Download button
            st.download_button(
                label="Download Results",
                data=results,
                file_name="attribute_descriptions.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            # Clean up temporary files
            try:
                os.unlink(input_file_path)
                os.unlink(output_file_path)
            except:
                pass