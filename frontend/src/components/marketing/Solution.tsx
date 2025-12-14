import { Clock, ShoppingCart, BarChart3, Check } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

const features = [
  {
    icon: Clock,
    title: "Never Miss a Lead Again",
    description:
      "Our AI responds to every DM instantly, 24/7. No more lost sales while you sleep.",
    highlights: ["24/7 availability", "Instant responses", "Never miss a lead"],
  },
  {
    icon: ShoppingCart,
    title: "Answer Product Questions Instantly",
    description:
      "Connected to your Shopify store. Real-time inventory, pricing, and order tracking.",
    highlights: [
      "Shopify integration",
      "Real-time inventory",
      "Order tracking",
    ],
  },
  {
    icon: BarChart3,
    title: "Know Your Customers Better",
    description:
      "AI-powered conversation analytics show you what customers really want.",
    highlights: [
      "Conversation analytics",
      "Customer insights",
      "Data-driven decisions",
    ],
  },
];

export function Solution() {
  return (
    <section id="features" className="bg-muted/50 py-20 md:py-28">
      <div className="container mx-auto max-w-6xl px-4">
        {/* Headline */}
        <div className="mx-auto max-w-3xl text-center">
          <p className="mb-4 text-sm font-semibold uppercase tracking-wider text-primary">
            The Solution
          </p>
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl md:text-5xl">
            Your AI Sales Assistant for Instagram & TikTok DMs
          </h2>
        </div>

        {/* Feature Cards */}
        <div className="mt-16 grid gap-8 lg:grid-cols-3">
          {features.map((feature, index) => (
            <Card key={index} className="relative overflow-hidden">
              <CardContent className="pt-6">
                <div className="mb-4 inline-flex rounded-lg bg-primary/10 p-3">
                  <feature.icon className="h-6 w-6 text-primary" />
                </div>
                <h3 className="mb-2 text-xl font-semibold">{feature.title}</h3>
                <p className="mb-4 text-muted-foreground">
                  {feature.description}
                </p>
                <ul className="space-y-2">
                  {feature.highlights.map((highlight, i) => (
                    <li key={i} className="flex items-center gap-2 text-sm">
                      <Check className="h-4 w-4 text-primary" />
                      {highlight}
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
