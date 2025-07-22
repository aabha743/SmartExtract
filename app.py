import streamlit as st
import pdfplumber
import os
import json
import re
from PIL import Image
import io
import zipfile
from datetime import datetime

def extract_pdf_content(pdf_file, output_dir):
    """
    Extracts text and images from a PDF file using pdfplumber.
    Organizes content into a JSON with question, images, and option_images.
    Returns JSON content, JSON path, and output directory.
    """
    # Create output directory with timestamp to avoid conflicts
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(output_dir, f"extract_{timestamp}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    questions = []
    image_counter = 0
    saved_images = []
    
    with pdfplumber.open(pdf_file) as pdf:
        for page_num, page in enumerate(pdf.pages):
            # Extract text
            text = page.extract_text() or ""
            
            # Split text into lines and parse questions
            lines = text.split('\n')
            current_question = None
            current_options = []
            question_text = ""
            in_question = False
            
            # Regex to match question numbers, options, and answers
            question_pattern = re.compile(r'^\s*(\d+)\.\s*(.*?)(?=\s*\[A\]|$)', re.DOTALL)
            option_pattern = re.compile(r'^\s*\[([A-D])\]\s*(.*?)(?=\s*\[|$)', re.MULTILINE)
            answer_pattern = re.compile(r'Ans\s*\[([A-D])\]|\[([A-D])\]\s*$')
            
            for line in lines:
                # Check for question start
                question_match = question_pattern.match(line)
                if question_match:
                    if current_question:
                        # Save previous question
                        questions.append({
                            "question": question_text.strip(),
                            "images": "",
                            "option_images": []
                        })
                    question_text = question_match.group(2).strip()
                    in_question = True
                    current_options = []
                    continue
                
                # Check for options
                option_match = option_pattern.match(line)
                if option_match:
                    current_options.append(option_match.group(1))
                    continue
                
                # Check for answer or end of question
                answer_match = answer_pattern.search(line)
                if answer_match:
                    if current_question:
                        questions.append({
                            "question": question_text.strip(),
                            "images": "",
                            "option_images": []
                        })
                        in_question = False
                        question_text = ""
                    continue
                
                # Append to question text if in question
                if in_question:
                    question_text += " " + line.strip()
            
            # Append last question on page
            if in_question and question_text.strip():
                questions.append({
                    "question": question_text.strip(),
                    "images": "",
                    "option_images": []
                })
            
            # Extract images
            images = page.images
            for img_index, img in enumerate(images):
                try:
                    # Define bounding box for cropping: (x0, top, x1, bottom)
                    bbox = (img['x0'], img['top'], img['x1'], img['bottom'])
                    
                    # Crop the page to the image bounding box
                    cropped_page = page.crop(bbox)
                    
                    # Convert to image with higher resolution
                    image_obj = cropped_page.to_image(resolution=300)
                    pil_image = image_obj.original
                    
                    # Define image filename and path
                    image_filename = f"page{page_num + 1}_image{img_index + 1}.png"
                    image_path = os.path.join(output_dir, image_filename)
                    
                    # Save the image as PNG
                    pil_image.save(image_path, format="PNG")
                    saved_images.append(image_path)
                    
                    # Assign images to questions
                    if questions:
                        question_index = len(questions) - 1
                        if image_counter % 5 == 0:  # Assume first image is question image
                            questions[question_index]["images"] = image_filename
                        else:  # Subsequent images are option images
                            questions[question_index]["option_images"].append(image_filename)
                    image_counter += 1
                except Exception as e:
                    st.error(f"Error extracting image {img_index + 1} on page {page_num + 1}: {e}")
    
    # Save the JSON file
    json_path = os.path.join(output_dir, "extracted_content.json")
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(questions, json_file, ensure_ascii=False, indent=4)
    
    return questions, json_path, output_dir

def create_zip(output_dir):
    """
    Creates a ZIP file containing all files in the output directory.
    Returns the path to the ZIP file.
    """
    zip_path = f"{output_dir}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)
    return zip_path

# Streamlit app
st.title("PDF Content Extraction App")
st.write("Upload a PDF file to extract questions and images, and generate a JSON output.")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    temp_pdf_path = os.path.join("temp", "uploaded.pdf")
    os.makedirs("temp", exist_ok=True)
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Process the PDF
    with st.spinner("Extracting content from PDF..."):
        try:
            questions, json_path, output_dir = extract_pdf_content(temp_pdf_path, "extracted_output")
            
            # Create ZIP file
            zip_path = create_zip(output_dir)
            
            # Display JSON content
            st.subheader("Extracted Content (JSON)")
            st.json(questions)
            
            # Provide download button for ZIP
            with open(zip_path, "rb") as zip_file:
                zip_content = zip_file.read()
            st.download_button(
                label="Download ZIP (JSON + Images)",
                data=zip_content,
                file_name="extracted_content.zip",
                mime="application/zip"
            )
            
            st.success(f"Extraction complete. Output directory: {output_dir}")
        except Exception as e:
            st.error(f"Error processing PDF: {e}")
    
    # Clean up temporary PDF
    if os.path.exists(temp_pdf_path):
        os.remove(temp_pdf_path)