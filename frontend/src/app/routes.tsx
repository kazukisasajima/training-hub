import { createBrowserRouter } from "react-router-dom";
import WorkoutCreatePage from "../features/workouts/pages/WorkoutCreatePage";
import LoginPage from "../features/auth/pages/LoginPage";
import WorkoutsPage from "../features/workouts/pages/WorkoutsPage";
import Dashboard from "../shared/pages/Dashboard";
import ProtectedRoute from "../features/auth/components/ProtectedRoute";
import SignupPage from "../features/auth/pages/SignupPage";

export const router = createBrowserRouter([
  { path: "/login", element: <LoginPage /> },
  { path: "/signup", element: <SignupPage /> },
  
  // 認証が必要なページ
  {
    element: <ProtectedRoute />, 
    children: [
      { path: "/", element: <WorkoutsPage /> },
      { path: "/workouts", element: <WorkoutsPage /> },
      { path: "/workouts/new", element: <WorkoutCreatePage /> },
      { path: "/dashboard", element: <Dashboard /> },
    ],
  },
]);