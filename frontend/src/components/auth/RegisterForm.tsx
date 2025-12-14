"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { useAuth } from "@/hooks/useAuth";

export function RegisterForm() {
  const { register, isRegistering, registerError } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      await register({ email, password, full_name: fullName || undefined });
      router.push("/login?registered=true");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {(error || registerError) && (
        <div className="rounded-md bg-red-50 p-4">
          <p className="text-sm text-red-700">
            {error || registerError?.message}
          </p>
        </div>
      )}

      <div>
        <label
          htmlFor="fullName"
          className="block text-sm font-medium text-gray-700"
        >
          Full name (optional)
        </label>
        <input
          id="fullName"
          name="fullName"
          type="text"
          autoComplete="name"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
        />
      </div>

      <div>
        <label
          htmlFor="email"
          className="block text-sm font-medium text-gray-700"
        >
          Email address
        </label>
        <input
          id="email"
          name="email"
          type="email"
          autoComplete="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
        />
      </div>

      <div>
        <label
          htmlFor="password"
          className="block text-sm font-medium text-gray-700"
        >
          Password
        </label>
        <input
          id="password"
          name="password"
          type="password"
          autoComplete="new-password"
          required
          minLength={8}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-indigo-500"
        />
        <p className="mt-1 text-xs text-gray-500">
          Minimum 8 characters
        </p>
      </div>

      <div>
        <button
          type="submit"
          disabled={isRegistering}
          className="flex w-full justify-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
        >
          {isRegistering ? "Creating account..." : "Create account"}
        </button>
      </div>

      <div className="text-center text-sm">
        <span className="text-gray-600">Already have an account? </span>
        <Link
          href="/login"
          className="font-medium text-indigo-600 hover:text-indigo-500"
        >
          Sign in
        </Link>
      </div>
    </form>
  );
}
