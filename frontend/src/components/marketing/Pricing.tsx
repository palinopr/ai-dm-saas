"use client";

import { useState } from "react";
import { Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { cn } from "@/lib/utils";
import Link from "next/link";
import type { PricingTier } from "@/types/marketing";

const pricingTiers: PricingTier[] = [
  {
    name: "Starter",
    monthlyPrice: 79,
    annualPrice: 63,
    description: "Perfect for small stores getting started",
    messageLimit: "1,000 messages/month",
    accountLimit: "1 Instagram account",
    features: ["1,000 messages/month", "1 Instagram account", "Email support"],
    highlighted: false,
  },
  {
    name: "Growth",
    monthlyPrice: 149,
    annualPrice: 119,
    description: "For growing brands ready to scale",
    messageLimit: "5,000 messages/month",
    accountLimit: "3 Instagram accounts",
    features: [
      "5,000 messages/month",
      "3 Instagram accounts",
      "Priority support",
      "Advanced analytics",
    ],
    highlighted: true,
  },
  {
    name: "Enterprise",
    monthlyPrice: 399,
    annualPrice: 319,
    description: "For high-volume stores",
    messageLimit: "Unlimited messages",
    accountLimit: "Unlimited accounts",
    features: [
      "Unlimited messages",
      "Unlimited accounts",
      "Dedicated account manager",
      "Custom AI training",
    ],
    highlighted: false,
  },
];

export function Pricing() {
  const [billingPeriod, setBillingPeriod] = useState<"annual" | "monthly">(
    "annual"
  );

  const calculateSavings = (tier: PricingTier): number => {
    return (tier.monthlyPrice - tier.annualPrice) * 12;
  };

  return (
    <section id="pricing" className="bg-muted/50 py-20 md:py-28">
      <div className="container mx-auto max-w-6xl px-4">
        {/* Headline */}
        <div className="mx-auto max-w-3xl text-center">
          <p className="mb-4 text-sm font-semibold uppercase tracking-wider text-primary">
            Pricing
          </p>
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl md:text-5xl">
            Choose the plan that&apos;s right for you
          </h2>
        </div>

        {/* Billing Toggle */}
        <div className="mt-10 flex flex-col items-center gap-4">
          <Tabs
            value={billingPeriod}
            onValueChange={(v) => setBillingPeriod(v as "annual" | "monthly")}
            className="w-auto"
          >
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="monthly">Monthly</TabsTrigger>
              <TabsTrigger value="annual" className="gap-2">
                Annual
                <Badge variant="secondary" className="text-xs">
                  Save 20%
                </Badge>
              </TabsTrigger>
            </TabsList>
          </Tabs>
        </div>

        {/* Pricing Cards */}
        <div className="mt-12 grid gap-8 lg:grid-cols-3">
          {pricingTiers.map((tier) => (
            <Card
              key={tier.name}
              className={cn(
                "relative flex flex-col",
                tier.highlighted &&
                  "border-primary shadow-lg ring-2 ring-primary"
              )}
            >
              {tier.highlighted && (
                <Badge className="absolute -top-3 left-1/2 -translate-x-1/2">
                  Most Popular
                </Badge>
              )}
              <CardHeader>
                <CardTitle className="text-xl">{tier.name}</CardTitle>
                <CardDescription>{tier.description}</CardDescription>
              </CardHeader>
              <CardContent className="flex-1">
                {/* Price */}
                <div className="mb-6">
                  <div className="flex items-baseline gap-1">
                    <span className="text-4xl font-bold">
                      $
                      {billingPeriod === "annual"
                        ? tier.annualPrice
                        : tier.monthlyPrice}
                    </span>
                    <span className="text-muted-foreground">/month</span>
                  </div>
                  {billingPeriod === "annual" && (
                    <p className="mt-1 text-sm text-primary">
                      Save ${calculateSavings(tier)}/year
                    </p>
                  )}
                  {billingPeriod === "annual" && (
                    <p className="text-xs text-muted-foreground">
                      Billed ${tier.annualPrice * 12} annually
                    </p>
                  )}
                </div>

                {/* Features */}
                <ul className="space-y-3">
                  {tier.features.map((feature, index) => (
                    <li key={index} className="flex items-center gap-2">
                      <Check className="h-4 w-4 text-primary" />
                      <span className="text-sm">{feature}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
              <CardFooter>
                <Link href="/register" className="w-full">
                  <Button
                    className="w-full"
                    variant={tier.highlighted ? "default" : "outline"}
                  >
                    Start Free Trial
                  </Button>
                </Link>
              </CardFooter>
            </Card>
          ))}
        </div>

        {/* Urgency Text */}
        <div className="mt-12 text-center">
          <Badge variant="secondary" className="px-4 py-2 text-sm">
            Limited time: 20% off for the first 50 customers
          </Badge>
        </div>
      </div>
    </section>
  );
}
