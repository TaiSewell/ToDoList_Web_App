import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "./Register.css";

/*******************************************************
Function: Register()
Description: This function handles the user registration process.
It includes a form for the user to input their username and password.
*******************************************************/
function Register() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch("http://localhost:8000/users/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username,
                    password,
                }),
            });

            if (response.ok) {
                const data = await response.json();
                alert(`User registered successfully! Welcome, ${data.username || username}`);
                navigate("/login");
            } else {
                const errorData = await response.json();
                alert(errorData.detail || "Registration failed!");
            }
        } catch (error) {
            console.error("Registration failed:", error);
            alert("An error occurred. Please try again.");
        }
    };

    return (
        <div className="register-container">
            <Link to="/" className="home-link">← Home</Link>
            <h1 className="register-title">Create Account</h1>
            <form className="register-form" onSubmit={handleRegister}>
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
                <button type="submit">Register</button>
            </form>
        </div>
    );
}

export default Register;