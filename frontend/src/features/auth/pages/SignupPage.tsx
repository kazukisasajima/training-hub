import { useState } from "react";
import { useAuth } from "../hooks/useAuth";
import { signup } from "../api/api";
import { useNavigate } from "react-router-dom";

export default function SignupPage() {
  const { refresh } = useAuth();
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState<string | null>(null);

  const handleSignup = async () => {
    setErr(null);

    try {
      await signup(name, email, password);
      await refresh(); // user更新
      navigate("/dashboard", { replace: true });
    } catch (e: any) {
      setErr(e.message);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <div className="w-full max-w-md bg-white rounded shadow p-8">
        <h2 className="text-2xl font-bold mb-6 text-center">Sign Up</h2>

        {err && (
          <div className="mb-4 text-red-600 bg-red-100 p-2 rounded">
            {err}
          </div>
        )}

        <div className="space-y-4">
          <input
            className="w-full border px-3 py-2 rounded"
            placeholder="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

          <input
            className="w-full border px-3 py-2 rounded"
            placeholder="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <input
            className="w-full border px-3 py-2 rounded"
            type="password"
            placeholder="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button
            className="w-full bg-green-600 text-white py-2 rounded"
            onClick={handleSignup}
          >
            Sign Up
          </button>
        </div>
      </div>
    </div>
  );
}