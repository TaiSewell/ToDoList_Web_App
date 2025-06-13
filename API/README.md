# ToDoList API Microservice

This is the **API microservice** for the ToDoList web application. It provides secure, authenticated endpoints for user registration, login, and task management (CRUD operations). Built with **FastAPI**, this service is containerized using **Docker** and communicates with other microservices in the app.

---

## 🚀 Features

- 🔐 User registration and login (JWT-based authentication)
- 📝 Create, read, update, and delete tasks
- 🔒 Protected endpoints requiring valid tokens
- 🧪 Unit tests for authentication and task operations

---

## 🛠 Tech Stack

- **FastAPI** – Web framework
- **SQLAlchemy** – ORM for database access
- **MySQL** – Backend relational database (in separate container)
- **Docker** – Containerization
- **Pytest** – Testing framework

---

## 📁 Project Structure
ToDoList_Web_App
├── API/
    ├── src/
    │ ├── app/
    │ │ ├── main.py
    | | ├── auth.py
    │ │ ├── routes/
    | | |     ├── tasks.py
    | | |     ├── users.py
    └── tests/
    │ └── test_main.py
    ├── Dockerfile
    └── requirements.txt

🧪 7. Running Tests
This project includes automated tests for the API using Pytest. These tests cover:

✅ User registration and login

❌ Login failure handling

🔐 Protected route access

📝 Task CRUD operations

🗑 Account deletion

To run the tests:

✅ Step 1: Start the Docker containers
From the root of your project (where docker-compose.yml is located), run:

docker-compose up --build -d
This will build the images and start all containers in detached mode.

🐳 Step 2: Access the API container
Run the following command to enter the API container:

docker exec -it api-container bash

🧪 Step 3: Run the tests inside the container
Once you're inside the container, run:

pytest
This will execute all tests located in the src/tests/ directory.