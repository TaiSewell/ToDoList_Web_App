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
```text
ToDoList_Web_App/
├── API/
│ ├── src/
│ │ ├── app/
│ │ │ ├── main.py
│ │ │ ├── auth.py
│ │ │ ├── routes/
│ │ │ │ ├── tasks.py
│ │ │ │ └── users.py
│ │ └── tests/
│ │ └── test_main.py
│ ├── Dockerfile
│ └── requirements.txt
```
---

## 🧪 Running Tests
This project includes automated tests for the API using Pytest. These tests cover:

✅ User registration and login

❌ Login failure handling

🔐 Protected route access

📝 Task CRUD operations

🗑 Account deletion

To run the tests:

✅ Step 1: Start the API container

To start container if it's already built:

```bash
docker-compose start <api-container-name>
```

---

🐳 Step 2: Access the API container
Run the following command to enter the API container:

```bash
docker exec -it <api-container-name> bash
```

🧪 Step 3: Run the tests inside the container
Once you're inside the container, run:

```bash
pytest
```
This will execute all tests located in the src/tests/ directory.

If it is not picking up pytest for some reason:
- install pytest in the api-container

```bash
pip install pytest
```

---

## Linting
This project uses pylint to enforce code quality and consistency.

Make sure you are in API directory:

```bash
cd API
```

📌 Run Lint Check

```bash
pylint src/app/
```
### 🧹 Shut Down and Clean Up

To exit the container:

```bash
exit
```

To stop the container:

```bash
docker-compose stop <api-container-name>
```