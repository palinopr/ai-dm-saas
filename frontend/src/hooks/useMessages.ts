/**
 * Hook for fetching messages with polling and auto-mark-as-read
 */

"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useEffect, useRef } from "react";

import { getMessages, markConversationAsRead } from "@/lib/conversations-api";
import type { PaginatedMessages } from "@/types";

interface UseMessagesOptions {
  page?: number;
  pageSize?: number;
  enabled?: boolean;
  autoMarkAsRead?: boolean;
}

export function useMessages(
  conversationId: string | null,
  options: UseMessagesOptions = {}
) {
  const {
    page = 1,
    pageSize = 50,
    enabled = true,
    autoMarkAsRead = true,
  } = options;

  const queryClient = useQueryClient();
  const hasMarkedAsRead = useRef(false);

  const {
    data,
    isLoading,
    error,
    refetch,
    isFetching,
  } = useQuery<PaginatedMessages, Error>({
    queryKey: ["messages", conversationId, page, pageSize],
    queryFn: () => getMessages(conversationId!, page, pageSize),
    enabled: enabled && !!conversationId,
    refetchInterval: 5000, // Poll every 5 seconds
    staleTime: 2000, // Consider data stale after 2 seconds
  });

  const markAsReadMutation = useMutation({
    mutationFn: () => markConversationAsRead(conversationId!),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
      queryClient.invalidateQueries({ queryKey: ["conversation", conversationId] });
    },
  });

  // Auto mark as read when messages are loaded
  useEffect(() => {
    if (
      autoMarkAsRead &&
      conversationId &&
      data?.items?.length &&
      !hasMarkedAsRead.current
    ) {
      hasMarkedAsRead.current = true;
      markAsReadMutation.mutate();
    }
  }, [conversationId, data?.items?.length, autoMarkAsRead]);

  // Reset the read flag when conversation changes
  useEffect(() => {
    hasMarkedAsRead.current = false;
  }, [conversationId]);

  return {
    messages: data?.items ?? [],
    meta: data?.meta,
    isLoading,
    isFetching,
    error,
    refetch,
    markAsRead: () => markAsReadMutation.mutateAsync(),
    isMarkingAsRead: markAsReadMutation.isPending,
  };
}
