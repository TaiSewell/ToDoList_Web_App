import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";

function Dashboard() {
    const navigate = useNavigate();
    const [tasks, setTasks] = useState([]);
    const [newTask, setNewTask] = useState("");
    const token = localStorage.getItem("token"); // Get the token from local storage
    
    const [editingTaskId, setEditingTaskId] = useState(null);
    const [editedTitle, setEditedTitle] = useState("");
    const [editedDescription, setEditedDescription] = useState("");
    const [editedCompleted, setEditedCompleted] = useState(false);
    const [accountDeleted, setAccountDeleted] = useState(false);

    /********************************************************
     * useEffect Hook
     * Description: Runs once when the component mounts. Checks if a
     * token exists in localStorage. If not found, alerts the user and
     * navigates them to the login page. If found, it calls fetchTasks
     * to load tasks.
    ********************************************************/
    useEffect(() => {
        if (!token || accountDeleted) return;
        fetchTasks();
    }, [token, accountDeleted]); // Dependency array includes token and navigate

    /********************************************************
     * Function: fetchTasks
     * Description: Fetches all tasks for the authenticated user using
     * the token stored in localStorage. Updates the local state with
     * the retrieved task data. Called on initial render and after task
     * updates, deletions, or additions.
    ********************************************************/
    const fetchTasks = async () => {
        //console.log("Authorization header:", `Bearer ${token}`); // Need to delete this line when pushing to prod

        try {
            const response = await fetch("http://localhost:8000/tasks/", {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            if (response.ok) {
                const data = await response.json();
                setTasks(data);
            } else {
                alert("Failed to load tasks.");
            }
        } catch (error) {
            console.error("Error fetching tasks:", error);
        }
    };

    /********************************************************
     * Function: handleAddTask
     * Description: Sends a POST request to the backend API to create
     * a new task using the value from the newTask state. If the task
     * is successfully added, clears the input field and refreshes the
     * task list by calling fetchTasks.
    ********************************************************/
    const handleAddTask = async () => {
        if (!newTask.trim()) return;

        try {
            const response = await fetch("http://localhost:8000/tasks/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ 
                    title: newTask,
                    description: "",
                    completed: false 
                 })
            });
            if (response.ok) {
                setNewTask("");
                fetchTasks(); // Refresh the task list
            } else {
                alert("Failed to add task.");
            }
        } catch (error) {
            console.error("Error adding task:", error);
        }
    };

    /********************************************************
     * Function: handleUpdateTask
     * Description: Sends a PUT request to update the title and
     * description of a specific task (identified by taskId) for the
     * authenticated user. On success, updates the local task list
     * and resets the editing state.
     * 
     * Parameters:
     *  - taskId (number): The ID of the task to update.
    ********************************************************/
    const handleUpdateTask = async (taskId) => {
        const token = localStorage.getItem("token"); // or your auth method
        try {
          const response = await fetch(`http://localhost:8000/tasks/${taskId}`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
              title: editedTitle,
              description: editedDescription,
              completed: editedCompleted,
            }),
          });
      
          if (!response.ok) {
            throw new Error("Failed to update task");
          }
      
          const updatedTask = await response.json();
      
          // Refresh tasks in state (e.g., re-fetch or update locally)
          setTasks((prevTasks) =>
            prevTasks.map((task) =>
              task.id === taskId ? updatedTask : task
            )
          );
      
          // Clear editing state
          setEditingTaskId(null);
          setEditedTitle("");
          setEditedDescription("");
          setEditedCompleted(false);
        } catch (err) {
          console.error(err);
          alert("Could not update task.");
        }
      };

    /********************************************************
     * Function: handleDeleteTask
     * Description: Sends a DELETE request to remove a task identified
     * by taskId from the backend for the authenticated user. If successful,
     * fetches and updates the task list to reflect the change.
     * 
     * Parameters:
     *  - taskId (number): The ID of the task to delete.
    ********************************************************/
    const handleDeleteTask = async (taskId) => {
        try {
            const response = await fetch(`http://localhost:8000/tasks/${taskId}`, {
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            if (response.ok) {
                fetchTasks(); // Refresh the list
            } else {
                alert("Failed to delete task.");
            }
        } catch (error) {
            console.error("Error deleting task:", error);
        }
    };
    



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
                localStorage.removeItem("token"); 
                setTasks([]);                      
                setAccountDeleted(true);          
                navigate("/register");           
            } else {
                const errorData = await response.json();
                alert(errorData.detail || "Failed to delete account.");
            }
        } catch (error) {
            console.error("Error deleting account:", error);
            alert("An error occurred. Please try again.");
        }
    };

    /*******************************************************
      Function: handleCheckboxToggle
      Description: handles the toggling of the checkbox for a task.
      It updates the task's completion status in the local state and
      sends a PUT request to the backend to update the task's status.
     *******************************************************/
    const handleCheckboxToggle = async (taskId, currentStatus) => {
    const updatedTasks = tasks.map((task) =>
        task.id === taskId ? { ...task, completed: !currentStatus } : task
    );
    setTasks(updatedTasks);

    try {
        await fetch(`http://localhost:8000/tasks/${taskId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ completed: !currentStatus }),
        });
    } catch (error) {
        console.error("Error updating completion status:", error);
    }
};

return (
    <div className="dashboard-container">
        <h1 className="dashboard-title">Dashboard</h1>
        <p className="dashboard-welcome">Welcome to your dashboard!</p>

        <div className="dashboard-input-group">
            <input
                type="text"
                placeholder="Add a new task"
                value={newTask}
                onChange={(e) => setNewTask(e.target.value)}
            />
            <button onClick={handleAddTask}>Add</button>
        </div>

        <ul className="dashboard-task-list">
            {tasks.map((task) => (
                <li key={task.id}>
                    {editingTaskId === task.id ? (
                        <>
                            <input
                                type="text"
                                value={editedTitle}
                                onChange={(e) => setEditedTitle(e.target.value)}
                                placeholder="Title"
                            />
                            <button onClick={() => handleUpdateTask(task.id)}>Save</button>
                            <button onClick={() => {
                                setEditingTaskId(null);
                                setEditedTitle("");
                                setEditedDescription("");
                                setEditedCompleted(false);
                            }}>Cancel</button>
                        </>
                    ) : (
                        <>
        <input
            type="checkbox"
            checked={task.completed}
            onChange={() => handleCheckboxToggle(task.id, task.completed)}
            style={{ marginRight: "10px" }}
          />
          <span style={{ textDecoration: task.completed ? "line-through" : "none" }}>
            {task.title}
          </span>
          <div className="dashboard-task-actions">
            <button
              onClick={() => {
                setEditingTaskId(task.id);
                setEditedTitle(task.title);
                setEditedDescription(task.description || "");
                setEditedCompleted(task.completed);
              }}
            >
              Edit
            </button>
            <button onClick={() => handleDeleteTask(task.id)}>Delete</button>
          </div>
        </>
      )}
    </li>
  ))}
</ul>

        <div className="dashboard-actions">
            <button onClick={handleLogout}>Logout</button>
            <button onClick={handleDeleteAccount}>Delete Account</button>
        </div>
    </div>
);
}

export default Dashboard;