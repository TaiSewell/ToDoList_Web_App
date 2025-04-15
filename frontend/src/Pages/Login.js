import React, { useState } from "react";
import { useNavigate } from "react-router-dom";



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
            } 
        }

        return (
            <div>
              <h1>Login</h1>
              <form onSubmit={handleLogin}>
                <label>
                  Username:
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                  />
                </label>
                <br />
                <label>
                  Password:
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </label>
                <br />
                <button type="submit">Login</button>
              </form>
            </div>
          );
        }

export default Login;