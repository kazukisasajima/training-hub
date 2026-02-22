export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(path, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error: ${res.status} ${text}`);
  }
  return (await res.json()) as T;
}
