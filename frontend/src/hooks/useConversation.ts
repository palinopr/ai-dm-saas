/**
 * Hook for fetching a single conversation
 */

"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import {
  getConversation,
  updateConversationStatus,
} from "@/lib/conversations-api";
import type { ConversationDetail, ConversationStatus } from "@/types";

interface UseConversationOptions {
  enabled?: boolean;
}

export function useConversation(
  conversationId: string | null,
  options: UseConversationOptions = {}
) {
  const { enabled = true } = options;
  const queryClient = useQueryClient();

  const {
    data: conversation,
    isLoading,
    error,
    refetch,
  } = useQuery<ConversationDetail, Error>({
    queryKey: ["conversation", conversationId],
    queryFn: () => getConversation(conversationId!),
    enabled: enabled && !!conversationId,
    staleTime: 30000, // Consider data stale after 30 seconds
  });

  const updateStatusMutation = useMutation({
    mutationFn: (status: ConversationStatus) =>
      updateConversationStatus(conversationId!, status),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["conversation", conversationId] });
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
    },
  });

  return {
    conversation,
    isLoading,
    error,
    refetch,
    updateStatus: (status: ConversationStatus) =>
      updateStatusMutation.mutateAsync(status),
    isUpdatingStatus: updateStatusMutation.isPending,
  };
}
