import easyocr
from transformers import BertTokenizer
import torch

# Initialize OCR reader for English text using EasyOCR
reader = easyocr.Reader(['en'])

# Initialize Hugging Face tokenizer (e.g., BERT tokenizer)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Function to extract text from an image using EasyOCR
def extract_text_from_image(image_path):
    # Extract text using EasyOCR
    result = reader.readtext(image_path, detail=0)  # detail=0 gives only text, not bounding boxes
    return " ".join(result)  # Join the list into a single string

# Function to tokenize the extracted text using Hugging Face tokenizer
def tokenize_text(text):
    # Tokenize the text using the tokenizer
    encoding = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    return encoding

# Example usage
if __name__ == "__main__":
    # Path to the image with the answer
    image_path = "path_to_your_image.jpg"
    
    # Step 1: Extract text from the image
    extracted_text = extract_text_from_image(image_path)
    print(f"Extracted Text: {extracted_text}")
    
    # Step 2: Tokenize the extracted text
    tokenized_text = tokenize_text(extracted_text)
    print(f"Tokenized Text: {tokenized_text}")

    # You can access the tokenized input like this:
    print("Input IDs:", tokenized_text['input_ids'])
    print("Attention Mask:", tokenized_text['attention_mask'])
