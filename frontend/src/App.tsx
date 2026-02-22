import { useEffect, useState } from "react";
import { apiGet } from "./shared/api/client";
import { useAuth } from "./features/auth/hooks/useAuth";
import LoginForm from "./features/auth/components/LoginForm";

type Health = { status: string };

export default function App() {
  const { token, error, loading, handleLogin, handleLogout } = useAuth();
  const [data, setData] = useState<Health | null>(null);
  const [healthErr, setHealthErr] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    apiGet<Health>("/api/health", token)
      .then(setData)
      .catch((e) => setHealthErr(e.message));
  }, [token]);

  if (!token) {
    return <LoginForm onLogin={handleLogin} error={error} loading={loading} />;
  }

  return (
    <div style={{ padding: 16 }}>
      <h1>training-hub</h1>
      <button onClick={handleLogout}>ログアウト</button>
      {healthErr && <pre>{healthErr}</pre>}
      {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : <p>loading...</p>}
    </div>
  );
}
