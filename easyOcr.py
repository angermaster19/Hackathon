import cv2
import easyocr
from sentence_transformers import SentenceTransformer, util

# Initialize EasyOCR and SentenceTransformer models
reader = easyocr.Reader(['en'])
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to extract text using EasyOCR
def extract_text(image_path):
    text = reader.readtext(image_path, detail=0)
    return " ".join(text)  # Combine extracted text

# Function to detect answer regions (optional improvement)
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
    # Extract text using EasyOCR
    extracted_text = extract_text(image_path)
    print("Extracted Text:", extracted_text)

    # Detect answer regions (optional)
    regions = detect_answer_regions(image_path)
    print(f"Detected {len(regions)} answer regions.")

    # Grade answers
    scores = []
    for i, model_answer in enumerate(model_answers):
        student_answer = extracted_text  # Process each detected region separately if needed
        status, marks = grade_answers(student_answer, model_answer)
        scores.append((i + 1, status, marks))

    # Print results
    print("\nEvaluation Results:")
    for question, status, marks in scores:
        print(f"Question {question}: {status} ({marks} marks)")

# Example usage
if __name__ == "__main__":
    # Example image and model answers
    image_path = "handwritten_answer_sheet.jpg"
    model_answers = [
        "The process of photosynthesis involves converting light energy into chemical energy.",
        "Newton's second law states that force equals mass times acceleration."
    ]

    evaluate_answer_sheet(image_path, model_answers)
