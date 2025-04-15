import React from "react";
import { useNavigate } from "react-router-dom";

function Dashboard() {
    const navigate = useNavigate();


    /*******************************************************
      Function: handleLogout
      Description: Logs the user out by removing the authentication 
      token from localStorage and redirects them to the login page.
     *******************************************************/
    const handleLogout = () => {
        localStorage.removeItem("token"); // Remove the token from local storage
        navigate("/login"); // Redirect to the login page
    }

    /*******************************************************
      Function: handleDeleteAccount
      Description: Deletes the user's account by sending a DELETE 
      request to the backend API. If successful, logs the user out 
      and redirects them to the registration page.
     *******************************************************/
    const handleDeleteAccount = async () => {
        const token = localStorage.getItem("token"); // Get the token from local storage
        if (!token) {
            alert("You need to be logged in to delete your account.");
            return;
        }
        
        const confirmDelete = window.confirm("Are you sure you want to delete your account? This action cannot be undone.");
        if (!confirmDelete) {
            return; // User canceled the deletion
        }
        try {
            const response = await fetch("http://localhost:8000/users/me", {
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            if (response.ok) {
                alert("Your account has been deleted successfully.");
                localStorage.removeItem("token"); // Remove the token
                navigate("/register"); // Redirect to the registration page
            } else {
                const errorData = await response.json();
                alert(errorData.detail || "Failed to delete account.");
            }
        } catch (error) {
            console.error("Error deleting account:", error);
            alert("An error occurred. Please try again.");
        }
    };

    return (
        <div>
            <h1>Dashboard</h1>
            <p>Welcome to your dashboard!</p>
            <button onClick={handleLogout}>Logout</button>
            <button onClick={handleDeleteAccount}>Delete Account</button>
        </div>
    );
}

export default Dashboard;