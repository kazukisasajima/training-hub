import { createBrowserRouter } from "react-router-dom";
import WorkoutCreatePage from "../features/workouts/pages/WorkoutCreatePage";
import LoginPage from "../features/auth/pages/LoginPage";
import WorkoutsPage from "../features/workouts/pages/WorkoutsPage";
import Dashboard from "../shared/pages/Dashboard";
import ProtectedRoute from "../features/auth/components/ProtectedRoute";

export const router = createBrowserRouter([
  { path: "/", element: <WorkoutsPage /> },
  { path: "login", element: <LoginPage /> },

  // 認証が必要なページ
  {
    element: <ProtectedRoute />, 
    children: [
      { path: "workouts", element: <WorkoutsPage /> },
      { path: "workouts/new", element: <WorkoutCreatePage /> },
      { path: "dashboard", element: <Dashboard /> },
    ],
  },
]);