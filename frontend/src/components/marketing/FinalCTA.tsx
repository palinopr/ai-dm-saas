import { ArrowRight, Play, Shield, Clock, CreditCard } from "lucide-react";
import { Button } from "@/components/ui/button";
import { GradientButton } from "@/components/ui/gradient-button";
import Link from "next/link";

const trustPoints = [
  { icon: Shield, text: "No credit card required" },
  { icon: Clock, text: "Setup in 5 minutes" },
  { icon: CreditCard, text: "Cancel anytime" },
];

export function FinalCTA() {
  return (
    <section className="relative overflow-hidden py-20 md:py-28">
      {/* Full Gradient Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-gradient-start/20 via-gradient-mid/10 to-gradient-end/20" />
      
      {/* Animated Orbs */}
      <div className="absolute -top-40 -left-40 h-[500px] w-[500px] animate-blob rounded-full bg-gradient-start/30 mix-blend-multiply blur-[100px] filter" />
      <div className="absolute -bottom-40 -right-40 h-[500px] w-[500px] animate-blob animation-delay-2000 rounded-full bg-gradient-end/30 mix-blend-multiply blur-[100px] filter" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-[400px] w-[400px] animate-blob animation-delay-4000 rounded-full bg-gradient-mid/20 mix-blend-multiply blur-[100px] filter" />
      
      {/* Content */}
      <div className="container relative mx-auto max-w-4xl px-4 text-center">
        {/* Badge */}
        <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-primary/30 bg-background/50 px-4 py-2 backdrop-blur-sm">
          <span className="relative flex h-2 w-2">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-primary opacity-75" />
            <span className="relative inline-flex h-2 w-2 rounded-full bg-primary" />
          </span>
          <span className="text-sm font-medium">Start converting DMs into sales today</span>
        </div>
        
        {/* Headline */}
        <h2 className="font-display text-3xl font-bold tracking-tight sm:text-4xl md:text-5xl lg:text-6xl">
          Ready to Turn Your DMs Into a{" "}
          <span className="gradient-text">Sales Machine?</span>
        </h2>

        <p className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground md:text-xl">
          Join hundreds of e-commerce brands using ReplyHQ to automate customer 
          conversations and increase revenue.
        </p>

        {/* Dual CTAs */}
        <div className="mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
          <Link href="/register">
            <GradientButton size="xl" className="gap-2 text-base font-semibold">
              Start Free 14-Day Trial
              <ArrowRight className="h-5 w-5" />
            </GradientButton>
          </Link>
          <Button
            variant="outline"
            size="lg"
            className="gap-2 border-2 bg-background/50 text-base font-semibold backdrop-blur-sm hover:bg-background/80"
          >
            <Play className="h-4 w-4 fill-current" />
            Watch Demo
          </Button>
        </div>

        {/* Trust Points */}
        <div className="mt-10 flex flex-wrap items-center justify-center gap-6">
          {trustPoints.map((point, index) => (
            <div key={index} className="flex items-center gap-2 text-sm text-muted-foreground">
              <point.icon className="h-4 w-4 text-primary" />
              <span>{point.text}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
