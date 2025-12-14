"use client";

import { ArrowRight, Play, Sparkles, Zap, MessageCircle, ShoppingBag } from "lucide-react";
import { Button } from "@/components/ui/button";
import { GradientButton } from "@/components/ui/gradient-button";
import { AnimatedBackground } from "@/components/ui/animated-background";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";
import Image from "next/image";

const trustLogos = [
  "GlowBox",
  "UrbanThreads",
  "PetPalace",
  "FitGear",
  "HomeStyle",
];

export function Hero() {
  return (
    <section className="relative min-h-[90vh] overflow-hidden pt-28 pb-16 md:pt-36 md:pb-24 lg:pt-40 lg:pb-32">
      {/* Animated Background */}
      <AnimatedBackground variant="hero" />

      <div className="container relative mx-auto max-w-6xl px-4">
        <div className="flex flex-col items-center text-center">
          {/* Eyebrow Badge */}
          <Badge
            variant="outline"
            className="mb-6 gap-2 border-gradient-start/30 bg-gradient-start/5 px-4 py-2 text-sm font-medium backdrop-blur-sm animate-fade-in"
          >
            <Sparkles className="h-4 w-4 text-gradient-start" />
            <span className="gradient-text font-semibold">AI-Powered DM Automation</span>
          </Badge>

          {/* Headline */}
          <h1 className="max-w-4xl font-display text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl animate-fade-in-up">
            Your{" "}
            <span className="gradient-text">AI Sales Team</span>{" "}
            for Instagram & TikTok
          </h1>

          {/* Subheadline */}
          <p className="mt-6 max-w-2xl text-lg text-muted-foreground md:text-xl lg:text-2xl animate-fade-in-up [animation-delay:100ms]">
            Never miss a DM again. AI responds instantly, 24/7, turning 
            conversations into revenue while you sleep.
          </p>

          {/* Dual CTAs */}
          <div className="mt-10 flex flex-col gap-4 sm:flex-row animate-fade-in-up [animation-delay:200ms]">
            <Link href="/register">
              <GradientButton size="lg" className="gap-2 text-base font-semibold">
                Start Free 14-Day Trial
                <ArrowRight className="h-5 w-5" />
              </GradientButton>
            </Link>
            <Button
              variant="outline"
              size="lg"
              className="gap-2 border-2 text-base font-semibold hover:bg-muted/50"
            >
              <Play className="h-4 w-4 fill-current" />
              Watch Demo
            </Button>
          </div>

          {/* Trust Text */}
          <p className="mt-6 text-sm text-muted-foreground animate-fade-in-up [animation-delay:300ms]">
            No credit card required • Setup in 5 minutes • Cancel anytime
          </p>

          {/* Hero Image */}
          <div className="mt-16 w-full max-w-5xl animate-fade-in-up [animation-delay:400ms]">
            <div className="relative aspect-[16/10] overflow-hidden rounded-2xl border border-border/50 bg-card shadow-2xl shadow-gradient-start/10">
              {/* Gradient border glow */}
              <div className="absolute -inset-[1px] rounded-2xl bg-gradient-primary opacity-20 blur-sm" />
              
              <div className="relative h-full w-full overflow-hidden rounded-2xl bg-gradient-to-br from-muted/50 via-background to-muted/30">
                <Image
                  src="/images/hero-dashboard.png"
                  alt="ReplyHQ AI Dashboard - Automated Instagram and TikTok DM conversations with Shopify integration"
                  fill
                  className="object-cover"
                  priority
                  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 90vw, 1200px"
                />
                
                {/* Floating Feature Cards */}
                <div className="absolute left-4 top-1/4 hidden md:block animate-float">
                  <div className="flex items-center gap-2 rounded-lg border border-border/50 bg-card/90 px-3 py-2 shadow-lg backdrop-blur-sm">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-start/10">
                      <MessageCircle className="h-4 w-4 text-gradient-start" />
                    </div>
                    <div className="text-left">
                      <p className="text-xs font-semibold">Instant Response</p>
                      <p className="text-[10px] text-muted-foreground">AI replied in 2 seconds</p>
                    </div>
                  </div>
                </div>
                
                <div className="absolute right-4 top-1/3 hidden md:block animate-float [animation-delay:1s]">
                  <div className="flex items-center gap-2 rounded-lg border border-border/50 bg-card/90 px-3 py-2 shadow-lg backdrop-blur-sm">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-end/10">
                      <ShoppingBag className="h-4 w-4 text-gradient-end" />
                    </div>
                    <div className="text-left">
                      <p className="text-xs font-semibold">Shopify Connected</p>
                      <p className="text-[10px] text-muted-foreground">Real-time inventory</p>
                    </div>
                  </div>
                </div>
                
                <div className="absolute bottom-1/4 left-1/4 hidden md:block animate-float [animation-delay:2s]">
                  <div className="flex items-center gap-2 rounded-lg border border-border/50 bg-card/90 px-3 py-2 shadow-lg backdrop-blur-sm">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-mid/10">
                      <Zap className="h-4 w-4 text-gradient-mid" />
                    </div>
                    <div className="text-left">
                      <p className="text-xs font-semibold">Sale Confirmed</p>
                      <p className="text-[10px] text-muted-foreground">Order #4829 completed</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Trust Bar - Company Logos */}
          <div className="mt-16 w-full animate-fade-in-up [animation-delay:500ms]">
            <p className="mb-6 text-center text-sm font-medium text-muted-foreground">
              Trusted by e-commerce brands worldwide
            </p>
            <div className="flex flex-wrap items-center justify-center gap-8 md:gap-12">
              {trustLogos.map((logo, index) => (
                <div
                  key={index}
                  className="group flex h-10 items-center justify-center px-4 text-muted-foreground/60 transition-all duration-300 hover:text-foreground"
                >
                  <span className="text-lg font-semibold tracking-tight opacity-60 transition-opacity group-hover:opacity-100">
                    {logo}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
