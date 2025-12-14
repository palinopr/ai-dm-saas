"use client";

import { Star, Quote, ArrowRight, TrendingUp } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import Link from "next/link";
import { GradientButton } from "@/components/ui/gradient-button";

interface Testimonial {
  quote: string;
  result: string;
  author: string;
  role: string;
  company: string;
}

const testimonials: Testimonial[] = [
  {
    quote:
      "We went from responding to 20% of DMs to 100%. The AI handles everything from sizing questions to order tracking.",
    result: "40% increase in Instagram sales",
    author: "Sarah Chen",
    role: "Founder",
    company: "GlowBox Cosmetics",
  },
  {
    quote:
      "The AI actually understands our products better than some of our staff. It's like having a 24/7 sales team that never takes a break.",
    result: "3x faster response time",
    author: "Marcus Williams",
    role: "Owner",
    company: "UrbanThreads",
  },
  {
    quote:
      "Setup took 10 minutes. Connected to Shopify, trained on our products, and we were live. ROI was immediate.",
    result: "Saved 20+ hours per week",
    author: "Jessica Park",
    role: "CMO",
    company: "PetPalace",
  },
];

export function SocialProof() {
  return (
    <section id="testimonials" className="relative py-20 md:py-28 overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-muted/30 via-background to-background" />
      
      <div className="container relative mx-auto max-w-6xl px-4">
        {/* Headline */}
        <div className="mx-auto max-w-3xl text-center">
          <p className="mb-4 inline-flex items-center gap-2 rounded-full bg-gradient-primary/10 px-4 py-1.5 text-sm font-semibold text-primary">
            <Star className="h-4 w-4 fill-primary" />
            Early Adopters Love Us
          </p>
          <h2 className="font-display text-3xl font-bold tracking-tight sm:text-4xl md:text-5xl">
            See What Our Customers{" "}
            <span className="gradient-text">Are Saying</span>
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Real results from real e-commerce businesses using ReplyHQ.
          </p>
        </div>

        {/* Testimonial Cards */}
        <div className="mt-16 grid gap-6 md:grid-cols-3">
          {testimonials.map((testimonial, index) => (
            <Card
              key={index}
              className="group relative overflow-hidden border-border/50 bg-card transition-all duration-300 hover:border-primary/30 hover:shadow-lg hover:shadow-primary/5"
            >
              {/* Gradient border on hover */}
              <div className="absolute inset-x-0 top-0 h-1 bg-gradient-primary opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
              
              <CardContent className="pt-6">
                {/* Quote Icon */}
                <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-full bg-gradient-primary/10">
                  <Quote className="h-5 w-5 text-primary" />
                </div>

                {/* Quote */}
                <blockquote className="mb-6 text-base leading-relaxed">
                  &quot;{testimonial.quote}&quot;
                </blockquote>

                {/* Result Badge */}
                <div className="mb-6 inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-gradient-start/10 via-gradient-mid/10 to-gradient-end/10 px-4 py-2">
                  <TrendingUp className="h-4 w-4 text-primary" />
                  <span className="text-sm font-semibold text-foreground">
                    {testimonial.result}
                  </span>
                </div>

                {/* Author */}
                <div className="border-t border-border/50 pt-4">
                  <p className="font-semibold">{testimonial.author}</p>
                  <p className="text-sm text-muted-foreground">
                    {testimonial.role}, {testimonial.company}
                  </p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* CTA Section */}
        <div className="mt-16 text-center">
          <div className="mx-auto max-w-2xl rounded-2xl border border-border/50 bg-gradient-to-br from-muted/50 to-muted/30 p-8 md:p-10">
            <h3 className="font-display text-xl font-bold md:text-2xl">
              Ready to Join Them?
            </h3>
            <p className="mt-2 text-muted-foreground">
              Start your free trial today and see results in your first week.
            </p>
            <div className="mt-6">
              <Link href="/register">
                <GradientButton size="lg" className="gap-2">
                  Start Free 14-Day Trial
                  <ArrowRight className="h-5 w-5" />
                </GradientButton>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
