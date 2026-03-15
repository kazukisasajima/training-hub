import { useState } from "react";

export function LoginForm(props: { onLogin: (email: string, password: string) => Promise<void> }) {
  const [email, setEmail] = useState("test@example.com");
  const [password, setPassword] = useState("password");
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setErr(null);
    setLoading(true);

    try {
      await props.onLogin(email, password);
    } catch (e: any) {
      setErr(e?.message ?? "login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">

      <div className="w-full max-w-md bg-white rounded-lg shadow-md p-8">

        <h2 className="text-2xl font-bold text-center mb-6">
          Login
        </h2>

        {err && (
          <div className="mb-4 text-sm text-red-600 bg-red-100 p-2 rounded">
            {err}
          </div>
        )}

        <div className="space-y-4">

          <input
            className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-blue-200"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="email"
          />

          <input
            className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-blue-200"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="password"
            type="password"
          />

          <button
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition disabled:opacity-50"
            disabled={loading}
            onClick={handleSubmit}
          >
            {loading ? "Loading..." : "Login"}
          </button>

        </div>
      </div>

    </div>
  );
}