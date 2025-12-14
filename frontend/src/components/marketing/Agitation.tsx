import { Clock, DollarSign, MessageSquareX } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

const painPoints = [
  {
    icon: Clock,
    stat: "85%",
    title: "of customers expect a response within 10 minutes",
    description: "You can't be online 24/7.",
  },
  {
    icon: DollarSign,
    stat: "$3,000+",
    title: "per month for a social media manager",
    description: "Hiring help is expensive.",
  },
  {
    icon: MessageSquareX,
    stat: "Generic",
    title: "auto-replies annoy customers",
    description: "And kill your sales.",
  },
];

export function Agitation() {
  return (
    <section className="py-20 md:py-28">
      <div className="container mx-auto max-w-6xl px-4">
        {/* Headline */}
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl md:text-5xl">
            Your DMs are a goldmine.{" "}
            <span className="text-muted-foreground">
              You&apos;re just not equipped to mine it.
            </span>
          </h2>
        </div>

        {/* Pain Point Cards */}
        <div className="mt-16 grid gap-6 md:grid-cols-3">
          {painPoints.map((point, index) => (
            <Card
              key={index}
              className="relative overflow-hidden border-destructive/20 bg-destructive/5"
            >
              <CardContent className="pt-6">
                <div className="mb-4 inline-flex rounded-lg bg-destructive/10 p-3">
                  <point.icon className="h-6 w-6 text-destructive" />
                </div>
                <div className="mb-2 text-3xl font-bold text-destructive">
                  {point.stat}
                </div>
                <p className="text-lg font-semibold">{point.title}</p>
                <p className="mt-2 text-muted-foreground">{point.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
