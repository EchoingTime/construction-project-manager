"""
@File Name: main.py
@Description: This file contains the main entry point for our Flask application.
@Running:
    - Open Visual Studio Code's terminal
    - Run the following commands:
        - python -m venv venv (if venv doesn't already exist)
        - source venv/bin/activate (Mac/Linux)
        - venv\Scripts\activate (Windows)
        - pip install -r requirements.txt
        - Optional: Set Flask environment variable:
            - export FLASK_APP=main.py (Mac/Linux)  # Set the app to main.py
            - set FLASK_APP=main.py (Windows)       # Set the app to main.py
            - flask run                             # Run the Flask app
        - Or you can run it directly:
            - python main.py                        # Alternatively, run Flask directly with python
    - Testing Account: test@test.com | Test1234
    - Control + C to stop the server
@References
    - https://www.youtube.com/watch?v=dam0GPOAvVI&ab_channel=TechWithTim
    - ChatGPT for formatted and detailed Running Steps
"""

from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)