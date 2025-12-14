"use client";

import { useState } from "react";
import { 
  MessageCircle, 
  ShoppingBag, 
  Globe, 
  BarChart3,
  Sparkles,
  Package,
  Truck,
  CreditCard,
  Instagram,
  MessageSquare,
  TrendingUp,
  Users,
  Check
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Card, CardContent } from "@/components/ui/card";

interface Feature {
  id: string;
  icon: React.ElementType;
  label: string;
  title: string;
  description: string;
  highlights: string[];
  demoPoints: {
    icon: React.ElementType;
    title: string;
    description: string;
  }[];
}

const features: Feature[] = [
  {
    id: "ai",
    icon: Sparkles,
    label: "AI Conversations",
    title: "Intelligent AI That Understands Context",
    description: "Our AI doesn't just respond—it understands. It handles complex questions, remembers conversation history, and knows when to escalate to a human.",
    highlights: [
      "Natural language understanding",
      "Context-aware responses",
      "Learns your brand voice",
      "Smart escalation to humans",
    ],
    demoPoints: [
      {
        icon: MessageCircle,
        title: "Customer asks about sizing",
        description: "AI provides accurate size guide from your product catalog",
      },
      {
        icon: Package,
        title: "Follow-up about materials",
        description: "AI remembers context and answers with product details",
      },
      {
        icon: CreditCard,
        title: "Ready to purchase",
        description: "AI sends direct checkout link, completes the sale",
      },
    ],
  },
  {
    id: "shopify",
    icon: ShoppingBag,
    label: "Shopify Integration",
    title: "Real-Time Shopify Connection",
    description: "Connected directly to your Shopify store. AI accesses live inventory, prices, order status, and product details to give customers accurate answers instantly.",
    highlights: [
      "Live inventory status",
      "Real-time pricing",
      "Order tracking",
      "Product recommendations",
    ],
    demoPoints: [
      {
        icon: Package,
        title: "\"Is this in stock?\"",
        description: "AI checks live inventory: 'Yes! 12 left in your size.'",
      },
      {
        icon: Truck,
        title: "\"Where's my order?\"",
        description: "AI pulls tracking: 'Out for delivery today!'",
      },
      {
        icon: CreditCard,
        title: "\"Any discounts?\"",
        description: "AI applies active promo codes automatically",
      },
    ],
  },
  {
    id: "platforms",
    icon: Globe,
    label: "Multi-Platform",
    title: "One Inbox for All Your DMs",
    description: "Instagram, TikTok, WhatsApp—manage all your customer conversations from a single dashboard. AI handles them all with the same intelligence.",
    highlights: [
      "Instagram DMs",
      "TikTok messages",
      "WhatsApp Business",
      "Unified inbox",
    ],
    demoPoints: [
      {
        icon: Instagram,
        title: "Instagram DM",
        description: "Customer asks about a product they saw in your Reel",
      },
      {
        icon: MessageSquare,
        title: "TikTok message",
        description: "Viewer wants to buy the item from your viral video",
      },
      {
        icon: MessageCircle,
        title: "WhatsApp inquiry",
        description: "International customer needs shipping info",
      },
    ],
  },
  {
    id: "analytics",
    icon: BarChart3,
    label: "Analytics",
    title: "Insights That Drive Growth",
    description: "See what customers are really asking. Discover trending products, common objections, and opportunities to improve your sales process.",
    highlights: [
      "Conversation analytics",
      "Popular questions",
      "Conversion tracking",
      "Response time metrics",
    ],
    demoPoints: [
      {
        icon: TrendingUp,
        title: "Trending Topics",
        description: "\"Sizing questions up 40% - update product descriptions?\"",
      },
      {
        icon: Users,
        title: "Customer Insights",
        description: "\"Most questions come between 9-11 PM\"",
      },
      {
        icon: CreditCard,
        title: "Revenue Attribution",
        description: "\"$12,340 in sales from AI conversations this month\"",
      },
    ],
  },
];

export function FeatureTabs() {
  const [activeTab, setActiveTab] = useState(features[0].id);

  const activeFeature = features.find((f) => f.id === activeTab)!;

  return (
    <div className="space-y-8">
      {/* Tab Navigation */}
      <div className="flex flex-wrap justify-center gap-2">
        {features.map((feature) => (
          <button
            key={feature.id}
            onClick={() => setActiveTab(feature.id)}
            className={cn(
              "group flex items-center gap-2 rounded-full px-5 py-2.5 text-sm font-medium transition-all duration-300",
              activeTab === feature.id
                ? "bg-gradient-primary text-white shadow-lg shadow-gradient-start/30"
                : "bg-muted text-muted-foreground hover:bg-muted/80 hover:text-foreground"
            )}
          >
            <feature.icon
              className={cn(
                "h-4 w-4 transition-transform duration-300 group-hover:scale-110",
                activeTab === feature.id && "text-white"
              )}
            />
            {feature.label}
          </button>
        ))}
      </div>

      {/* Feature Content */}
      <div className="grid gap-8 lg:grid-cols-2 lg:items-center">
        {/* Left: Description */}
        <div className="space-y-6">
          <div className="inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-primary/10">
            <activeFeature.icon className="h-7 w-7 text-primary" />
          </div>
          
          <h3 className="font-display text-2xl font-bold md:text-3xl">
            {activeFeature.title}
          </h3>
          
          <p className="text-lg text-muted-foreground">
            {activeFeature.description}
          </p>

          <ul className="grid grid-cols-2 gap-3">
            {activeFeature.highlights.map((highlight, index) => (
              <li key={index} className="flex items-center gap-2">
                <div className="flex h-5 w-5 items-center justify-center rounded-full bg-gradient-primary/20">
                  <Check className="h-3 w-3 text-primary" />
                </div>
                <span className="text-sm font-medium">{highlight}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Right: Demo Preview */}
        <Card className="overflow-hidden border-border/50 bg-gradient-to-br from-muted/50 to-muted/30">
          <CardContent className="p-6">
            <div className="space-y-4">
              {activeFeature.demoPoints.map((point, index) => (
                <div
                  key={index}
                  className="group flex gap-4 rounded-xl border border-border/50 bg-card/50 p-4 transition-all duration-300 hover:border-primary/30 hover:bg-card"
                >
                  <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg bg-gradient-primary/10 transition-colors group-hover:bg-gradient-primary/20">
                    <point.icon className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <p className="font-semibold">{point.title}</p>
                    <p className="mt-1 text-sm text-muted-foreground">
                      {point.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

