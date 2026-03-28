import { apiGet, apiPostJson } from "../../../shared/api/client";

export type MeResponse = { id: number; email: string; name: string };

export async function login(email: string, password: string) {
  return apiPostJson<{ ok: boolean }>("/api/auth/login", { email, password });
}

export async function me() {
  return apiGet<MeResponse>("/api/auth/me");
}

export async function logout() {
  return apiPostJson<{ ok: boolean }>("/api/auth/logout", {});
}

export async function signup(name: string, email: string, password: string) {
  const res = await fetch("/api/auth/signup", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name, email, password }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text);
  }

  return res.json();
}