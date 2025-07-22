# SmartExtract

**SmartExtract** is a Streamlit web application designed to extract questions and images from a PDF file, specifically tailored for educational content such as Olympiad sample papers. It processes the PDF to extract text and images, organizes the content into a structured JSON format, and provides a downloadable ZIP file containing the JSON and extracted images.

---

## 🚀 Features

- 📂 Upload a PDF file through a user-friendly web interface.
- 📝 Extract text (questions and options) and images from the PDF using `pdfplumber`.
- 📁 Organize content into a structured JSON format:

```json
[
    {
        "question": "Question text",
        "images": "path/to/question_image.png",
        "option_images": ["path/to/option_image_1.png", ...]
    },
    ...
]
```

- 🖥️ Display the extracted JSON content in the app.
- 📦 Download a ZIP file containing the `extracted_content.json` and all extracted images.

---

## ⚙️ Prerequisites

- Python 3.8 or higher
- [Streamlit](https://streamlit.io/)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [Pillow](https://python-pillow.org/)

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd SmartExtract
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install streamlit pdfplumber pillow
```

---

## ▶️ Running the Application

1. **Save the Streamlit script as `app.py`** in your project directory.

2. **Launch the app:**

```bash
streamlit run app.py
```

This will start the Streamlit server and open the app in your default web browser at:  
http://localhost:8501

---

## 🧪 Using the App

- **Upload a PDF:** Use the file uploader to select a sample paper (e.g., `IMO Class 1 Maths Olympiad Sample Paper 1 for the year 2024-25.pdf`).
- **View JSON Output:** The extracted content will be displayed in JSON format.
- **Download ZIP:** Click the `Download ZIP (JSON + Images)` button to download the `extracted_content.json` and extracted images in a ZIP file.

---

## 📁 Project Structure

```
SmartExtract/
│
├── app.py                        # Main Streamlit application
├── extracted_output/
│   └── extract_YYYYMMDD_HHMMSS/ # Timestamped output directory (JSON + images)
├── temp/                         # Temporary PDF storage during processing
```

---

## 📝 Notes

- **PDF Layout Assumption:** Designed for educational papers where each question may have:
  - One main image (e.g., figure or diagram)
  - Up to four option images

  If your PDF differs structurally, you may need to modify image parsing logic in `app.py`.

- **Error Handling:** The app includes basic error messages for corrupted PDFs or unexpected layouts.

- **Temporary File Cleanup:** Uploaded PDFs are deleted after processing. Extracted content is stored in timestamped directories to prevent overwriting.

---

## ❗ Troubleshooting

- **Module Not Found:** Ensure dependencies are installed:

```bash
pip install streamlit pdfplumber pillow
```

- **PDF Extraction Errors:** Use clean, text-based PDFs. For complex layouts, consider switching to [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) for better handling.

- **Port Conflict:** If `localhost:8501` is busy, run:

```bash
streamlit run app.py --server.port 8502
```

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
