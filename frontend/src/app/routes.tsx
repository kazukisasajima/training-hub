import { createBrowserRouter } from "react-router-dom";
import WorkoutCreatePage from "../features/workouts/pages/WorkoutCreatePage";
import LoginPage from "../features/auth/pages/LoginPage";
import WorkoutsPage from "../features/workouts/pages/WorkoutsPage";
import Dashboard from "../shared/pages/Dashboard";

export const router = createBrowserRouter([
  { path: "/", element: <WorkoutsPage /> },
  { path: "workouts", element: <WorkoutsPage /> },
  { path: "workouts/new", element: <WorkoutCreatePage /> },
  { path: "login", element: <LoginPage /> },
  { path: "dashboard", element: <Dashboard /> },
]);