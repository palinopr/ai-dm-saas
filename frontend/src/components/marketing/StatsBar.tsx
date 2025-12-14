import { Clock, ShoppingCart, MessageSquare, Code2 } from "lucide-react";

const valueProps = [
  {
    icon: Clock,
    title: "24/7 Instant Responses",
    description: "AI never sleeps",
  },
  {
    icon: ShoppingCart,
    title: "Shopify Connected",
    description: "Real-time product data",
  },
  {
    icon: MessageSquare,
    title: "Multi-Platform",
    description: "Instagram, TikTok, WhatsApp",
  },
  {
    icon: Code2,
    title: "No Code Required",
    description: "Setup in minutes",
  },
];

export function StatsBar() {
  return (
    <section className="relative border-y border-border/50 bg-muted/30 py-8 md:py-10">
      {/* Subtle gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-r from-gradient-start/5 via-transparent to-gradient-end/5" />
      
      <div className="container relative mx-auto max-w-6xl px-4">
        <div className="grid grid-cols-2 gap-6 md:grid-cols-4 md:gap-8">
          {valueProps.map((prop, index) => (
            <div
              key={index}
              className="group flex flex-col items-center text-center md:flex-row md:text-left"
            >
              {/* Icon */}
              <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-primary/10 transition-all duration-300 group-hover:bg-gradient-primary/20 md:mb-0 md:mr-4">
                <prop.icon className="h-5 w-5 text-primary transition-transform duration-300 group-hover:scale-110" />
              </div>
              
              {/* Text */}
              <div>
                <h3 className="font-display text-sm font-semibold md:text-base">
                  {prop.title}
                </h3>
                <p className="mt-0.5 text-xs text-muted-foreground md:text-sm">
                  {prop.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

