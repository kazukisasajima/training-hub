import { LoginForm } from "../components/LoginForm";
import { useAuth } from "../hooks/useAuth";
import { Navigate } from "react-router-dom";

export default function LoginPage() {
  const { user, loading, signIn } = useAuth();

  if (loading) return <p>loading...</p>;
  if (user) return <Navigate to="/dashboard" replace />;

  return <LoginForm onLogin={signIn} />;
}