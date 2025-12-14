"use client";

import { MessageSquare } from "lucide-react";

export function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center h-full p-6 text-center">
      <div className="rounded-full bg-muted p-4 mb-4">
        <MessageSquare className="h-8 w-8 text-muted-foreground" />
      </div>
      <h3 className="font-semibold text-lg mb-1">No conversation selected</h3>
      <p className="text-sm text-muted-foreground max-w-sm">
        Select a conversation from the sidebar to view messages and manage your
        Instagram DMs
      </p>
    </div>
  );
}
