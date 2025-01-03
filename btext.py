import os
import streamlit as st
import PyPDF2
from groq import Groq

# Streamlit Page Configurations
st.set_page_config(
    layout="wide",
    page_title="AI Business model Analyzer",
    initial_sidebar_state="expanded"
)

# Sidebar Configuration
st.sidebar.image("p2.PNG", width=200)
st.sidebar.image("p1.png", width=300)
st.sidebar.title("Configuration Options")
st.sidebar.subheader("1. Select AI Model")

SUPPORTED_MODELS = {
    "Llama 3 8B": "llama3-8b-8192",
    "Llama 3.2 1B (Preview)": "llama-3.2-1b-preview",
    "Llama 3 70B": "llama3-70b-8192",
    "Mixtral 8x7B": "mixtral-8x7b-32768",
    "Gemma 2 9B": "gemma2-9b-it",
    "Llama 3.2 11B Vision (Preview)": "llama-3.2-11b-vision-preview",
    "Llama 3.2 11B Text (Preview)": "llama-3.2-11b-text-preview",
    "Llama 3.1 8B Instant (Text-Only Workloads)": "llama-3.1-8b-instant",
    "Llama 3.2 90B Vision (Preview)": "llama-3.2-90b-vision-preview",
    "Llama 3.1 70B Versatile": "llama-3.1-70b-versatile",
    "Llama 3.3 70B SpecDec": "llama-3.3-70b-specdec",
    "Llama 3.3 70B Versatile": "llama-3.3-70b-versatile",
}

selected_model = st.sidebar.selectbox("Choose an AI Model", list(SUPPORTED_MODELS.keys()))

st.sidebar.subheader("2. Select Business Role")
BUSINESS_ROLES = [
    "Blue Ocean Strategy",
    "SWOT Analysis",
    "BCG Matrix",
    "Porter’s Five Forces",
    "Value Chain Analysis",
    "OKR Methodology",
    "RACI Matrix",
    "VRIO Framework",
    "McKinsey 7S Framework",
    "Balanced Scorecard",
    "Customer Journey Mapping",
    "Ansoff Matrix",
    "Lean Startup Methodology"
]

selected_role = st.sidebar.radio("Choose a Business Role", BUSINESS_ROLES)

st.sidebar.subheader("3. Adjust Temperature")
temperature = st.sidebar.slider("Set Temperature", min_value=0.0, max_value=1.0, value=0.7)

st.sidebar.subheader("4. Upload PDF Document")
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

st.sidebar.subheader("5. Customize Role Instructions")
role_instructions = st.sidebar.text_area(f"Edit Instructions for {selected_role}", value="", height=300)

# Main Section
st.title("AI Business Analyzer")
st.write("Analyze your PDF document using advanced AI prompts. Results will be displayed below.")

# Function to Extract Text from PDF
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

if uploaded_file:
    with st.expander("Extracted PDF Text"):
        pdf_text = extract_text_from_pdf(uploaded_file)
        st.text_area("Preview of Extracted Text", pdf_text, height=500)

    if st.button("Analyze Document"):
        st.write("Analyzing the document...")
        if not pdf_text.strip():
            st.warning("No text extracted from the PDF. Please check the document.")
        else:
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                st.error("GROQ_API_KEY is not set. Please configure your environment variables.")
            else:
                client = Groq(api_key=groq_api_key)

                try:
                    response = client.chat.completions.create(
                        model=SUPPORTED_MODELS[selected_model],
                        messages=[
                            {"role": "system", "content": role_instructions},
                            {"role": "user", "content": pdf_text},
                        ],
                        temperature=temperature,
                        max_tokens=1500,
                    )
                    analysis_result = response.choices[0].message.content.strip()
                    
                    # Display the result
                    st.subheader("Analysis Result")
                    st.write(analysis_result)

                except Exception as e:
                    st.error(f"Error during analysis: {e}")

else:
    st.info("Please upload a PDF document to start the analysis.")
