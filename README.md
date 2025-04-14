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
2. Install the dependencies using:

```python
pip install -r requirements.txt
```

## Running the Code:

- Instructions for running the code can be found in main.py

## Testing Accounts:

- Contractor: test@con.com | test123
- Subcontractor: test@sub.com | test123

## Database Modifications:

After making a change to models.py (adding a new table or modifying an existing one), read the instructions below. If viewing via IDE, do not include Python (this is for styling the README).

1. Activate the virtual environment
   - For Windows Command Prompt/VS Code Terminal
     ```python
     venv\Scripts\activate.bat
     ```
   - For Git Bash or WSL (Mac/Linux)
     ```
     python source venv/Scripts/activate
     ```
2. Set FLASK_APP
   - For Windows Command Prompt/VS Code Terminal
     ```python
     set FLASK_APP=main.py
     ```
   - For Git Bash or WSL (Mac/Linux):
     ```python
     export FLASK_APP=main.py
     ```
3. Generate migration file
   - **This is an example:**
     ```python
     flask --app main.py db migrate -m "Renamed data column to project_name"
     ```
4. (Provided via ChatGPT - This is for the above example) Modify the generated migration file:
   - Open the migration file located in the `migrations/versions` folder.
   - Add the following code to migrate data from `data` to `project_name`:
     ```python
     op.execute('UPDATE project SET project_name = data')
     ```
   - Make sure the data is copied before dropping the old `data` column.
5. Apply the migration
   ```python
   flask --app main.py db upgrade
   ```

## References

- “An Idea for a Simple Responsive Spreadsheet | CSS-Tricks.” CSS-Tricks, 28 Nov. 2017, css-tricks.com/idea-simple-responsive-spreadsheet/.
- 2025.Coding2GO. “Login & Signup with HTML, CSS, JavaScript (Form Validation).” YouTube, 13 July 2024, www.youtube.com/watch?v=bVl5_UdcAy0.
- “How to Create a Responsive Navigation Bar (for Beginners).” Www.youtube.com, www.youtube.com/watch?v=U8smiWQ8Seg.
- Open Source Coding. “Modern Calendar with Todo in HTML, CSS and JS Part 2 | JavaScript Events Calendar.” YouTube, 16 Nov. 2022, www.youtube.com/watch?v=r1devGCrm2Y. Accessed 11 Apr. 2025.
- OpenAI. “ChatGPT.” ChatGPT, OpenAI, chatgpt.com/.
- “Python Website Full Tutorial - Flask, Authentication, Databases & More.” Www.youtube.com, www.youtube.com/watch?v=dam0GPOAvVI. Accessed 20 June 2021.
