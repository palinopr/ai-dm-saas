import { FeatureTabs } from "./FeatureTabs";
import { AnimatedBackground } from "@/components/ui/animated-background";

export function Solution() {
  return (
    <section id="features" className="relative py-20 md:py-28 overflow-hidden">
      {/* Background */}
      <AnimatedBackground variant="section" />
      
      <div className="container relative mx-auto max-w-6xl px-4">
        {/* Headline */}
        <div className="mx-auto max-w-3xl text-center">
          <p className="mb-4 inline-flex items-center gap-2 rounded-full bg-gradient-primary/10 px-4 py-1.5 text-sm font-semibold text-primary">
            <span className="h-1.5 w-1.5 rounded-full bg-primary" />
            The Solution
          </p>
          <h2 className="font-display text-3xl font-bold tracking-tight sm:text-4xl md:text-5xl">
            Your AI Sales Assistant for{" "}
            <span className="gradient-text">Instagram & TikTok</span>
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            ReplyHQ combines powerful AI with your Shopify store to create the 
            ultimate customer experience across all platforms.
          </p>
        </div>

        {/* Feature Tabs */}
        <div className="mt-16">
          <FeatureTabs />
        </div>
      </div>
    </section>
  );
}
