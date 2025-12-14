"use client";

import { Clock, DollarSign, MessageSquareX, X, Check, ArrowRight } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

const painPoints = [
  {
    icon: Clock,
    stat: "85%",
    title: "of customers expect a response within 10 minutes",
    description: "But you can't be online 24/7. Every missed DM is a lost opportunity.",
  },
  {
    icon: DollarSign,
    stat: "$3,000+",
    title: "per month for a social media manager",
    description: "Hiring help is expensive. That cuts directly into your margins.",
  },
  {
    icon: MessageSquareX,
    stat: "Generic",
    title: "auto-replies annoy customers and kill sales",
    description: "Canned responses feel robotic. Customers want real answers, not templates.",
  },
];

const beforeAfter = {
  before: [
    "Missed DMs while you sleep",
    "Hours spent answering same questions",
    "Lost sales from slow responses",
    "No product info in conversations",
    "Can't scale without hiring",
  ],
  after: [
    "24/7 instant AI responses",
    "AI handles FAQs automatically",
    "Convert leads in seconds",
    "Real-time Shopify integration",
    "Scale infinitely with AI",
  ],
};

export function Agitation() {
  return (
    <section className="relative py-20 md:py-28 overflow-hidden">
      {/* Background accent */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-muted/30 to-background" />
      
      <div className="container relative mx-auto max-w-6xl px-4">
        {/* Headline */}
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="font-display text-3xl font-bold tracking-tight sm:text-4xl md:text-5xl">
            Your DMs are a goldmine.{" "}
            <span className="text-muted-foreground">
              But you&apos;re leaving money on the table.
            </span>
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Every unanswered message is a customer choosing your competitor instead.
          </p>
        </div>

        {/* Pain Point Cards */}
        <div className="mt-16 grid gap-6 md:grid-cols-3">
          {painPoints.map((point, index) => (
            <Card
              key={index}
              className="group relative overflow-hidden border-destructive/20 bg-gradient-to-br from-destructive/5 to-destructive/10 transition-all duration-300 hover:border-destructive/40 hover:shadow-lg"
            >
              <CardContent className="pt-6">
                <div className="mb-4 inline-flex rounded-xl bg-destructive/10 p-3 transition-colors group-hover:bg-destructive/20">
                  <point.icon className="h-6 w-6 text-destructive" />
                </div>
                <div className="mb-2 font-display text-3xl font-bold text-destructive">
                  {point.stat}
                </div>
                <p className="text-lg font-semibold">{point.title}</p>
                <p className="mt-2 text-sm text-muted-foreground">
                  {point.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Before/After Comparison */}
        <div className="mt-20">
          <h3 className="mb-10 text-center font-display text-2xl font-bold md:text-3xl">
            See the Difference
          </h3>
          
          <div className="grid gap-6 lg:grid-cols-2">
            {/* Before */}
            <Card className="relative overflow-hidden border-muted-foreground/20 bg-muted/50">
              <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-muted-foreground/30 to-muted-foreground/10" />
              <CardContent className="pt-8">
                <div className="mb-6 flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-muted-foreground/10">
                    <X className="h-5 w-5 text-muted-foreground" />
                  </div>
                  <h4 className="font-display text-xl font-semibold text-muted-foreground">
                    Without ReplyHQ
                  </h4>
                </div>
                <ul className="space-y-4">
                  {beforeAfter.before.map((item, index) => (
                    <li key={index} className="flex items-start gap-3">
                      <div className="mt-0.5 flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-muted-foreground/10">
                        <X className="h-3 w-3 text-muted-foreground" />
                      </div>
                      <span className="text-muted-foreground">{item}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>

            {/* After */}
            <Card className="relative overflow-hidden border-primary/30 bg-gradient-to-br from-primary/5 to-gradient-end/5">
              <div className="absolute inset-x-0 top-0 h-1 bg-gradient-primary" />
              <CardContent className="pt-8">
                <div className="mb-6 flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-primary">
                    <Check className="h-5 w-5 text-white" />
                  </div>
                  <h4 className="font-display text-xl font-semibold">
                    With ReplyHQ
                  </h4>
                </div>
                <ul className="space-y-4">
                  {beforeAfter.after.map((item, index) => (
                    <li key={index} className="flex items-start gap-3">
                      <div className="mt-0.5 flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-gradient-primary/20">
                        <Check className="h-3 w-3 text-primary" />
                      </div>
                      <span className="font-medium">{item}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
}
