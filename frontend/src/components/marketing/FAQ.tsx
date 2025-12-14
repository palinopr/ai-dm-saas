"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { faqs } from "./FAQSchema";

function FAQItem({ question, answer, isOpen, onClick }: {
  question: string;
  answer: string;
  isOpen: boolean;
  onClick: () => void;
}) {
  return (
    <Card className="mb-4">
      <CardContent className="p-0">
        <button
          onClick={onClick}
          className="flex w-full items-center justify-between p-6 text-left transition-colors hover:bg-muted/50"
        >
          <h3 className="text-lg font-semibold pr-4">{question}</h3>
          <ChevronDown
            className={`h-5 w-5 flex-shrink-0 text-muted-foreground transition-transform ${
              isOpen ? "rotate-180" : ""
            }`}
          />
        </button>
        {isOpen && (
          <div className="px-6 pb-6">
            <p className="text-base text-muted-foreground">{answer}</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section className="py-20 md:py-28">
        <div className="container mx-auto max-w-4xl px-4">
          {/* Headline */}
          <div className="mb-12 text-center">
            <p className="mb-4 text-sm font-semibold uppercase tracking-wider text-primary">
              Frequently Asked Questions
            </p>
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl md:text-5xl">
              Everything You Need to Know About Instagram & TikTok DM Automation
            </h2>
          </div>

          {/* FAQ List */}
          <div className="w-full">
            {faqs.map((faq, index) => (
              <FAQItem
                key={index}
                question={faq.question}
                answer={faq.answer}
                isOpen={openIndex === index}
                onClick={() => setOpenIndex(openIndex === index ? null : index)}
              />
            ))}
          </div>

          {/* CTA */}
          <div className="mt-12 text-center">
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
      </section>
  );
}
