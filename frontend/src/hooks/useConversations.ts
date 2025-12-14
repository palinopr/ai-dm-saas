/**
 * Hook for fetching conversations with polling
 */

"use client";

import { useQuery } from "@tanstack/react-query";

import { getConversations } from "@/lib/conversations-api";
import type { PaginatedConversations } from "@/types";

interface UseConversationsOptions {
  page?: number;
  pageSize?: number;
  enabled?: boolean;
}

export function useConversations(options: UseConversationsOptions = {}) {
  const { page = 1, pageSize = 20, enabled = true } = options;

  const {
    data,
    isLoading,
    error,
    refetch,
    isFetching,
  } = useQuery<PaginatedConversations, Error>({
    queryKey: ["conversations", page, pageSize],
    queryFn: () => getConversations(page, pageSize),
    enabled,
    refetchInterval: 5000, // Poll every 5 seconds
    staleTime: 2000, // Consider data stale after 2 seconds
  });

  return {
    conversations: data?.items ?? [],
    meta: data?.meta,
    isLoading,
    isFetching,
    error,
    refetch,
  };
}
