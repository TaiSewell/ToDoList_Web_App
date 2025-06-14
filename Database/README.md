# ToDoList Database Microservice

This microservice is responsible for managing the application's relational database using **MySQL**. It is containerized with Docker and connects to other services such as the API.

---

## 📦 Technologies

- MySQL 8+
- Docker
- Docker Compose

---

## 🚀 Getting Started

## 🧾 Environment Variables

This service uses a `.env` file to configure database credentials and settings.

Since the actual `.env` file is not included (for security reasons), you must create one in the root directory based on the `.env.example` file:

### 1. Create a `.env` file

Copy the example file:

```bash
cp .env.example .env
```
### 2. Edit .env with your values
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=todolist_db
MYSQL_USER=your_user
MYSQL_PASSWORD=your_user_password

Make sure your .env file is in the same directory as your Dockerfile or docker-compose.yml.

---

### 1. Build and Start the Database Container

Make sure Docker is installed and containers are built, then run:

To start container if it's already built:

```bash
docker-compose start mysql-container
```

---

### 2. Connect to the Database

Connect to Database:

```bash
docker exec -it mysql-container bash
```
Login:

```bash
mysql -u root -p
```
Enter the password defined in your environment or docker-compose.yml (e.g., rootpassword).

Explore the Database:

```MySQL
SHOW DATABASES;
USE your_database_name;
SHOW TABLES;
```

---

### 🗃️ Database Schema
The database includes the following tables:

users – Stores user account information

tasks – Stores to-do list items linked to users

---

### 🧹 Shut Down and Clean Up

To exit the container:

```bash
exit
```

To stop the container:

```bash
docker-compose stop mysql-container
```
