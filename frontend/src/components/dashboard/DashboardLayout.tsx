"use client";

import { useState, useCallback } from "react";

import { cn } from "@/lib/utils";
import type { User } from "@/types";

import { DashboardHeader } from "./DashboardHeader";

interface DashboardLayoutProps {
  user: User | null | undefined;
  onLogout: () => void;
  sidebar: React.ReactNode;
  main: React.ReactNode;
  showSidebar?: boolean;
  onSidebarToggle?: () => void;
}

export function DashboardLayout({
  user,
  onLogout,
  sidebar,
  main,
  showSidebar: controlledShowSidebar,
  onSidebarToggle,
}: DashboardLayoutProps) {
  const [internalShowSidebar, setInternalShowSidebar] = useState(true);

  const isControlled = controlledShowSidebar !== undefined;
  const showSidebar = isControlled ? controlledShowSidebar : internalShowSidebar;

  const handleToggle = useCallback(() => {
    if (onSidebarToggle) {
      onSidebarToggle();
    } else {
      setInternalShowSidebar((prev) => !prev);
    }
  }, [onSidebarToggle]);

  return (
    <div className="flex flex-col h-screen bg-background">
      <DashboardHeader
        user={user}
        onLogout={onLogout}
        onMenuToggle={handleToggle}
      />

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar - responsive */}
        <aside
          className={cn(
            "border-r bg-background transition-all duration-200 ease-in-out",
            // Mobile: full width overlay when visible
            "fixed inset-y-0 left-0 z-50 w-full pt-14",
            "md:relative md:inset-auto md:z-auto md:pt-0",
            // Desktop: fixed width
            "md:w-80 lg:w-96",
            // Visibility
            showSidebar ? "translate-x-0" : "-translate-x-full md:translate-x-0"
          )}
        >
          <div className="h-full overflow-hidden">{sidebar}</div>
        </aside>

        {/* Mobile overlay backdrop */}
        {showSidebar && (
          <div
            className="fixed inset-0 bg-black/50 z-40 md:hidden"
            onClick={handleToggle}
          />
        )}

        {/* Main content */}
        <main className="flex-1 overflow-hidden">{main}</main>
      </div>
    </div>
  );
}
