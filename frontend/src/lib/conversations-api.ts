/**
 * Conversations API functions
 */

import { api } from "./api";
import type {
  Conversation,
  ConversationDetail,
  ConversationStatus,
  ConversationStatusUpdate,
  PaginatedConversations,
  PaginatedMessages,
} from "@/types";

export async function getConversations(
  page: number = 1,
  pageSize: number = 20
): Promise<PaginatedConversations> {
  return api.get<PaginatedConversations>(
    `/api/conversations?page=${page}&page_size=${pageSize}`
  );
}

export async function getConversation(
  conversationId: string
): Promise<ConversationDetail> {
  return api.get<ConversationDetail>(`/api/conversations/${conversationId}`);
}

export async function getMessages(
  conversationId: string,
  page: number = 1,
  pageSize: number = 50
): Promise<PaginatedMessages> {
  return api.get<PaginatedMessages>(
    `/api/conversations/${conversationId}/messages?page=${page}&page_size=${pageSize}`
  );
}

export async function updateConversationStatus(
  conversationId: string,
  status: ConversationStatus
): Promise<Conversation> {
  const body: ConversationStatusUpdate = { status };
  return api.patch<Conversation>(
    `/api/conversations/${conversationId}/status`,
    body
  );
}

export async function markConversationAsRead(
  conversationId: string
): Promise<Conversation> {
  return api.post<Conversation>(
    `/api/conversations/${conversationId}/read`,
    {}
  );
}
