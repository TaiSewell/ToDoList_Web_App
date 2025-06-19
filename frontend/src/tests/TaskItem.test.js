import { render, screen, fireEvent } from "@testing-library/react";
import TaskItem from "../components/TaskItem";

const mockTask = {
  id: 1,
  title: "Sample Task",
};

const mockOnDelete = jest.fn();
const mockOnEdit = jest.fn();

test("renders task info and handles button clicks", () => {
  render(
    <TaskItem
      task={mockTask}
      onDelete={mockOnDelete}
      onEdit={mockOnEdit}
    />
  );

  expect(screen.getByText(/sample task/i)).toBeInTheDocument();

  fireEvent.click(screen.getByText(/delete/i));
  expect(mockOnDelete).toHaveBeenCalled();

  fireEvent.click(screen.getByText(/edit/i));
  expect(mockOnEdit).toHaveBeenCalled();
});