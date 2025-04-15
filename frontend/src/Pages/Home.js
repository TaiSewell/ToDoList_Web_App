import React from "react";
import { Link } from "react-router-dom";

/*******************************************************
Function: Home()
Description: This function displays the home page of the application.
It includes a welcome message and navigation links to the login page.
*******************************************************/
function Home() {
    return (
        <div>
            <h1>Home Page</h1>
            <p>Welcome to my home page</p>
            <nav> 
                <ul>
                    <li><Link href="/">Home</Link></li>
                    <li><Link href="/login">Login</Link></li>
                </ul>
            </nav>
        </div>
    );
}

export default Home;