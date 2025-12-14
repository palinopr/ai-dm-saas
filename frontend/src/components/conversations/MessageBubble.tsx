"use client";

import { format } from "date-fns";
import { Bot } from "lucide-react";

import { cn } from "@/lib/utils";
import type { Message } from "@/types";

interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isOutbound = message.direction === "outbound";
  const timestamp = message.instagram_timestamp || message.created_at;
  const formattedTime = format(new Date(timestamp), "h:mm a");

  return (
    <div
      className={cn(
        "flex w-full gap-2",
        isOutbound ? "justify-end" : "justify-start"
      )}
    >
      <div
        className={cn(
          "max-w-[75%] rounded-2xl px-4 py-2",
          isOutbound
            ? "bg-primary text-primary-foreground rounded-br-md"
            : "bg-muted rounded-bl-md"
        )}
      >
        <p className="text-sm whitespace-pre-wrap break-words">
          {message.content}
        </p>

        <div
          className={cn(
            "flex items-center gap-1.5 mt-1",
            isOutbound ? "justify-end" : "justify-start"
          )}
        >
          {isOutbound && message.is_ai_generated && (
            <Bot className="h-3 w-3 opacity-70" />
          )}
          <span
            className={cn(
              "text-xs opacity-70",
              isOutbound ? "text-primary-foreground" : "text-muted-foreground"
            )}
          >
            {formattedTime}
          </span>
        </div>

        {isOutbound && message.intent && (
          <div className="mt-1">
            <span
              className={cn(
                "text-xs opacity-60",
                isOutbound ? "text-primary-foreground" : "text-muted-foreground"
              )}
            >
              Intent: {message.intent}
              {message.confidence !== null &&
                ` (${Math.round(message.confidence * 100)}%)`}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
