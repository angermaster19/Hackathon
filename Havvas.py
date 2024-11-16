import easyocr
from sentence_transformers import SentenceTransformer, util
import cv2

# Initialize OCR reader and Sentence-Transformer model
reader = easyocr.Reader(['en'])  # Initialize EasyOCR reader for English
model = SentenceTransformer('all-MiniLM-L6-v2')  # Pre-trained model from Hugging Face

# Function to extract text using EasyOCR from image
def extract_text_from_image(image_path):
    # Read image with EasyOCR
    result = reader.readtext(image_path, detail=0)  # detail=0 gives only text, not bounding boxes
    return " ".join(result)  # Join the extracted text into a single string

# Function to calculate semantic similarity between model answer and student answer
def calculate_similarity(student_answer, model_answer):
    # Convert both answers to embeddings
    student_embedding = model.encode(student_answer, convert_to_tensor=True)
    model_embedding = model.encode(model_answer, convert_to_tensor=True)
    
    # Calculate cosine similarity between both embeddings
    similarity = util.pytorch_cos_sim(student_embedding, model_embedding).item()
    return similarity

# Function to evaluate the subjective answer
def evaluate_subjective_answer(image_path, model_answer):
    # Extract text from the answer sheet image
    student_answer = extract_text_from_image(image_path)
    print(f"Extracted Student Answer: {student_answer}")
    
    # Calculate the similarity between the student's answer and the model answer
    similarity = calculate_similarity(student_answer, model_answer)
    
    # Define thresholds for grading
    if similarity > 0.7:
        return "Correct", 10  # Full marks
    elif similarity > 0.5:
        return "Partially Correct", 5  # Partial marks
    else:
        return "Incorrect", 0  # No marks

# Example usage
if __name__ == "__main__":
    # Example subjective answer sheet image and model answer
    image_path = "student_answer_sheet.jpg"  # Path to the image file
    model_answer = "Newton's laws of motion describe the relationship between a body and the forces acting on it."
    
    # Evaluate the student's subjective answer
    result, marks = evaluate_subjective_answer(image_path, model_answer)
    
    print(f"Evaluation Result: {result} ({marks} marks)")
