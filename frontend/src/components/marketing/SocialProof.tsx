import { Star } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import type { Testimonial } from "@/types/marketing";

const testimonials: Testimonial[] = [
  {
    quote:
      "We went from responding to 20% of DMs to 100%. Sales from Instagram increased 40% in the first month.",
    author: "Sarah Chen",
    role: "Founder",
    company: "GlowBox Cosmetics",
    initials: "SC",
  },
  {
    quote:
      "The AI actually understands our products better than some of our staff. It's like having a 24/7 sales team.",
    author: "Marcus Williams",
    role: "Owner",
    company: "UrbanThreads",
    initials: "MW",
  },
  {
    quote:
      "Setup took 10 minutes. ROI was immediate. Best tool we've added this year.",
    author: "Jessica Park",
    role: "CMO",
    company: "PetPalace",
    initials: "JP",
  },
];

const companyLogos = [
  { name: "GlowBox", initials: "GB" },
  { name: "UrbanThreads", initials: "UT" },
  { name: "PetPalace", initials: "PP" },
  { name: "FitGear", initials: "FG" },
  { name: "HomeStyle", initials: "HS" },
  { name: "TechWear", initials: "TW" },
];

export function SocialProof() {
  return (
    <section id="testimonials" className="py-20 md:py-28">
      <div className="container mx-auto max-w-6xl px-4">
        {/* Headline */}
        <div className="mx-auto max-w-3xl text-center">
          <p className="mb-4 text-sm font-semibold uppercase tracking-wider text-primary">
            Social Proof
          </p>
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl md:text-5xl">
            See what our customers are saying
          </h2>
        </div>

        {/* Testimonial Cards */}
        <div className="mt-16 grid gap-6 md:grid-cols-3">
          {testimonials.map((testimonial, index) => (
            <Card key={index} className="relative">
              <CardContent className="pt-6">
                {/* Stars */}
                <div className="mb-4 flex gap-1">
                  {[...Array(5)].map((_, i) => (
                    <Star
                      key={i}
                      className="h-4 w-4 fill-yellow-400 text-yellow-400"
                    />
                  ))}
                </div>

                {/* Quote */}
                <blockquote className="mb-6 text-lg">
                  &quot;{testimonial.quote}&quot;
                </blockquote>

                {/* Author */}
                <div className="flex items-center gap-3">
                  {/* PLACEHOLDER: Customer photo */}
                  <Avatar>
                    <AvatarFallback className="bg-primary/10 text-primary">
                      {testimonial.initials}
                    </AvatarFallback>
                  </Avatar>
                  <div>
                    <p className="font-semibold">{testimonial.author}</p>
                    <p className="text-sm text-muted-foreground">
                      {testimonial.role}, {testimonial.company}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Company Logos */}
        <div className="mt-20">
          <p className="mb-8 text-center text-sm font-medium text-muted-foreground">
            Trusted by leading e-commerce brands
          </p>
          {/* PLACEHOLDER: Company logos - replace with actual logos */}
          <div className="flex flex-wrap items-center justify-center gap-8 md:gap-12">
            {companyLogos.map((logo, index) => (
              <div
                key={index}
                className="flex h-12 w-24 items-center justify-center rounded-lg bg-muted text-sm font-medium text-muted-foreground"
              >
                {logo.initials}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
