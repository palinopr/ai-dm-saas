"use client";

import { useEffect, useRef } from "react";

import { ScrollArea } from "@/components/ui/scroll-area";
import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";
import type { Message } from "@/types";

import { MessageBubble } from "./MessageBubble";

interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
}

function MessageListSkeleton() {
  return (
    <div className="flex flex-col gap-3 p-4">
      {Array.from({ length: 6 }).map((_, i) => (
        <div
          key={i}
          className={cn(
            "flex",
            i % 2 === 0 ? "justify-start" : "justify-end"
          )}
        >
          <Skeleton
            className={cn(
              "h-12 rounded-2xl",
              i % 2 === 0
                ? "w-[60%] rounded-bl-md"
                : "w-[50%] rounded-br-md"
            )}
          />
        </div>
      ))}
    </div>
  );
}

export function MessageList({ messages, isLoading }: MessageListProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  if (isLoading) {
    return <MessageListSkeleton />;
  }

  if (messages.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full p-6 text-center">
        <p className="text-sm text-muted-foreground">No messages yet</p>
        <p className="text-xs text-muted-foreground mt-1">
          Messages will appear here when they arrive
        </p>
      </div>
    );
  }

  // Sort messages by timestamp (oldest first)
  const sortedMessages = [...messages].sort((a, b) => {
    const dateA = new Date(a.instagram_timestamp || a.created_at);
    const dateB = new Date(b.instagram_timestamp || b.created_at);
    return dateA.getTime() - dateB.getTime();
  });

  return (
    <ScrollArea className="h-full" ref={scrollRef}>
      <div className="flex flex-col gap-3 p-4">
        {sortedMessages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        <div ref={bottomRef} />
      </div>
    </ScrollArea>
  );
}
