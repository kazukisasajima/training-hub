import { useEffect, useState } from "react";
import { apiGet } from "./shared/api/client";

type Health = { status: string };

export default function App() {
  const [data, setData] = useState<Health | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    apiGet<Health>("/api/health")
      .then(setData)
      .catch((e) => setErr(e.message));
  }, []);

  return (
    <div style={{ padding: 16 }}>
      <h1>training-hub</h1>
      {err && <pre>{err}</pre>}
      {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : <p>loading...</p>}
    </div>
  );
}
