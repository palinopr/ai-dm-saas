export const faqs = [
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

export function FAQSchema() {
  return (
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
  );
}

