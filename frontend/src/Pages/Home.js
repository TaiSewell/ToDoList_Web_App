import React from "react";
import { Link } from "react-router-dom";
import "./Home.css";

/*******************************************************
Function: Home()
Description: This function displays the home page of the application.
It includes a welcome message and navigation links to the login page.
*******************************************************/
function Home() {
    return (
        <div className="home-container">
            <h1 className="home-title">TaskTrackr</h1>
            <p className="home-welcome">TaskTrackr helps you stay organized by letting you create an account and 
                easily manage your daily tasks. Add, view, and take off items on your to-do list so you can stay 
                on top of what needs to get done anytime, anywhere.</p>
            <nav className="home-nav">
                <ul>
                    <li>
                        <Link to="/login" className="home-link">Login</Link>
                    </li>
                    <li>
                        <Link to="/register" className="home-link">Create Account</Link>
                    </li>
                </ul>
            </nav>
        </div>
    );
}

export default Home;