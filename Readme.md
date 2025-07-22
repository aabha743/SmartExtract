SmartExtract
SmartExtract is a Streamlit web application designed to extract questions and images from a PDF file, specifically tailored for educational content. The app processes the PDF to extract text and images, organizes the content into a structured JSON format, and provides a downloadable ZIP file containing the JSON and extracted images.
Features

Upload a PDF file through a user-friendly web interface.
Extract text (questions and options) and images from the PDF using pdfplumber.
Organize content into a JSON file with the structure:[
    {
        "question": "Question text",
        "images": "path/to/question_image.png",
        "option_images": ["path/to/option_image_1.png", ...]
    },
    ...
]


Display the extracted JSON content in the app.
Provide a downloadable ZIP file containing the JSON and all extracted images.

Prerequisites

Python 3.8 or higher
Streamlit
pdfplumber
Pillow

Installation

Clone the Repository (if applicable):
git clone <repository-url>
cd MathExtract


Create a Virtual Environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install streamlit pdfplumber pillow



Running the Application

Ensure the Script is Saved:

Save the Streamlit app code as app.py in your project directory.


Run the Streamlit App:
streamlit run app.py


This command starts the Streamlit server and opens the app in your default web browser (typically at http://localhost:8501).


Using the App:

Upload a PDF: Use the file uploader to select a PDF file (e.g., "IMO Class 1 Maths Olympiad Sample Paper 1 for the year 2024-25.pdf").
View JSON Output: The extracted content will be displayed as JSON in the app.
Download ZIP: Click the "Download ZIP (JSON + Images)" button to download a ZIP file containing the extracted_content.json and all extracted images.



Project Structure

app.py: The main Streamlit application script.
extracted_output/extract_YYYYMMDD_HHMMSS/: Directory where extracted images and JSON are saved (created dynamically with a timestamp).
temp/: Temporary directory for storing the uploaded PDF during processing.

Notes

PDF Structure: The app assumes each question may have one main image (e.g., a figure pattern) and up to four option images, based on typical Olympiad paper layouts. If your PDF has a different structure, you may need to adjust the image assignment logic in app.py.
Error Handling: The app includes error handling for PDF processing and image extraction. Check the app interface for any error messages if issues arise.
Cleanup: The temporary PDF file is automatically deleted after processing. The extracted output is saved in a timestamped directory to avoid conflicts.

Troubleshooting

Module Not Found: Ensure all dependencies are installed using pip install streamlit pdfplumber pillow.
PDF Processing Errors: Verify that the PDF is not corrupted and is accessible. Complex layouts may require switching to PyMuPDF for better extraction.
Port Conflict: If http://localhost:8501 is unavailable, Streamlit will prompt you to use a different port (e.g., streamlit run app.py --server.port 8502).

License
This project is licensed under the MIT License.