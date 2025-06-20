import React from "react";

function TaskItem({ task, onDelete, onEdit }) {
  return (
    <div className="task-item">
      <h3>{task.title}</h3>
      <p>{task.description}</p>
      <button onClick={() => onEdit(task)}>Edit</button>
      <button onClick={() => onDelete(task.id)}>Delete</button>
    </div>
  );
}

export default TaskItem;