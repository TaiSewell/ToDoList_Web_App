import React from "react";
import { Link } from "react-router-dom";

function Home() {
    return (
        <div>
            <h1>Home Page</h1>
            <p>Welcome to my home page</p>
            <nav> 
                <ul>
                    <li><Link href="/">Home</Link></li>
                    <li><Link href="/Login">Login</Link></li>
                </ul>
            </nav>
        </div>
    );
}

export default Home;