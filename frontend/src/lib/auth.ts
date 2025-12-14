/**
 * Authentication API functions
 */

import { api } from "./api";
import type { LoginRequest, RegisterRequest, TokenResponse, User } from "@/types";

const TOKEN_KEY = "auth_token";

export function getStoredToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function setStoredToken(token: string): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(TOKEN_KEY, token);
  api.setToken(token);
}

export function removeStoredToken(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem(TOKEN_KEY);
  api.setToken(null);
}

export async function login(data: LoginRequest): Promise<TokenResponse> {
  const formData = new URLSearchParams();
  formData.append("username", data.email);
  formData.append("password", data.password);

  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/auth/login`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData,
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Login failed");
  }

  const tokenData: TokenResponse = await response.json();
  setStoredToken(tokenData.access_token);
  return tokenData;
}

export async function register(data: RegisterRequest): Promise<User> {
  return api.post<User>("/auth/register", data);
}

export async function getCurrentUser(): Promise<User> {
  const token = getStoredToken();
  if (token) {
    api.setToken(token);
  }
  return api.get<User>("/auth/me");
}

export function logout(): void {
  removeStoredToken();
}
