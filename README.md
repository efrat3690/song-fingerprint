# System for identifying songs using acoustic fingerprinting

A system for identifying song fragments based on the principles of acoustic fingerprinting, combined with a React-based user interface and an API server in FastAPI.

## Main features
- Record an audio clip or upload a file.
- Analyze fingerprints and compare them against a database.
- Identify the song that matches the recording.
- Song management interface (add, update, delete).
- Display results sorted by level of reliability.

## Technologies used
- FastAPI – API server in Python.
- React – interactive user interface.
- MongoDB – database for storing fingerprints.
- Uvicorn – running the API server.
- Python – processing and analyzing audio and finding matches.

## Local execution

### Activating the database
- Loading data into a database called **AcosticFingerprint** for collections called `songs`, `fingerprints`, `admin`.
- Running Mongo on `mongodb://localhost:27017`.
- Of course, you can change and adapt to your names.

### Running the server
- Installing the dependencies with the following command:
  ```bash
  pip install -r requirements.txt
  ```
- Running the server with the following command:
  ```bash
  uvicorn main:app --reload
  ```

### Running the Frontend
- Installing the dependencies if necessary with the following command:
  ```bash
  npm install
  ```
- Running with the following command:
  ```bash
  npm start
  ```

### Administration password
- Setting the desired password in the `plain_password` variable in the `database.password` file.
- Running the file with the following command:
  ```bash
  python database.password.py
  ```
- Saving the desired username and password encoded in a database in the `admin` collection.

---

**notebook**  
**efrat sharet**
