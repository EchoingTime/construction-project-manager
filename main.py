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
        - python main.py
    - Testing Account: test@test.com | Test123
    - Control + C to stop the server
@Referenced: https://www.youtube.com/watch?v=dam0GPOAvVI&ab_channel=TechWithTim
"""

from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)