import { apiPostForm } from "../../shared/api/client";
import type { LoginRequest, TokenResponse } from "./types";

export async function login(credentials: LoginRequest): Promise<TokenResponse> {
  const form = new URLSearchParams();
  form.append("username", credentials.email);
  form.append("password", credentials.password);
  return apiPostForm<TokenResponse>("/api/auth/login", form);
}
