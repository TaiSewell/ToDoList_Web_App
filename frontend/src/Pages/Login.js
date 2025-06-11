import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import "./Login.css";

/*******************************************************
Function: Login()
Description: This function handles the user login process.
*******************************************************/
function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch("http://localhost:8000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({
                    username,
                    password,
                }),
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem("token", data.access_token); // Store the token
                alert("Login successful!");
                navigate("/dashboard"); // Redirect to the dashboard
              } else {
                alert("Invalid username or password!");
              }
            } catch (error) {
              console.error("Login failed:", error);
              alert("Please Check for valid Username/Password.")
            } 
        }

return (
  <div className="login-container">
    <Link to="/" className="home-link">← Home</Link>
    <h2 className="login-title">Login</h2>
    <form className="login-form" onSubmit={handleLogin}>
      <label>
        Username:
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
      </label>
      <label>
        Password:
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </label>
      <button type="submit">Login</button>
    </form>
  </div>
);
}

export default Login;