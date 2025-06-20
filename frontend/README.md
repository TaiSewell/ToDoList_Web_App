## 🖥️ Frontend Microservice – ToDoList Web App
This is the frontend microservice for the ToDoList Web App, built with React and containerized with Docker. The application is served in production using Nginx and tested using Jest and React Testing Library.

---

## 🧰 Tech Stack
The frontend of the ToDoList Web App is built using the following technologies:

JavaScript (ES6+) – Core programming language used for the React application.

React – Frontend library for building dynamic and interactive user interfaces.

React Router DOM – Manages client-side routing, including protected routes.

React Hooks – Utilized for state management and lifecycle methods (e.g., useState, useEffect).

CSS Modules – Scoped component styling using individual .css files.

Jest – JavaScript testing framework used for unit and integration tests.

React Testing Library – Provides utilities to test React components in a user-centric way.

Create React App – Development environment and build setup provided by CRA.

dotenv (REACT_APP_*) – Used to manage environment variables for API URLs and other configs.

Docker – Containerizes the frontend for consistent builds and deployments.

Nginx – Serves the built React app as a static site in production.

---

## 📁 Project Structure
```txt
frontend/
├── build/                  # Production build output
├── node_modules/           # Installed dependencies
├── public/                 # Static public files (e.g., index.html)
├── src/
│   ├── components/         # Reusable UI components
│   │   └── TaskItem.js
│   ├── pages/              # Page-level components and styling
│   │   ├── Dashboard.js / Dashboard.css
│   │   ├── Home.js / Home.css
│   │   ├── Login.js / Login.css
│   │   ├── Register.js / Register.css
│   │   └── NotFound.js / PrivateRoute.js
│   ├── tests/              # Component and route test files
│   │   ├── Dashboard.test.js
│   │   ├── Login.test.js
│   │   ├── router.test.js
│   │   └── TaskItem.test.js
│   ├── App.js / App.css / App.test.js
│   ├── index.js / index.css
│   ├── reportWebVitals.js
│   └── setupTests.js
├── Dockerfile              # Multi-stage Dockerfile for production build 
├── .gitignore
├── .eslintrc.json
├── package.json
├── package-lock.json
└── README.md
```

---

## 🚀 1. Getting Started
Prerequisites
- Node.js

- Docker

- npm

---

## 🐳 2. Running in Docker
Your frontend is containerized and served via Nginx after a production build.

With Docker Compose
If you're using Compose:

```bash
docker-compose up --build -d
```

Standalone Docker (Manual)

```bash
docker build -t frontend .
docker run -p 3000:80 --name frontend-container frontend
```
Then visit:

```txt
http://localhost:3000
```

---

## 🧪 3. Running Tests
Frontend tests use Jest and React Testing Library.

To run tests locally:

```bash
cd frontend
npm install
npm test
```

Tests are located in:

```txt
src/tests/
```

---

## 🔒 4. Authentication
JWT token is stored in localStorage

Sent with Authorization: Bearer <token> in all API requests

Protected routes use PrivateRoute.js to block unauthenticated access

---

## 📦 5. Production Build & Nginx Serve (Handled in Dockerfile)
Your Dockerfile performs the following:

- Builds the React app: npm run build

- Copies the static build to Nginx directory

- Runs Nginx to serve the app on port 80

- No manual steps needed post-docker-compose up.

---

## Linting
This project uses ESLint to enforce code quality and consistency.

Make sure you are in frontend directory:

```bash
cd frontend
```

📌 Run Lint Check

```bash
npm run lint
```

🛠️ Auto-fix Lint Errors

```bash
npm run lint:fix
```
These scripts check the src/ directory using the rules defined in .eslintrc.json.

ESLint is configured to check for things like unused variables, missing PropTypes, and bad syntax. Fixing these ensures a cleaner and more reliable codebase.

## Accessing The Frontend Container

✅ Step 1: Start the API container

To start container if it's already built:

```bash
docker-compose start <frontend-container-name>
```

---

🐳 Step 2: Access the API container
Run the following command to enter the API container:

```bash
docker exec -it <frontend-container-name> sh
```

---

### 🧹 Shut Down and Clean Up

To exit the container:

```bash
exit
```

To stop the container:

```bash
docker-compose stop <frontend-container-name>
```
