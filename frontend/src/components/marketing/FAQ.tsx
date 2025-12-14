import { ChevronDown } from "lucide-react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const faqs = [
  {
    question: "How does Instagram DM automation work?",
    answer:
      "Our AI connects to your Instagram Business account through the official Meta API. When someone sends a DM, our AI instantly analyzes the message, checks your Shopify inventory, and responds with accurate information about products, pricing, shipping, and more. It works 24/7 without any manual intervention.",
  },
  {
    question: "Is TikTok DM automation allowed by TikTok?",
    answer:
      "Yes! Our platform complies with TikTok's API guidelines and terms of service. We use official TikTok Business APIs to ensure your account stays safe and compliant. TikTok encourages businesses to use automation tools to improve customer service response times.",
  },
  {
    question: "Can the AI bot handle complex customer questions?",
    answer:
      "Absolutely. Our AI is trained on e-commerce conversations and can handle product questions, shipping inquiries, return policies, discount codes, and order tracking. If a question is too complex, it can seamlessly hand off to a human team member with full conversation context.",
  },
  {
    question: "How do I integrate with my Shopify store?",
    answer:
      "Integration takes less than 5 minutes. Simply install our Shopify app, connect your Instagram and TikTok Business accounts, and our AI will automatically sync your product catalog, inventory levels, and order data. No coding required.",
  },
  {
    question: "Will customers know they're talking to an AI?",
    answer:
      "You can choose! Our AI can introduce itself as an automated assistant, or you can configure it to respond naturally without disclosure. We recommend transparency, as customers appreciate fast, accurate responses regardless of whether it's AI or human.",
  },
  {
    question: "What happens if the AI doesn't know the answer?",
    answer:
      "If our AI encounters a question it can't confidently answer, it will politely let the customer know and offer to connect them with your team. You'll receive a notification and can take over the conversation seamlessly from where the AI left off.",
  },
  {
    question: "How much does Instagram DM automation cost?",
    answer:
      "Plans start at $63/month for up to 500 conversations. This includes unlimited Instagram and TikTok accounts, Shopify integration, and 24/7 AI responses. We offer a 14-day free trial with no credit card required so you can test it risk-free.",
  },
  {
    question: "Can I use this for multiple Instagram and TikTok accounts?",
    answer:
      "Yes! All plans include support for unlimited Instagram and TikTok Business accounts. Perfect for agencies managing multiple clients or brands with multiple social media profiles.",
  },
];

export function FAQ() {
  return (
    <>
      {/* FAQ Schema for SEO */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faqs.map((faq) => ({
              "@type": "Question",
              "name": faq.question,
              "acceptedAnswer": {
                "@type": "Answer",
                "text": faq.answer,
              },
            })),
          }),
        }}
      />

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

          {/* FAQ Accordion */}
          <Accordion type="single" collapsible className="w-full">
            {faqs.map((faq, index) => (
              <AccordionItem key={index} value={`item-${index}`}>
                <AccordionTrigger className="text-left text-lg font-semibold">
                  {faq.question}
                </AccordionTrigger>
                <AccordionContent className="text-base text-muted-foreground">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>

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
    </>
  );
}
