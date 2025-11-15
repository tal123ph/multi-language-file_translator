import streamlit as st
import asyncio
from io import BytesIO
from lingodotdev.engine import LingoDotDevEngine

# -----------------------------
# ERROR HANDLING FOR IMPORTS
# -----------------------------
# FPDF (PDF output)
try:
    from fpdf import FPDF
except ImportError:
    st.error("❌ Missing library: fpdf. Install it using `pip install fpdf`")
    st.stop()

# PyPDF2 (PDF input)
try:
    import PyPDF2
except ImportError:
    st.error("❌ Missing library: PyPDF2. Install it using `pip install PyPDF2`")
    st.stop()

# -----------------------------
# STREAMLIT PAGE SETTINGS
# -----------------------------
st.set_page_config(page_title="Universal File Translator", layout="wide")
st.title("🌍 Universal File Translator (Lingo.dev + Streamlit)")
st.write("Upload `.srt`, `.txt`, or `.pdf` file and download translations in desired format.")

# -----------------------------
# INPUTS
# -----------------------------
try:
    api_key = st.secrets["api_key_val"]
except KeyError:
    st.error("❌ API key not found. Add it in .streamlit/secrets.toml as `api_key_val`")
    st.stop()

uploaded_file = st.file_uploader(
    "📤 Upload File (.srt, .txt, .pdf)",
    type=["srt", "txt", "pdf"]
)

target_language = st.selectbox(
    "🌐 Select Target Language",
    ["ur", "ar", "tr", "fr", "hi", "de", "zh", "es"]
)

output_format = st.selectbox(
    "💾 Select Output Format",
    ["PDF", "TXT", "SRT"]
)

translate_btn = st.button("🚀 Translate File")

# -----------------------------
# HELPER: Read file content
# -----------------------------
def read_file_content(uploaded_file):
    file_type = uploaded_file.name.split(".")[-1].lower()
    try:
        if file_type in ["txt", "srt"]:
            return uploaded_file.read().decode("utf-8"), file_type
        elif file_type == "pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text, "pdf"
        else:
            return None, None
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        return None, None

# -----------------------------
# ASYNC TRANSLATION FUNCTION
# -----------------------------
async def translate_text(text, api_key, target_language):
    try:
        translated = await LingoDotDevEngine.quick_translate(
            text,
            api_key=api_key,
            source_locale="en",
            target_locale=target_language,
            fast=True
        )
        return translated
    except Exception as e:
        st.error(f"❌ Translation error: {e}")
        return None

# -----------------------------
# SAFE ASYNC RUNNER FOR STREAMLIT
# -----------------------------
def run_async(coro):
    try:
        return asyncio.run(coro)
    except RuntimeError:
        return asyncio.get_event_loop().run_until_complete(coro)

# -----------------------------
# PROCESS THE TRANSLATION
# -----------------------------
if translate_btn:
    if not uploaded_file:
        st.error("❌ Please upload a file.")
    else:
        content, file_type = read_file_content(uploaded_file)
        if not content:
            st.stop()
        st.info("⏳ Translating... please wait.")
        translated_text = run_async(
            translate_text(content, api_key, target_language)
        )
        if not translated_text:
            st.stop()

        # -----------------------------
        # CREATE OUTPUT FILE
        # -----------------------------
        try:
            if output_format == "PDF":
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 8, translated_text)
                buffer = BytesIO()
                pdf.output(buffer)
                buffer.seek(0)
                st.download_button(
                    label="📥 Download PDF",
                    data=buffer,
                    file_name=f"translated.{target_language}.pdf",
                    mime="application/pdf"
                )
            elif output_format == "TXT":
                buffer = BytesIO()
                buffer.write(translated_text.encode("utf-8"))
                buffer.seek(0)
                st.download_button(
                    label="📥 Download TXT",
                    data=buffer,
                    file_name=f"translated.{target_language}.txt",
                    mime="text/plain"
                )
            elif output_format == "SRT":
                if file_type != "srt":
                    st.warning("⚠️ SRT output requires an original SRT file. Output will be TXT style with timestamps.")
                buffer = BytesIO()
                buffer.write(translated_text.encode("utf-8"))
                buffer.seek(0)
                st.download_button(
                    label="📥 Download SRT",
                    data=buffer,
                    file_name=f"translated.{target_language}.srt",
                    mime="text/plain"
                )
            st.success("🎉 Translation completed!")
        except Exception as e:
            st.error(f"❌ Error generating output file: {e}")
