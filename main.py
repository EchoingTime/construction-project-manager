"""
@File Name: main.py
@Description: This file contains the main entry point for the Flask application.
@Running:
    - Open Visual Studio Code's terminal
    - Run the following commands (may need to write python3 instead):
        - python -m venv venv
        - (Mac/Linux): source venv/bin/activate
        - (Windows): venv\Scripts\activate
        - pip install -r requirements.txt (to update: pip freeze > requirements.txt)
        - python main.py 
    - Testing Accounts 
        - Contractor Testing Account: test@con.com | test123          
        - Subcontractor Testing Account: test@sub.com | test123        
    - Control + C to stop the server
"""

from website import create_app, create_database
from flask_mail import Mail

app = create_app()
create_database(app) # Constructs the database
app.config.from_object('config.Config') # Configures the app with the settings in config.py
mail = Mail(app)

if __name__ == '__main__':
    app.run(debug=True)