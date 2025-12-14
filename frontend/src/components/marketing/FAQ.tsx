"use client";

import { useState } from "react";
import { ChevronDown, HelpCircle, MessageCircle } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { faqs } from "./FAQSchema";

interface FAQItemProps {
  question: string;
  answer: string;
  isOpen: boolean;
  onClick: () => void;
  index: number;
}

function FAQItem({ question, answer, isOpen, onClick, index }: FAQItemProps) {
  return (
    <Card 
      className={cn(
        "overflow-hidden border-border/50 transition-all duration-300",
        isOpen 
          ? "border-primary/30 shadow-md shadow-primary/5" 
          : "hover:border-border"
      )}
    >
      <CardContent className="p-0">
        <button
          onClick={onClick}
          className="flex w-full items-start justify-between gap-4 p-5 text-left transition-colors hover:bg-muted/50"
        >
          <div className="flex items-start gap-3">
            <div className={cn(
              "mt-0.5 flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-md text-xs font-semibold transition-colors",
              isOpen 
                ? "bg-gradient-primary text-white" 
                : "bg-muted text-muted-foreground"
            )}>
              {index + 1}
            </div>
            <h3 className="font-display text-base font-semibold pr-4">{question}</h3>
          </div>
          <ChevronDown
            className={cn(
              "mt-1 h-5 w-5 flex-shrink-0 text-muted-foreground transition-transform duration-300",
              isOpen && "rotate-180 text-primary"
            )}
          />
        </button>
        <div
          className={cn(
            "grid transition-all duration-300",
            isOpen ? "grid-rows-[1fr]" : "grid-rows-[0fr]"
          )}
        >
          <div className="overflow-hidden">
            <div className="px-5 pb-5 pl-14">
              <p className="text-muted-foreground leading-relaxed">{answer}</p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  // Split FAQs into two columns
  const midpoint = Math.ceil(faqs.length / 2);
  const leftColumn = faqs.slice(0, midpoint);
  const rightColumn = faqs.slice(midpoint);

  return (
    <section className="relative py-20 md:py-28 overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-muted/30 via-background to-background" />
      
      <div className="container relative mx-auto max-w-6xl px-4">
        {/* Headline */}
        <div className="mx-auto max-w-3xl text-center mb-12">
          <p className="mb-4 inline-flex items-center gap-2 rounded-full bg-gradient-primary/10 px-4 py-1.5 text-sm font-semibold text-primary">
            <HelpCircle className="h-4 w-4" />
            FAQ
          </p>
          <h2 className="font-display text-3xl font-bold tracking-tight sm:text-4xl md:text-5xl">
            Got Questions?{" "}
            <span className="gradient-text">We&apos;ve Got Answers</span>
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Everything you need to know about ReplyHQ and AI DM automation.
          </p>
        </div>

        {/* FAQ Grid - Two Columns on Desktop */}
        <div className="grid gap-4 lg:grid-cols-2">
          {/* Left Column */}
          <div className="space-y-4">
            {leftColumn.map((faq, index) => (
              <FAQItem
                key={index}
                question={faq.question}
                answer={faq.answer}
                isOpen={openIndex === index}
                onClick={() => setOpenIndex(openIndex === index ? null : index)}
                index={index}
              />
            ))}
          </div>
          
          {/* Right Column */}
          <div className="space-y-4">
            {rightColumn.map((faq, index) => {
              const actualIndex = index + midpoint;
              return (
                <FAQItem
                  key={actualIndex}
                  question={faq.question}
                  answer={faq.answer}
                  isOpen={openIndex === actualIndex}
                  onClick={() => setOpenIndex(openIndex === actualIndex ? null : actualIndex)}
                  index={actualIndex}
                />
              );
            })}
          </div>
        </div>

        {/* Contact CTA */}
        <div className="mt-12 text-center">
          <div className="inline-flex items-center gap-3 rounded-full border border-border/50 bg-muted/30 px-6 py-3">
            <MessageCircle className="h-5 w-5 text-primary" />
            <p className="text-muted-foreground">
              Still have questions?{" "}
              <a
                href="mailto:support@replyhq.ai"
                className="font-semibold text-primary hover:underline"
              >
                Contact our team
              </a>
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
