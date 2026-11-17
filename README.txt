PYTHON QUIZ APPLICATION - FLASK WEBSITE

FEATURES
- Same five Python questions from your original Python program.
- Random question order and randomized answer options.
- Student name entry and multiple-choice quiz.
- Automatic score and percentage calculation.
- Saves every attempt to quiz_results.csv.
- Uses Pandas to calculate average, highest and lowest scores.
- Results table and two charts: score distribution and student performance.

STEP 1 - Install Python
Make sure Python 3 is installed. In Terminal, check:
    python3 --version

STEP 2 - Open the project folder
Extract python_quiz_website.zip.
Open the extracted "python_quiz_website" folder in Visual Studio Code.

STEP 3 - Open the VS Code terminal
Choose Terminal > New Terminal.

STEP 4 - Create and activate a virtual environment (recommended)
Mac:
    python3 -m venv venv
    source venv/bin/activate

Windows:
    py -m venv venv
    venv\Scripts\activate

STEP 5 - Install the required packages
    pip install -r requirements.txt

STEP 6 - Run the website
Mac:
    python3 app.py

Windows:
    python app.py

STEP 7 - Open the website
In your browser, visit:
    http://127.0.0.1:5000

HOW TO USE
1. Enter the student's name on the home page.
2. Click Start quiz.
3. Select one answer for each of the five questions.
4. Click Submit quiz to see the score and answer review.
5. Open Results & Analysis to view all saved attempts and charts.

DATA STORAGE
The website creates quiz_results.csv in the project folder after the first quiz is submitted.
Do not delete this file if you want to keep the saved results.

NOTE
The website uses Chart.js from a CDN for the browser charts, so an internet connection is needed to load the charts.
For a real deployment, set a strong SECRET_KEY environment variable and turn debug mode off.
