"use client";

import { LogOut, Menu, MessageSquare } from "lucide-react";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import type { User } from "@/types";

interface DashboardHeaderProps {
  user: User | null | undefined;
  onLogout: () => void;
  onMenuToggle: () => void;
  showMenuButton?: boolean;
}

export function DashboardHeader({
  user,
  onLogout,
  onMenuToggle,
  showMenuButton = true,
}: DashboardHeaderProps) {
  const initials = user?.email
    ?.split("@")[0]
    .slice(0, 2)
    .toUpperCase() || "??";

  return (
    <header className="border-b bg-background">
      <div className="flex h-14 items-center gap-4 px-4">
        {showMenuButton && (
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={onMenuToggle}
          >
            <Menu className="h-5 w-5" />
            <span className="sr-only">Toggle menu</span>
          </Button>
        )}

        <div className="flex items-center gap-2">
          <MessageSquare className="h-6 w-6 text-primary" />
          <span className="font-semibold text-lg hidden sm:inline">
            DM Automation
          </span>
        </div>

        <div className="flex-1" />

        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-2">
            <Avatar className="h-8 w-8">
              <AvatarFallback className="text-xs">{initials}</AvatarFallback>
            </Avatar>
            <span className="text-sm text-muted-foreground">
              {user?.email || "Loading..."}
            </span>
          </div>

          <Separator orientation="vertical" className="h-6 hidden sm:block" />

          <Button variant="ghost" size="sm" onClick={onLogout}>
            <LogOut className="h-4 w-4 mr-2" />
            <span className="hidden sm:inline">Logout</span>
          </Button>
        </div>
      </div>
    </header>
  );
}
