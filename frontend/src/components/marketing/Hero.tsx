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
            Tired of losing sales in your{" "}
            <span className="text-primary">DMs?</span>
          </h1>

          {/* Subheadline */}
          <p className="mt-6 max-w-2xl text-lg text-muted-foreground md:text-xl">
            Every missed DM is a lost customer. Stop letting revenue slip
            through your fingers.
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

          {/* Hero Image Placeholder */}
          <div className="mt-16 w-full max-w-4xl">
            {/* PLACEHOLDER: Product Demo Animation - 600x400px */}
            <div className="relative aspect-[3/2] overflow-hidden rounded-xl border bg-gradient-to-br from-primary/20 via-primary/10 to-background shadow-2xl">
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center">
                  <div className="mb-4 text-6xl">📱</div>
                  <p className="text-sm font-medium text-muted-foreground">
                    Product Demo Animation
                  </p>
                  <p className="text-xs text-muted-foreground">
                    Chaotic DM inbox → Organized automation
                  </p>
                </div>
              </div>
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
