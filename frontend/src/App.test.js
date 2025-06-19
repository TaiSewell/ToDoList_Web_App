import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders home page content", () => {
  render(<App />);
  const title = screen.getByRole("heading", { name: /TaskTrackr/i });
  expect(title).toBeInTheDocument();
});