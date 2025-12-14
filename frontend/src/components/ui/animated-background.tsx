"use client";

import { cn } from "@/lib/utils";

interface AnimatedBackgroundProps {
  className?: string;
  variant?: "hero" | "section" | "subtle";
}

export function AnimatedBackground({
  className,
  variant = "hero",
}: AnimatedBackgroundProps) {
  if (variant === "subtle") {
    return (
      <div className={cn("absolute inset-0 -z-10 overflow-hidden", className)}>
        <div className="absolute inset-0 bg-gradient-to-b from-gradient-start/5 via-transparent to-transparent" />
      </div>
    );
  }

  if (variant === "section") {
    return (
      <div className={cn("absolute inset-0 -z-10 overflow-hidden", className)}>
        <div className="absolute inset-0 bg-gradient-to-br from-gradient-start/5 via-gradient-mid/5 to-gradient-end/5" />
        <div className="absolute top-0 left-1/4 h-[500px] w-[500px] rounded-full bg-gradient-start/10 blur-[100px]" />
        <div className="absolute bottom-0 right-1/4 h-[400px] w-[400px] rounded-full bg-gradient-end/10 blur-[100px]" />
      </div>
    );
  }

  return (
    <div className={cn("absolute inset-0 -z-10 overflow-hidden", className)}>
      {/* Base gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-background to-background" />

      {/* Animated blobs */}
      <div className="absolute -top-40 -left-40 h-[600px] w-[600px] animate-blob rounded-full bg-gradient-start/20 mix-blend-multiply blur-[100px] filter" />
      <div className="absolute -top-20 left-1/3 h-[500px] w-[500px] animate-blob animation-delay-2000 rounded-full bg-gradient-mid/15 mix-blend-multiply blur-[100px] filter" />
      <div className="absolute top-20 right-0 h-[550px] w-[550px] animate-blob animation-delay-4000 rounded-full bg-gradient-end/20 mix-blend-multiply blur-[100px] filter" />

      {/* Additional depth */}
      <div className="absolute bottom-0 left-1/4 h-[400px] w-[400px] animate-blob animation-delay-2000 rounded-full bg-gradient-start/10 mix-blend-multiply blur-[80px] filter" />
      <div className="absolute -bottom-20 right-1/3 h-[450px] w-[450px] animate-blob animation-delay-4000 rounded-full bg-gradient-mid/10 mix-blend-multiply blur-[80px] filter" />

      {/* Subtle noise overlay for texture */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIj48ZmlsdGVyIGlkPSJhIiB4PSIwIiB5PSIwIj48ZmVUdXJidWxlbmNlIGJhc2VGcmVxdWVuY3k9Ii43NSIgc3RpdGNoVGlsZXM9InN0aXRjaCIgdHlwZT0iZnJhY3RhbE5vaXNlIi8+PGZlQ29sb3JNYXRyaXggdHlwZT0ic2F0dXJhdGUiIHZhbHVlcz0iMCIvPjwvZmlsdGVyPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbHRlcj0idXJsKCNhKSIgb3BhY2l0eT0iMC4wNSIvPjwvc3ZnPg==')] opacity-50" />

      {/* Gradient overlay for smooth blending */}
      <div className="absolute inset-0 bg-gradient-to-t from-background via-background/50 to-transparent" />
    </div>
  );
}

interface GlowOrbProps {
  className?: string;
  color?: "primary" | "accent" | "mixed";
  size?: "sm" | "md" | "lg" | "xl";
  animate?: boolean;
}

export function GlowOrb({
  className,
  color = "primary",
  size = "md",
  animate = true,
}: GlowOrbProps) {
  const sizeClasses = {
    sm: "h-32 w-32",
    md: "h-64 w-64",
    lg: "h-96 w-96",
    xl: "h-[500px] w-[500px]",
  };

  const colorClasses = {
    primary: "bg-gradient-start/30",
    accent: "bg-gradient-end/30",
    mixed: "bg-gradient-to-r from-gradient-start/30 via-gradient-mid/30 to-gradient-end/30",
  };

  return (
    <div
      className={cn(
        "rounded-full blur-[80px] filter",
        sizeClasses[size],
        colorClasses[color],
        animate && "animate-blob",
        className
      )}
    />
  );
}

