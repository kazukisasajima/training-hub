import { apiGet, apiPostJson } from "../../../shared/api/client";

export type MeResponse = { id: number; email: string };

export async function login(email: string, password: string) {
  return apiPostJson<{ ok: boolean }>("/api/auth/login", { email, password });
}

export async function me() {
  return apiGet<MeResponse>("/api/auth/me");
}

export async function logout() {
  return apiPostJson<{ ok: boolean }>("/api/auth/logout", {});
}