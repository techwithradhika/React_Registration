# Registration React Application

This is a simple registration application built using FastAPI for the backend, React for the frontend and MySQL for the database.

## Features

- Allows users to register with their name, email, and date of birth.
- Validates the date of birth format and emal on the frontend and backend.
- Provides API endpoints for performing CRUD operations on user registration data.

## Technologies Used

- **Backend**:
  - FastAPI
  - SQLAlchemy
  - MySQL

- **Frontend**:
  - React
  - Axios
 
## Project Structure

The project is structured into two main folders:

- **Backend**:
  - Contains the FastAPI application for handling registration logic.
  - Uses SQLAlchemy to interact with a MySQL database.
  - Utilizes Pydantic for request and response validation.

- **Frontend**:
  - Contains the React application for the user interface.
  - Allows users to fill out a registration form with name, email, and date of birth.
  - Sends registration data to the backend API for processing.

## Installation and Setup

1. **Database Setup**:
   - Download the Xammp for MySQL database, and start both apach and mysql services.
   - Navigate to the "backend" folder.
   - In terminal install virtual environment using "pip install virtualenv".
   - Create new virtual environment using "python -m virtualenv venv".
   - Activate the VENV using ".\venv\Scripts\activate".
   - Install dependencies using "pip install -r requirements.txt".
   - Run the sql_db python file using "python sql_db.py", which will create the Registration Database and Register table in MySQL.

2. **Backend Setup**:
   - Navigate to the "backend" folder. We have already installed all the dependencies for the backed using "pip install -r requirements.txt".
   - Start the FastAPI server in terminal using "uvicorn api:app --reload".

3. **Frontend Setup**:3
   - Navigate to the "frontend" folder.
   - Install dependencies using "npm install".
   - Start the React development server using "npm start", which will open the react frontend application in your browse.
   - now you perform all the usage mentioned below .

## Usage

1. Access the frontend application by opening the URL displayed after starting the React development server.
2. Fill out the registration form with valid information.
3. Submit the form to register a new user.
4. View, update, or delete registered users data at API endpoints in "http://127.0.0.1:8000/docs" after starting uvicorn server.