# Construction Project Manager

# Authors of Project

- Dante Anzalone
- Nicholas Pietruszka
- Patrick Sawicki
- Joe Wagner

## Description:

This is a web application built using Flask and other modern technologies to manage construction projects.

## Dependencies and Versions:

- **Python**: 3.13.2
- **JavaScript**: (ES6+)
- **HTML5**
- **jQuery**: 3.6.0
- **Flask**: 3.1.0
- **Flask-Login**: 0.6.3
- **Flask-Migrate**: 4.1.0
- **Flask-SQLAlchemy**: 3.1.1
- **Jinja2**: 3.1.5
- **SQLAlchemy**: 2.0.38

## Others:

- **alembic**: 1.15.1
- **blinker**: 1.9.0
- **click**: 8.1.8
- **colorama**: 0.4.6
- **greenlet**: 3.1.1
- **itsdangerous**: 2.2.0
- **Mako**: 1.3.9
- **MarkupSafe**: 3.0.2
- **typing_extensions**: 4.12.2
- **Werkzeug**: 3.1.3

## Installation:

1. Clone the repository: https://github.com/EchoingTime/construction-project-manager.git
2. Install the dependencies using `pip install -r requirements.txt`.

## Running the Code:

- Instructions for running the code can be found in main.py

## Testing Accounts:

- test@test.com | test123
- test2@test.com | test123
- subcon@test.com | subpass

## Database Modifications:

After making a change to models.py (adding a new table or modifying an existing one), read the instructions below.

1. Activate the virtual environment
   - For Windows Command Prompt/VS Code Terminal
     - venv\Scripts\activate.bat
   - For Git Bash or WSL (Mac/Linux)
     - source venv/Scripts/activate
2. Set FLASK_APP
   - For Windows Command Prompt/VS Code Terminal
     - set FLASK_APP=main.py
   - For Git Bash or WSL (Mac/Linux):
     - export FLASK_APP=main.py
3. Generate migration file
   - **This is an example:**
     '''flask --app main.py db migrate -m "Renamed data column to project_name"
     '''
4. (Provided via ChatGPT) Modify the generated migration file:
   - Open the migration file located in the `migrations/versions` folder.
   - Add the following code to migrate data from `data` to `project_name`:
     ```python
     op.execute('UPDATE project SET project_name = data')
     ```
   - Make sure the data is copied before dropping the old `data` column.
5. Apply the migration
   - flask --app main.py db upgrade

## References

- "Login & Signup with HTML, CSS, JavaScript (form validation)." Www.youtube.com, https://www.youtube.com/watch?v=bVl5_UdcAy0&ab_channel=Coding2GO.
- “How to Create a Responsive Navigation Bar (for Beginners).” Www.youtube.com, https://www.youtube.com/watch?v=U8smiWQ8Seg&ab_channel=Coding2GO.
- “Python Website Full Tutorial - Flask, Authentication, Databases & More.” Www.youtube.com, https://www.youtube.com/watch?v=dam0GPOAvVI&ab_channel=TechWithTim.
- ChatGPT for formatting header documentation
