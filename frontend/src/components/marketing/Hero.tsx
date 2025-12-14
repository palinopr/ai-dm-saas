import { ArrowRight, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

export function Hero() {
  return (
    <section className="relative overflow-hidden pt-32 pb-20 md:pt-40 md:pb-32">
      {/* Background gradient */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-b from-primary/5 via-background to-background" />

      <div className="container mx-auto max-w-6xl px-4">
        <div className="flex flex-col items-center text-center">
          {/* Trust badge */}
          <Badge variant="secondary" className="mb-6 gap-1.5 px-3 py-1.5">
            <ShieldCheck className="h-3.5 w-3.5" />
            Trusted by 50+ Shopify brands
          </Badge>

          {/* Headline */}
          <h1 className="max-w-4xl text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl">
            Instagram & TikTok{" "}
            <span className="text-primary">DM Automation</span>{" "}
            That Turns Messages Into Sales
          </h1>

          {/* Subheadline */}
          <p className="mt-6 max-w-2xl text-lg text-muted-foreground md:text-xl">
            AI-powered customer service that responds to Instagram and TikTok DMs 24/7. 
            Never miss a sale while you sleep. Integrates with Shopify for instant product answers.
          </p>

          {/* CTA */}
          <div className="mt-10 flex flex-col gap-4 sm:flex-row">
            <Link href="/register">
              <Button size="lg" className="gap-2 text-base">
                Start My Free 14-Day Trial
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
          </div>

          {/* Hero Image */}
          <div className="mt-16 w-full max-w-4xl">
            <div className="relative aspect-[3/2] overflow-hidden rounded-xl border bg-gradient-to-br from-primary/20 via-primary/10 to-background shadow-2xl">
              <img
                src="/images/hero-dashboard.png"
                alt="AI-powered Instagram and TikTok DM automation dashboard showing manual messages vs AI-managed conversations with automated responses and Shopify integration"
                className="h-full w-full object-cover"
                loading="eager"
                fetchPriority="high"
              />
              {/* Decorative elements */}
              <div className="absolute -right-4 -top-4 h-24 w-24 rounded-full bg-primary/20 blur-3xl" />
              <div className="absolute -bottom-4 -left-4 h-32 w-32 rounded-full bg-primary/10 blur-3xl" />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
