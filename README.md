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

### ✅ Step 1: Create venv (Virtual Environment)

Create your own venv inside the root directory to help with all backend dependencies

### ✅ Step 2: Start the Docker containers

From the root of your project (where `docker-compose.yml` is located), run:

```bash
docker-compose up --build -d
```
This will:

Build the API container

Start the MySQL database

Serve the frontend (if configured)

### ✅ Step 3: Check each microservice's directory for the README.md files

- Reading the files will demonstrate how to use each microservice

### ✅ Step 4: Shut Down & Clean Up

- Whenever you are done shutdown the containers

```bash
docker-compose down
```

Shut Down & Delete Data:
```bash
docker-compose down -v
```