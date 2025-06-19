import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import Dashboard from "../pages/Dashboard"; // ✅ use this format

beforeEach(() => {
  localStorage.setItem("token", "fake-token");
});

afterEach(() => {
  localStorage.clear();
});

test("renders dashboard heading", () => {
  render(
    <BrowserRouter>
      <Dashboard />
    </BrowserRouter>
  );
  expect(screen.getByRole("heading", { name: /dashboard/i })).toBeInTheDocument();
});