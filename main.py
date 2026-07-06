import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Placeholder data - replace with actual database or logic
TOPICS = ["Machine Learning", "Deep Learning", "Natural Language Processing", "Computer Vision", "Reinforcement Learning"]

QUIZZES = [
    {
        "id": 1,
        "title": "Introduction to ML",
        "topic": "Machine Learning",
        "questions": [
            {
                "id": "q1",
                "question_text": "What is overfitting?",
                "options": ["Model is too simple", "Model performs poorly on training data", "Model performs well on training data but poorly on unseen data", "Model is not trained enough"]
            },
            {
                "id": "q2",
                "question_text": "Which algorithm is unsupervised?",
                "options": ["Linear Regression", "K-Means", "Decision Tree", "Support Vector Machine"]
            }
        ]
    },
    {
        "id": 2,
        "title": "NLP Basics",
        "topic": "Natural Language Processing",
        "questions": [
            {
                "id": "q3",
                "question_text": "What does NLP stand for?",
                "options": ["New Programming Language", "Natural Programming Language", "Natural Language Processing", "Non-linear Programming Language"]
            }
        ]
    }
]

@app.get("/api/topics")
def get_topics():
    return TOPICS

@app.get("/api/quizzes")
def get_quizzes(topic: str = None):
    if topic:
        return [q for q in QUIZZES if q["topic"] == topic]
    return QUIZZES

@app.get("/api/quizzes/{quiz_id}")
def get_quiz(quiz_id: int):
    for quiz in QUIZZES:
        if quiz["id"] == quiz_id:
            return quiz
    return {"message": "Quiz not found"}

@app.post("/api/quizzes/submit")
def submit_quiz_answers(submission: dict):
    # In a real app, you would validate answers, calculate score, and provide detailed explanations
    quiz_id = submission.get("quiz_id")
    answers = submission.get("answers", {})
    
    # Find the quiz to get correct answers (for demo purposes)
    quiz = next((q for q in QUIZZES if q["id"] == quiz_id), None)
    if not quiz:
        return {"error": "Quiz not found"}

    explanations = []
    score = 0
    for question in quiz["questions"]:
        user_answer = answers.get(question["id"])
        correct_answer_text = "Not answered"
        is_correct = False
        
        # Find the correct answer for demonstration
        # This assumes the first option is always the correct one for simplicity in this mock
        # A real implementation would require storing correct answers explicitly.
        if question["options"]:
            correct_answer_option = question["options"][0]
            if user_answer == correct_answer_option:
                is_correct = True
                score += 1
                correct_answer_text = correct_answer_option
            else:
                correct_answer_text = correct_answer_option # Show what the correct one was
        
        explanations.append({
            "question_id": question["id"],
            "question_text": question["question_text"],
            "your_answer": user_answer if user_answer else "Not answered",
            "correct_answer": correct_answer_text,
            "is_correct": is_correct
        })

    return {
        "message": "Quiz submitted successfully!",
        "score": f"{score}/{len(quiz['questions'])}",
        "explanations": explanations
    }

@app.get("/api/search/quizzes")
def search_quizzes(q: str = None):
    if not q:
        return QUIZZES
    q_lower = q.lower()
    results = []
    for quiz in QUIZZES:
        if q_lower in quiz["title"].lower() or q_lower in quiz["topic"].lower():
            results.append(quiz)
    return results

# Serve frontend static files and index.html
if os.path.isdir("frontend/build"):
    app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")

    @app.get("/{path:path}")
    async def serve_frontend(path: str):
        if path.startswith("api/") or path == "":
            # This case should ideally not be hit by the frontend routing logic 
            # for api paths. The empty path is for the root.
            # For other paths, FastAPI will handle routing or return a 404.
            return {"message": "API endpoint or not found"}
        else:
            # Serve index.html for all other paths to enable frontend routing
            return FileResponse("frontend/build/index.html")

else:
    # If frontend/build does not exist (e.g., during initial setup or testing),
    # ensure the API routes are still accessible.
    @app.get("/")
    async def root_message():
        return {"message": "FastAPI backend is running. Frontend build not found."}
