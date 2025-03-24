"""
@File Name: main.py
@Description: This file contains the main entry point for our Flask application.
@Running:
    - Open Visual Studio Code's terminal
    - Run the following commands:
        - python (or python3) -m venv venv (if venv doesn't already exist)
        - source venv/bin/activate (Mac/Linux)
        - venv\Scripts\activate (Windows)
        - pip install -r requirements.txt (to update: pip freeze > requirements.txt)
        - python (or python3) main.py 
    - Testing Account: test@test.com | test123          
    - Test Message Account: test2@test.com | test123        
    - Test Subcontractor Account: subcon@test.com | subpass 
    - Control + C to stop the server

    (test accounts 1 and 2 are *default* contractors because they were made before the user table had a "role" field)
"""

from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)