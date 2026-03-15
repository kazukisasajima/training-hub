import { useAuth } from "../../auth/hooks/useAuth";
import { Navigate } from "react-router-dom";

export default function WorkoutsPage() {
  const { user, loading } = useAuth();

  if (loading) return <p>loading...</p>;
  if (!user) return <Navigate to="/login" replace />;

  return (
    <div>
      <h1>Workouts</h1>
      <p>ここにワークアウト画面</p>
    </div>
  );
}