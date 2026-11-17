from flask import Flask, render_template, request, redirect, url_for, session, flash
import csv
import os
import random
import pandas as pd

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")
RESULTS_FILE = "quiz_results.csv"

# Questions are taken from the uploaded Python quiz application.
QUESTIONS = [
    {
        "question": "Which language is used for data analysis?",
        "options": ["Python", "HTML", "CSS", "SQL"],
        "answer": "Python"
    },
    {
        "question": "Which keyword is used to define a function in Python?",
        "options": ["function", "def", "fun", "define"],
        "answer": "def"
    },
    {
        "question": "Which data structure stores key-value pairs?",
        "options": ["List", "Tuple", "Dictionary", "Set"],
        "answer": "Dictionary"
    },
    {
        "question": "Which library is mainly used for data analysis?",
        "options": ["Pandas", "Turtle", "Tkinter", "Random"],
        "answer": "Pandas"
    },
    {
        "question": "Which function generates a random number?",
        "options": ["random()", "generate()", "number()", "rand()"],
        "answer": "random()"
    }
]


def load_results():
    if not os.path.exists(RESULTS_FILE):
        return pd.DataFrame(columns=["Student Name", "Score", "Total", "Percentage"])
    try:
        return pd.read_csv(RESULTS_FILE)
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        return pd.DataFrame(columns=["Student Name", "Score", "Total", "Percentage"])


def save_result(student_name, score, total, percentage):
    file_exists = os.path.exists(RESULTS_FILE)
    with open(RESULTS_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists or os.path.getsize(RESULTS_FILE) == 0:
            writer.writerow(["Student Name", "Score", "Total", "Percentage"])
        writer.writerow([student_name, score, total, round(percentage, 2)])


@app.route("/")
def index():
    data = load_results()
    stats = {
        "attempts": int(len(data)),
        "average": round(float(data["Percentage"].mean()), 1) if not data.empty else 0,
        "highest": int(data["Score"].max()) if not data.empty else 0,
        "lowest": int(data["Score"].min()) if not data.empty else 0,
    }
    return render_template("index.html", stats=stats)


@app.route("/start", methods=["POST"])
def start_quiz():
    student_name = request.form.get("student_name", "").strip()
    if not student_name:
        flash("Please enter your name before starting the quiz.", "error")
        return redirect(url_for("index"))

    quiz_questions = []
    for question in QUESTIONS:
        item = {
            "question": question["question"],
            "options": random.sample(question["options"], len(question["options"])),
            "answer": question["answer"]
        }
        quiz_questions.append(item)
    random.shuffle(quiz_questions)

    session["student_name"] = student_name
    session["quiz_questions"] = quiz_questions
    return redirect(url_for("quiz"))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    quiz_questions = session.get("quiz_questions")
    if not quiz_questions:
        flash("Start a new quiz to begin.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        score = 0
        review = []
        for i, question in enumerate(quiz_questions):
            selected = request.form.get(f"answer_{i}", "")
            correct = selected == question["answer"]
            if correct:
                score += 1
            review.append({
                "question": question["question"],
                "selected": selected or "Not answered",
                "correct_answer": question["answer"],
                "correct": correct
            })

        total = len(quiz_questions)
        percentage = (score / total) * 100
        student_name = session.get("student_name", "Student")
        save_result(student_name, score, total, percentage)
        session.pop("quiz_questions", None)
        session.pop("student_name", None)
        return render_template(
            "result.html",
            student_name=student_name,
            score=score,
            total=total,
            percentage=round(percentage, 1),
            review=review
        )

    return render_template(
        "quiz.html",
        questions=quiz_questions,
        student_name=session.get("student_name", "Student")
    )


@app.route("/results")
def results():
    data = load_results()
    records = data.fillna("").to_dict(orient="records")
    stats = {
        "attempts": int(len(data)),
        "average": round(float(data["Percentage"].mean()), 1) if not data.empty else 0,
        "highest": int(data["Score"].max()) if not data.empty else 0,
        "lowest": int(data["Score"].min()) if not data.empty else 0,
        "top_student": str(data.loc[data["Score"].idxmax(), "Student Name"]) if not data.empty else "—",
    }
    chart_data = {
        "names": data["Student Name"].astype(str).tolist() if not data.empty else [],
        "percentages": data["Percentage"].fillna(0).astype(float).tolist() if not data.empty else [],
        "scores": data["Score"].fillna(0).astype(int).tolist() if not data.empty else [],
    }
    return render_template("results.html", records=records, stats=stats, chart_data=chart_data)


if __name__ == "__main__":
    app.run(debug=True)
