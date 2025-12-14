import type { Metadata, Viewport } from "next";
import "./globals.css";
import { Providers } from "./providers";

export const metadata: Metadata = {
  metadataBase: new URL("https://replyhq.ai"),
  title: {
    default: "ReplyHQ",
    template: "%s | ReplyHQ",
  },
  description: "AI-powered DM Automation SaaS for e-commerce businesses",
  keywords: [
    // Primary keywords
    "Instagram DM automation",
    "TikTok DM bot",
    "AI sales assistant",
    "e-commerce automation",
    "Shopify Instagram integration",
    // Secondary keywords
    "Instagram automation for e-commerce",
    "TikTok customer service automation",
    "AI chatbot for Instagram",
    "automated DM responses",
    "Instagram business automation",
    // Long-tail keywords (easier to rank)
    "how to automate Instagram DMs for Shopify",
    "best AI bot for Instagram business messages",
    "TikTok DM automation for online stores",
    "Instagram DM management tool for e-commerce",
    "automated customer service for Instagram shop",
    "AI assistant for Instagram direct messages",
    "24/7 Instagram customer support automation",
    "Shopify TikTok DM integration",
  ],
  authors: [{ name: "ReplyHQ Team" }],
  creator: "ReplyHQ",
  publisher: "ReplyHQ",
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://replyhq.ai",
    siteName: "ReplyHQ",
    images: [
      {
        url: "/images/og-image.png",
        width: 1200,
        height: 630,
        alt: "ReplyHQ - AI DM Automation",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    site: "@replyhq",
    creator: "@replyhq",
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#000000" },
  ],
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.Node;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
        <link rel="apple-touch-icon" href="/images/og-image.png" />
      </head>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
