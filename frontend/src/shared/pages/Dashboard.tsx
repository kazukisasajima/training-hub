import { Navigate } from "react-router-dom";
import Header from "../components/layout/Header";
import Footer from "../components/layout/Footer";
import { useAuth } from "../../features/auth/hooks/useAuth";

const Dashboard = () => {
  const { user, loading } = useAuth();

  // TODO: useEffectでリフレッシュしないと状況によってはloadingが永遠に続く可能性がある
  // こっちでもリフレッシュするか、もしくはAuthProvider側でリフレッシュ失敗時にloadingをfalseにする必要がある
  // if (loading) return <p>loading...</p>;
  if (!user) return <Navigate to="/login" replace />;

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <main className="flex-grow flex flex-col items-center justify-center">
        <h2 className="text-3xl font-bold mb-6">ダッシュボード</h2>
        <p className="text-lg text-gray-700">
          ようこそ、<strong>{user.name}</strong> さん！
        </p>
      </main>

      <Footer />
    </div>
  );
};

export default Dashboard;