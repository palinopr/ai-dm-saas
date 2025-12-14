/**
 * Authentication hook using React Query
 */

"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useCallback, useEffect } from "react";

import {
  getCurrentUser,
  getStoredToken,
  login,
  logout as logoutFn,
  register,
} from "@/lib/auth";
import type { LoginRequest, RegisterRequest, User } from "@/types";

export function useAuth() {
  const queryClient = useQueryClient();
  const router = useRouter();

  const {
    data: user,
    isLoading,
    error,
    refetch,
  } = useQuery<User, Error>({
    queryKey: ["currentUser"],
    queryFn: getCurrentUser,
    enabled: !!getStoredToken(),
    retry: false,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  const loginMutation = useMutation({
    mutationFn: login,
    onSuccess: () => {
      refetch();
      router.push("/dashboard");
    },
  });

  const registerMutation = useMutation({
    mutationFn: register,
  });

  const logout = useCallback(() => {
    logoutFn();
    queryClient.setQueryData(["currentUser"], null);
    queryClient.invalidateQueries({ queryKey: ["currentUser"] });
    router.push("/login");
  }, [queryClient, router]);

  // Check for token on mount
  useEffect(() => {
    const token = getStoredToken();
    if (token && !user && !isLoading) {
      refetch();
    }
  }, [user, isLoading, refetch]);

  return {
    user,
    isLoading,
    isAuthenticated: !!user,
    error,
    login: (data: LoginRequest) => loginMutation.mutateAsync(data),
    loginError: loginMutation.error,
    isLoggingIn: loginMutation.isPending,
    register: (data: RegisterRequest) => registerMutation.mutateAsync(data),
    registerError: registerMutation.error,
    isRegistering: registerMutation.isPending,
    logout,
  };
}
