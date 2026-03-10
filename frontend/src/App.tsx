import { useAuth } from "./features/auth/hooks/useAuth";
import { LoginForm } from "./features/auth/components/LoginForm";

export default function App() {
  const { user, loading, signIn, signOut } = useAuth();

  if (loading) return <p style={{ padding: 16 }}>loading...</p>;

  if (!user) {
    return <LoginForm onLogin={signIn} />;
  }

  return (
    <div style={{ padding: 16 }}>
      <h1>training-hub</h1>
      <p>Logged in as: {user.email}</p>
      <button onClick={signOut}>Logout</button>

      {/* ここに workouts 画面など */}
    </div>
  );
}
