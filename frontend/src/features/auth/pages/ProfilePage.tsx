import { useState } from "react";
import type { FormEvent } from "react";
import Header from "../../../shared/components/layout/Header";
import Footer from "../../../shared/components/layout/Footer";
import { useAuth } from "../hooks/useAuth";
import { updateProfile } from "../api/api";

export default function ProfilePage() {
  const { user, refresh } = useAuth();

  const [name, setName] = useState(user?.name ?? "");
  const [email, setEmail] = useState(user?.email ?? "");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setMessage(null);
    setError(null);
    setLoading(true);

    try {
      await updateProfile({
        name,
        email,
        ...(password ? { password } : {}),
      });
      await refresh();
      setPassword("");
      setMessage("プロフィールを更新しました。");
    } catch (err) {
      setError(err instanceof Error ? err.message : "更新に失敗しました。");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <Header />

      <main className="flex-grow flex justify-center px-4 py-10">
        <div className="w-full max-w-xl bg-white rounded-lg shadow-md p-8">
          <h2 className="text-2xl font-bold mb-6">プロフィール編集</h2>

          {message && <p className="mb-4 text-green-700 bg-green-100 p-3 rounded">{message}</p>}
          {error && <p className="mb-4 text-red-700 bg-red-100 p-3 rounded">{error}</p>}

          <form className="space-y-4" onSubmit={handleSubmit}>
            <div>
              <label className="block text-sm font-medium mb-1">名前</label>
              <input
                className="w-full border border-gray-300 rounded px-3 py-2"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">メールアドレス</label>
              <input
                className="w-full border border-gray-300 rounded px-3 py-2"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">新しいパスワード（任意）</label>
              <input
                className="w-full border border-gray-300 rounded px-3 py-2"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="変更しない場合は空欄"
                minLength={8}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? "更新中..." : "保存する"}
            </button>
          </form>
        </div>
      </main>

      <Footer />
    </div>
  );
}