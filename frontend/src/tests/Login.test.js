import { render, screen, fireEvent } from "@testing-library/react";
import Login from "../pages/Login"; // adjust import path
import { BrowserRouter } from "react-router-dom";

test("renders login form", () => {
  render(
    <BrowserRouter>
      <Login />
    </BrowserRouter>
  );

  const username = screen.getByLabelText(/username/i);
  const password = screen.getByLabelText(/password/i);
  const button = screen.getByRole("button", { name: /login/i });

  expect(username).toBeInTheDocument();
  expect(password).toBeInTheDocument();
  expect(button).toBeInTheDocument();
});