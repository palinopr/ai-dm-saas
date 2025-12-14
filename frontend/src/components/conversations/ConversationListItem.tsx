"use client";

import { formatDistanceToNow } from "date-fns";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { Conversation } from "@/types";

interface ConversationListItemProps {
  conversation: Conversation;
  isSelected: boolean;
  onClick: () => void;
}

export function ConversationListItem({
  conversation,
  isSelected,
  onClick,
}: ConversationListItemProps) {
  const { instagram_user, last_message_at, unread_count, last_message_preview } =
    conversation;

  const displayName =
    instagram_user.name || instagram_user.username || "Unknown User";
  const initials = displayName
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);

  const timeAgo = last_message_at
    ? formatDistanceToNow(new Date(last_message_at), { addSuffix: true })
    : null;

  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        "w-full flex items-start gap-3 p-3 text-left transition-colors hover:bg-accent rounded-lg",
        isSelected && "bg-accent"
      )}
    >
      <Avatar className="h-10 w-10 shrink-0">
        <AvatarImage
          src={instagram_user.profile_picture_url ?? undefined}
          alt={displayName}
        />
        <AvatarFallback className="text-xs">{initials}</AvatarFallback>
      </Avatar>

      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between gap-2">
          <span className="font-medium text-sm truncate">{displayName}</span>
          {timeAgo && (
            <span className="text-xs text-muted-foreground shrink-0">
              {timeAgo}
            </span>
          )}
        </div>

        <div className="flex items-center justify-between gap-2 mt-0.5">
          <span className="text-sm text-muted-foreground truncate">
            {last_message_preview || "No messages yet"}
          </span>
          {unread_count > 0 && (
            <Badge variant="default" className="shrink-0 h-5 min-w-5 px-1.5">
              {unread_count > 99 ? "99+" : unread_count}
            </Badge>
          )}
        </div>
      </div>
    </button>
  );
}
