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

# Authentication

## Keycloak
Use [Keycloak](https://www.keycloak.org/) as Authentication manager behind a [reverse proxy](https://www.keycloak.org/server/reverseproxy) and return the user_id == username and the user roles.


# Setup at Home 

## Kubernetes
1.   Hardware Requirements

https://platform9.com/docs/kubernetes/kubernetes-cluster-pre-requisites
16GB RAM
60GB Speicherplatz mindestens 40GB frei

1.  Setup
     
https://youtu.be/_WW16Sp8-Jw?si=xxPXsJJu6fjkb6zd

 