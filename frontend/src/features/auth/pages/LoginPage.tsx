import { useAuth } from "../hooks/useAuth";
import { LoginForm } from "../components/LoginForm";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const { signIn } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (email: string, password: string) => {
    await signIn(email, password);

    navigate("/dashboard", { replace: true });
  };

  return <LoginForm onLogin={handleLogin} />;
}