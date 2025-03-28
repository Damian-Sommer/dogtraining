# Hundetrainings

# TODOs
 - [ ] Einzelne Trainingsbesuche
 - [ ] Trainingsabos / Karten

# Code Style:

Klassennamen: "Upper Camel Case" --> "SomeClass"
Funktionen: "Snake Case" --> "some_function"
Variablen: "Snake Case" --> "some_variable"

# Start on Windows locally

1. Install the required dependencies with pip.
1. Create the python venv in `vscode`.
1. Activate the python venv with: `./.venv/Scrips/activate.bat`
1. Create an empty `test.db` file in the source folder.
1. Initialize the database with: `python c:/dev/dogtraining/init_database.py --connection=sqlite+aiosqlite:///C:\\dev\\dogtraining\\test.db`
2. Start the server with: `python -m server --connection=sqlite+aiosqlite:///C:\\dev\\dogtraining\\test.db`