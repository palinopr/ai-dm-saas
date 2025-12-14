"use client";

import { useState } from "react";
import { Check, Sparkles, Shield, Zap, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { GradientButton } from "@/components/ui/gradient-button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import Link from "next/link";

interface PricingTier {
  name: string;
  monthlyPrice: number;
  annualPrice: number;
  description: string;
  features: string[];
  highlighted: boolean;
  badge?: string;
}

const pricingTiers: PricingTier[] = [
  {
    name: "Starter",
    monthlyPrice: 79,
    annualPrice: 63,
    description: "Perfect for small stores getting started",
    features: [
      "1,000 messages/month",
      "1 Instagram account",
      "Shopify integration",
      "Basic AI responses",
      "Email support",
    ],
    highlighted: false,
  },
  {
    name: "Growth",
    monthlyPrice: 149,
    annualPrice: 119,
    description: "For growing brands ready to scale",
    features: [
      "5,000 messages/month",
      "3 Instagram accounts",
      "TikTok + WhatsApp",
      "Advanced AI training",
      "Priority support",
      "Conversation analytics",
    ],
    highlighted: true,
    badge: "Most Popular",
  },
  {
    name: "Enterprise",
    monthlyPrice: 399,
    annualPrice: 319,
    description: "For high-volume stores",
    features: [
      "Unlimited messages",
      "Unlimited accounts",
      "Custom AI training",
      "Dedicated account manager",
      "API access",
      "White-label option",
    ],
    highlighted: false,
  },
];

const includedInAll = [
  { icon: Shield, text: "14-day free trial" },
  { icon: Zap, text: "No credit card required" },
  { icon: Clock, text: "Cancel anytime" },
];

export function Pricing() {
  const [billingPeriod, setBillingPeriod] = useState<"annual" | "monthly">("annual");

  const calculateSavings = (tier: PricingTier): number => {
    return (tier.monthlyPrice - tier.annualPrice) * 12;
  };

  return (
    <section id="pricing" className="relative py-20 md:py-28 overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-muted/20 to-background" />
      
      <div className="container relative mx-auto max-w-6xl px-4">
        {/* Headline */}
        <div className="mx-auto max-w-3xl text-center">
          <p className="mb-4 inline-flex items-center gap-2 rounded-full bg-gradient-primary/10 px-4 py-1.5 text-sm font-semibold text-primary">
            <Sparkles className="h-4 w-4" />
            Simple Pricing
          </p>
          <h2 className="font-display text-3xl font-bold tracking-tight sm:text-4xl md:text-5xl">
            Choose Your Plan
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Start free, upgrade when you&apos;re ready. No hidden fees.
          </p>
        </div>

        {/* Billing Toggle */}
        <div className="mt-10 flex flex-col items-center gap-4">
          <div className="inline-flex rounded-full bg-muted p-1">
            <button
              onClick={() => setBillingPeriod("monthly")}
              className={cn(
                "rounded-full px-6 py-2 text-sm font-medium transition-all duration-300",
                billingPeriod === "monthly"
                  ? "bg-background text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              )}
            >
              Monthly
            </button>
            <button
              onClick={() => setBillingPeriod("annual")}
              className={cn(
                "flex items-center gap-2 rounded-full px-6 py-2 text-sm font-medium transition-all duration-300",
                billingPeriod === "annual"
                  ? "bg-background text-foreground shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              )}
            >
              Annual
              <Badge className="bg-gradient-primary text-white text-xs">
                Save 20%
              </Badge>
            </button>
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="mt-12 grid gap-8 lg:grid-cols-3">
          {pricingTiers.map((tier) => (
            <Card
              key={tier.name}
              className={cn(
                "relative flex flex-col overflow-hidden transition-all duration-300",
                tier.highlighted
                  ? "border-primary/50 shadow-xl shadow-primary/10 scale-[1.02] lg:scale-105"
                  : "border-border/50 hover:border-primary/30 hover:shadow-lg"
              )}
            >
              {/* Gradient top border for highlighted */}
              {tier.highlighted && (
                <div className="absolute inset-x-0 top-0 h-1 bg-gradient-primary" />
              )}
              
              {tier.badge && (
                <Badge className="absolute right-4 top-4 bg-gradient-primary text-white">
                  {tier.badge}
                </Badge>
              )}
              
              <CardHeader className={cn(tier.badge && "pt-10")}>
                <CardTitle className="font-display text-xl">{tier.name}</CardTitle>
                <CardDescription>{tier.description}</CardDescription>
              </CardHeader>
              
              <CardContent className="flex-1">
                {/* Price */}
                <div className="mb-6">
                  <div className="flex items-baseline gap-1">
                    <span className={cn(
                      "font-display text-4xl font-bold",
                      tier.highlighted && "gradient-text"
                    )}>
                      ${billingPeriod === "annual" ? tier.annualPrice : tier.monthlyPrice}
                    </span>
                    <span className="text-muted-foreground">/month</span>
                  </div>
                  {billingPeriod === "annual" && (
                    <>
                      <p className="mt-1 text-sm font-medium text-primary">
                        Save ${calculateSavings(tier)}/year
                      </p>
                      <p className="text-xs text-muted-foreground">
                        Billed ${tier.annualPrice * 12} annually
                      </p>
                    </>
                  )}
                </div>

                {/* Features */}
                <ul className="space-y-3">
                  {tier.features.map((feature, index) => (
                    <li key={index} className="flex items-center gap-3">
                      <div className={cn(
                        "flex h-5 w-5 items-center justify-center rounded-full",
                        tier.highlighted
                          ? "bg-gradient-primary/20"
                          : "bg-primary/10"
                      )}>
                        <Check className={cn(
                          "h-3 w-3",
                          tier.highlighted ? "text-primary" : "text-primary"
                        )} />
                      </div>
                      <span className="text-sm">{feature}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
              
              <CardFooter>
                <Link href="/register" className="w-full">
                  {tier.highlighted ? (
                    <GradientButton className="w-full">
                      Start Free Trial
                    </GradientButton>
                  ) : (
                    <Button variant="outline" className="w-full border-2">
                      Start Free Trial
                    </Button>
                  )}
                </Link>
              </CardFooter>
            </Card>
          ))}
        </div>

        {/* What's Included in All Plans */}
        <div className="mt-16 text-center">
          <div className="inline-flex flex-wrap items-center justify-center gap-6 rounded-2xl border border-border/50 bg-muted/30 px-8 py-4">
            {includedInAll.map((item, index) => (
              <div key={index} className="flex items-center gap-2">
                <item.icon className="h-4 w-4 text-primary" />
                <span className="text-sm font-medium">{item.text}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
