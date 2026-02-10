import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image
import io
from googletrans import Translator
import pytesseract
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# No local path needed – packages.txt handles tesseract & poppler

st.set_page_config(page_title="My Free AI Tools - Faizan", layout="wide")
st.title("My Free AI Tools by Faizan")
st.markdown("100% Free AI Tools: Translate Books/PDFs fast, Convert PDF to Images, Images to PDF, Extract Text (OCR). Made in Jalgaon!")

translator = Translator()

tab1, tab2, tab3, tab4 = st.tabs(["Translate Book/PDF", "PDF → Image", "Image/JPG → PDF", "OCR Text Extract"])

with tab1:
    st.header("Translate Book or PDF/Text (up to 1000 pages in chunks)")
    uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
    target_lang = st.selectbox("Target Language", ["hi", "en", "mr", "gu", "fr", "es"])
    if uploaded_file and st.button("Translate Now"):
        with st.spinner("Reading & Translating... (large files take time)"):
            text = ""
            if uploaded_file.type == "application/pdf":
                images = convert_from_bytes(uploaded_file.getvalue())
                for img in images:
                    text += pytesseract.image_to_string(img) + "\n"
            else:
                text = uploaded_file.getvalue().decode("utf-8", errors="ignore")
            # Translate in chunks to avoid limits
            chunks = [text[i:i+4500] for i in range(0, len(text), 4500)]
            translated = ""
            for chunk in chunks:
                translated += translator.translate(chunk, dest=target_lang).text
        st.text_area("Translated Text", translated, height=400)
        st.download_button("Download Translated TXT", translated, file_name="translated_book.txt")

with tab2:
    st.header("PDF to Images (PNG)")
    pdf_upload = st.file_uploader("Upload PDF File", type="pdf")
    if pdf_upload and st.button("Convert to PNG"):
        with st.spinner("Converting pages..."):
            pages = convert_from_bytes(pdf_upload.getvalue())
            for num, page in enumerate(pages, 1):
                buf = io.BytesIO()
                page.save(buf, format="PNG")
                st.download_button(f"Page {num}.png", buf.getvalue(), f"page_{num}.png")

with tab3:
    st.header("Images to PDF")
    images_upload = st.file_uploader("Upload JPG/PNG Images", type=["jpg", "png"], accept_multiple_files=True)
    if images_upload and st.button("Make PDF"):
        with st.spinner("Combining into PDF..."):
            pdf_buf = io.BytesIO()
            c = canvas.Canvas(pdf_buf, pagesize=letter)
            for img_file in images_upload:
                img = Image.open(img_file)
                c.drawInlineImage(img, 30, 50, width=550, height=750)
                c.showPage()
            c.save()
        st.download_button("Download PDF", pdf_buf.getvalue(), "combined_images.pdf")

with tab4:
    st.header("OCR - Extract Text from Image/Scanned PDF")
    ocr_file = st.file_uploader("Upload Image or PDF", type=["jpg", "png", "pdf"])
    if ocr_file and st.button("Extract Text"):
        with st.spinner("Extracting..."):
            text_ex = ""
            if ocr_file.type == "application/pdf":
                imgs = convert_from_bytes(ocr_file.getvalue())
                text_ex = pytesseract.image_to_string(imgs[0])  # First page for demo
            else:
                text_ex = pytesseract.image_to_string(Image.open(ocr_file))
        st.text_area("Extracted Text", text_ex, height=300)

st.markdown("© Faizan 2026 | Free forever | Powered by Streamlit & Open Tools")
