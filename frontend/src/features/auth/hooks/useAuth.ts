import { useState } from "react";
import { login } from "../api";

const TOKEN_KEY = "access_token";

export function useAuth() {
  const [token, setToken] = useState<string | null>(() =>
    localStorage.getItem(TOKEN_KEY)
  );
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleLogin(email: string, password: string) {
    setLoading(true);
    setError(null);
    try {
      const res = await login({ email, password });
      localStorage.setItem(TOKEN_KEY, res.access_token);
      setToken(res.access_token);
    } catch (e) {
      setError(e instanceof Error ? e.message : "An unexpected error occurred during login. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  function handleLogout() {
    localStorage.removeItem(TOKEN_KEY);
    setToken(null);
  }

  return { token, error, loading, handleLogin, handleLogout };
}
