import { useState } from "react";

export function LoginForm(props: { onLogin: (email: string, password: string) => Promise<void> }) {
  const [email, setEmail] = useState("test@example.com");
  const [password, setPassword] = useState("password");
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  return (
    <div style={{ padding: 16, maxWidth: 360 }}>
      <h2>Login</h2>
      {err && <pre>{err}</pre>}

      <div style={{ display: "grid", gap: 8 }}>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="email" />
        <input
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="password"
          type="password"
        />
        <button
          disabled={loading}
          onClick={async () => {
            setErr(null);
            setLoading(true);
            try {
              await props.onLogin(email, password);
            } catch (e: any) {
              setErr(e?.message ?? "login failed");
            } finally {
              setLoading(false);
            }
          }}
        >
          {loading ? "..." : "Login"}
        </button>
      </div>
    </div>
  );
}