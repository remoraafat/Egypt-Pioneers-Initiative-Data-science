import fitz

def extract_text_from_pdf(file_path):
    """
    Extracts and returns plain text from a PDF file.
    """
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"
    
    

#Test the function with a sample PDF file
if __name__ == "__main__":
    # Replace 'sample.pdf' with the path to your PDF file
    pdf_file_path = 'test.pdf'
    extracted_text = extract_text_from_pdf(pdf_file_path)
    print(extracted_text)