"use client";

import { useState, useCallback } from "react";

import {
  ConversationList,
  ConversationDetail,
  EmptyState,
} from "@/components/conversations";
import { DashboardLayout } from "@/components/dashboard";
import { Input } from "@/components/ui/input";
import {
  useAuth,
  useConversations,
  useConversation,
  useMessages,
} from "@/hooks";
import { Search } from "lucide-react";

export default function DashboardPage() {
  const { user, logout } = useAuth();
  const [selectedConversationId, setSelectedConversationId] = useState<
    string | null
  >(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [showSidebar, setShowSidebar] = useState(true);

  // Fetch conversations
  const { conversations, isLoading: isLoadingConversations } =
    useConversations();

  // Fetch selected conversation details
  const {
    conversation,
    isLoading: isLoadingConversation,
    updateStatus,
  } = useConversation(selectedConversationId);

  // Fetch messages for selected conversation
  const { messages, isLoading: isLoadingMessages } =
    useMessages(selectedConversationId);

  // Filter conversations by search query
  const filteredConversations = conversations.filter((conv) => {
    if (!searchQuery) return true;
    const query = searchQuery.toLowerCase();
    const name = conv.instagram_user.name?.toLowerCase() || "";
    const username = conv.instagram_user.username?.toLowerCase() || "";
    const preview = conv.last_message_preview?.toLowerCase() || "";
    return (
      name.includes(query) ||
      username.includes(query) ||
      preview.includes(query)
    );
  });

  // Handle conversation selection
  const handleSelectConversation = useCallback((id: string) => {
    setSelectedConversationId(id);
    // Hide sidebar on mobile after selection
    setShowSidebar(false);
  }, []);

  // Handle back button (mobile)
  const handleBack = useCallback(() => {
    setSelectedConversationId(null);
    setShowSidebar(true);
  }, []);

  // Handle archive
  const handleArchive = useCallback(async () => {
    if (selectedConversationId) {
      await updateStatus("archived");
    }
  }, [selectedConversationId, updateStatus]);

  // Toggle sidebar
  const handleToggleSidebar = useCallback(() => {
    setShowSidebar((prev) => !prev);
  }, []);

  // Sidebar content
  const sidebarContent = (
    <div className="flex flex-col h-full">
      {/* Search */}
      <div className="p-4 border-b">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search conversations..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9"
          />
        </div>
      </div>

      {/* Conversation list */}
      <div className="flex-1 overflow-hidden">
        <ConversationList
          conversations={filteredConversations}
          selectedId={selectedConversationId}
          onSelect={handleSelectConversation}
          isLoading={isLoadingConversations}
        />
      </div>
    </div>
  );

  // Main content
  const mainContent = selectedConversationId ? (
    <ConversationDetail
      conversation={conversation}
      messages={messages}
      isLoadingConversation={isLoadingConversation}
      isLoadingMessages={isLoadingMessages}
      onBack={handleBack}
      onArchive={handleArchive}
    />
  ) : (
    <EmptyState />
  );

  return (
    <DashboardLayout
      user={user}
      onLogout={logout}
      sidebar={sidebarContent}
      main={mainContent}
      showSidebar={showSidebar}
      onSidebarToggle={handleToggleSidebar}
    />
  );
}
