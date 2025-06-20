# 📝 ToDoList_Web_App

This is my full-stack To-Do List web application built using **FastAPI (backend)**, **MySQL (database)**, and **JavaScript (frontend)**. The app is containerized with Docker and managed with `docker-compose`.

---

## 📁 Project Structure
```txt
ToDoList_Web_App/
├── API/ # Backend code (FastAPI)
├── Database/ # MySQL database setup
├── frontend/ # Frontend files (HTML/CSS/JavaScript)
├── .env # Environment variables
├── docker-compose.yml # Multi-container Docker config
└── README.md # This file
```
---

## 📦 Tech Stack
Backend: FastAPI, SQLAlchemy, JWT Auth

Database: MySQL

Frontend: JavaScript, HTML/CSS

DevOps: Docker, Docker Compose

---

## 🚀 Getting Started

### ✅ Step 1: Install all required softwares

Required Software
- Python (3.10+)

Required for the FastAPI backend

- Node.js & npm

Required to run and build the React frontend

- Docker & Docker Compose

Required for containerizing and running the full app (frontend, backend, database)

MySQL Workbench (Optional)

- GUI for viewing and managing the MySQL database

Git

- For cloning the project and managing source code

Visual Studio Code

- Recommended IDE for writing and managing code

⚙️ Optional but Useful Tools
- Postman – For testing API endpoints manually
https://www.postman.com/

- Docker VS Code Extension – Helps visualize and manage containers inside VS Code

### ✅ Step 2: Create venv (Virtual Environment)

Create your own venv inside the root directory to help with all backend dependencies

🐍 For Windows (Command Prompt or PowerShell):

```bash
python -m venv venv
```

### ✅ Step 3: Check each microservice's directory for the README.md files

- Read the files and setup each microservice's properly

### ✅ Step 4: Start the Docker containers

From the root of your project (where `docker-compose.yml` is located), run:

```bash
docker-compose up --build -d
```
This will:

Build the API container

Start the MySQL database

Serve the frontend (if configured)

If the api-container is giving an error saying "connection refused or couldn't connect to database":
    - Go to docker-compose.yml file in root 
    - Adjust the interval time on the database service
    - Interval range to mess around with 5-15 seconds
    - Should fix the issue

### ✅ Step 5: Shut Down & Clean Up

- Whenever you are done shutdown the containers

```bash
docker-compose down
```

Shut Down & Delete Data:
```bash
docker-compose down -v
```

---

## App Demo 

- Check out the App Demo Video Down Below

Watch the [app demo on YouTube](https://youtu.be/yWa3-FHXZug).