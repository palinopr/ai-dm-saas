import Script from "next/script";

type JsonLdType = "organization" | "softwareApplication" | "offers";

interface JsonLdProps {
  type: JsonLdType;
}

const schemas: Record<JsonLdType, object> = {
  organization: {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: "ReplyHQ",
    url: "https://replyhq.ai",
    logo: "https://replyhq.ai/images/logo.png",
    description:
      "AI-powered DM automation that turns Instagram and TikTok conversations into sales.",
    sameAs: ["https://twitter.com/replyhq", "https://instagram.com/replyhq"],
  },
  softwareApplication: {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    name: "ReplyHQ",
    applicationCategory: "BusinessApplication",
    operatingSystem: "Web",
    description:
      "AI-powered DM automation that turns Instagram and TikTok conversations into sales.",
    offers: {
      "@type": "AggregateOffer",
      lowPrice: "63",
      highPrice: "399",
      priceCurrency: "USD",
      offerCount: 3,
    },
  },
  offers: {
    "@context": "https://schema.org",
    "@type": "ItemList",
    itemListElement: [
      {
        "@type": "Offer",
        position: 1,
        name: "Starter Plan",
        description: "Perfect for small stores getting started",
        price: "63",
        priceCurrency: "USD",
        availability: "https://schema.org/InStock",
      },
      {
        "@type": "Offer",
        position: 2,
        name: "Growth Plan",
        description: "For growing brands ready to scale",
        price: "119",
        priceCurrency: "USD",
        availability: "https://schema.org/InStock",
      },
      {
        "@type": "Offer",
        position: 3,
        name: "Enterprise Plan",
        description: "For high-volume stores",
        price: "319",
        priceCurrency: "USD",
        availability: "https://schema.org/InStock",
      },
    ],
  },
};

export function JsonLd({ type }: JsonLdProps) {
  const schema = schemas[type];
  return (
    <Script
      id={`json-ld-${type}`}
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
      strategy="afterInteractive"
    />
  );
}
