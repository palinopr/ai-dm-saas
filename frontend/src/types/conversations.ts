/**
 * Conversation types for Instagram DM management
 */

export type ConversationStatus = "active" | "archived" | "closed";
export type MessageDirection = "inbound" | "outbound";
export type MessageType = "text" | "image" | "video" | "audio" | "sticker";

export interface InstagramUser {
  id: string;
  instagram_user_id: string;
  username: string | null;
  name: string | null;
  profile_picture_url: string | null;
}

export interface Message {
  id: string;
  conversation_id: string;
  instagram_message_id: string | null;
  direction: MessageDirection;
  message_type: MessageType;
  content: string;
  intent: string | null;
  confidence: number | null;
  is_ai_generated: boolean;
  instagram_timestamp: string | null;
  created_at: string;
}

export interface Conversation {
  id: string;
  instagram_account_id: string;
  status: ConversationStatus;
  last_message_at: string | null;
  unread_count: number;
  created_at: string;
  updated_at: string;
  instagram_user: InstagramUser;
  last_message_preview: string | null;
}

export interface ConversationDetail {
  id: string;
  instagram_account_id: string;
  status: ConversationStatus;
  last_message_at: string | null;
  unread_count: number;
  created_at: string;
  updated_at: string;
  instagram_user: InstagramUser;
}

export interface PaginationMeta {
  total: number;
  page: number;
  page_size: number;
  has_next: boolean;
  has_previous: boolean;
}

export interface PaginatedConversations {
  items: Conversation[];
  meta: PaginationMeta;
}

export interface PaginatedMessages {
  items: Message[];
  meta: PaginationMeta;
}

export interface ConversationStatusUpdate {
  status: ConversationStatus;
}
