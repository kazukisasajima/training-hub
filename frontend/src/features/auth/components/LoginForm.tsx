import { useState, type FormEvent } from "react";

type Props = {
  onLogin: (email: string, password: string) => void;
  error: string | null;
  loading: boolean;
};

export default function LoginForm({ onLogin, error, loading }: Props) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    onLogin(email, password);
  }

  return (
    <div style={{ maxWidth: 360, margin: "80px auto", padding: 24, border: "1px solid #ddd", borderRadius: 8 }}>
      <h2>ログイン</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 12 }}>
          <label htmlFor="email">メールアドレス</label>
          <br />
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ width: "100%", padding: 8, marginTop: 4, boxSizing: "border-box" }}
          />
        </div>
        <div style={{ marginBottom: 16 }}>
          <label htmlFor="password">パスワード</label>
          <br />
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ width: "100%", padding: 8, marginTop: 4, boxSizing: "border-box" }}
          />
        </div>
        {error && <p style={{ color: "red", marginBottom: 8 }}>{error}</p>}
        <button type="submit" disabled={loading} style={{ width: "100%", padding: 10 }}>
          {loading ? "ログイン中..." : "ログイン"}
        </button>
      </form>
    </div>
  );
}
