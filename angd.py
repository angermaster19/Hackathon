import cv2
import pytesseract
from sentence_transformers import SentenceTransformer, util

# Configure Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to extract text using OCR
def extract_text(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV)
    text = pytesseract.image_to_string(thresh, lang='eng')
    return text

# Function to detect answer regions
def detect_answer_regions(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 100 and h > 50:  # Filter by size
            regions.append((x, y, w, h))
    return regions

# Function to calculate semantic similarity
def calculate_similarity(student_answer, model_answer):
    model_embedding = model.encode(model_answer, convert_to_tensor=True)
    student_embedding = model.encode(student_answer, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(model_embedding, student_embedding).item()
    return similarity

# Function to grade answers
def grade_answers(student_answer, model_answer):
    similarity = calculate_similarity(student_answer, model_answer)
    if similarity > 0.7:
        return "Correct", 10
    elif similarity > 0.5:
        return "Partially Correct", 5
    else:
        return "Incorrect", 0

# Main function
def evaluate_answer_sheet(image_path, model_answers):
    # Extract text from the full image
    extracted_text = extract_text(image_path)
    print("Extracted Text:", extracted_text)

    # Detect answer regions
    regions = detect_answer_regions(image_path)
    print(f"Detected {len(regions)} answer regions.")

    # For each detected region (you may need to segment and process each separately)
    scores = []
    for i, model_answer in enumerate(model_answers):
        student_answer = extracted_text  # In a real system, this would segment the text
        status, marks = grade_answers(student_answer, model_answer)
        scores.append((i + 1, status, marks))

    # Print results
    print("\nEvaluation Results:")
    for question, status, marks in scores:
        print(f"Question {question}: {status} ({marks} marks)")

# Example usage
if __name__ == "__main__":
    # Example image and answers
    image_path = "handwritten_answer_sheet.jpg"
    model_answers = [
        "The process of photosynthesis involves converting light energy into chemical energy.",
        "Newton's second law states that force equals mass times acceleration."
    ]

    evaluate_answer_sheet(image_path, model_answers)
