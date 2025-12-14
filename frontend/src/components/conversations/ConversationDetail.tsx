"use client";

import { Archive, ArrowLeft, MoreVertical } from "lucide-react";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import type { ConversationDetail as ConversationDetailType, Message } from "@/types";

import { MessageList } from "./MessageList";

interface ConversationDetailProps {
  conversation: ConversationDetailType | undefined;
  messages: Message[];
  isLoadingConversation: boolean;
  isLoadingMessages: boolean;
  onBack: () => void;
  onArchive?: () => void;
}

function ConversationDetailSkeleton() {
  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-3 p-4 border-b">
        <Skeleton className="h-10 w-10 rounded-full" />
        <div className="space-y-1">
          <Skeleton className="h-4 w-32" />
          <Skeleton className="h-3 w-20" />
        </div>
      </div>
      <div className="flex-1 p-4 space-y-4">
        <Skeleton className="h-12 w-3/5 rounded-2xl" />
        <Skeleton className="h-12 w-2/5 rounded-2xl ml-auto" />
        <Skeleton className="h-12 w-3/5 rounded-2xl" />
      </div>
    </div>
  );
}

export function ConversationDetail({
  conversation,
  messages,
  isLoadingConversation,
  isLoadingMessages,
  onBack,
  onArchive,
}: ConversationDetailProps) {
  if (isLoadingConversation) {
    return <ConversationDetailSkeleton />;
  }

  if (!conversation) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-muted-foreground">Conversation not found</p>
      </div>
    );
  }

  const { instagram_user, status } = conversation;
  const displayName =
    instagram_user.name || instagram_user.username || "Unknown User";
  const initials = displayName
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center gap-3 p-4 border-b">
        <Button
          variant="ghost"
          size="icon"
          className="md:hidden"
          onClick={onBack}
        >
          <ArrowLeft className="h-5 w-5" />
          <span className="sr-only">Back to conversations</span>
        </Button>

        <Avatar className="h-10 w-10">
          <AvatarImage
            src={instagram_user.profile_picture_url ?? undefined}
            alt={displayName}
          />
          <AvatarFallback>{initials}</AvatarFallback>
        </Avatar>

        <div className="flex-1 min-w-0">
          <h2 className="font-semibold text-sm truncate">{displayName}</h2>
          {instagram_user.username && (
            <p className="text-xs text-muted-foreground">
              @{instagram_user.username}
            </p>
          )}
        </div>

        <div className="flex items-center gap-1">
          {onArchive && status !== "archived" && (
            <Button
              variant="ghost"
              size="icon"
              onClick={onArchive}
              title="Archive conversation"
            >
              <Archive className="h-4 w-4" />
              <span className="sr-only">Archive</span>
            </Button>
          )}
          <Button variant="ghost" size="icon">
            <MoreVertical className="h-4 w-4" />
            <span className="sr-only">More options</span>
          </Button>
        </div>
      </div>

      <Separator />

      {/* Messages */}
      <div className="flex-1 overflow-hidden">
        <MessageList messages={messages} isLoading={isLoadingMessages} />
      </div>
    </div>
  );
}
