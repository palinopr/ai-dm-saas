import type { Metadata, Viewport } from "next";
import { Bricolage_Grotesque, Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";
import { cn } from "@/lib/utils";

const displayFont = Bricolage_Grotesque({
  subsets: ["latin"],
  variable: "--font-clash",
  display: "swap",
  weight: ["400", "500", "600", "700", "800"],
});

const bodyFont = Plus_Jakarta_Sans({
  subsets: ["latin"],
  variable: "--font-satoshi",
  display: "swap",
  weight: ["400", "500", "600", "700"],
});

export const metadata: Metadata = {
  metadataBase: new URL("https://replyhq.ai"),
  title: {
    default: "ReplyHQ - AI Sales Team for Instagram & TikTok DMs",
    template: "%s | ReplyHQ",
  },
  description:
    "Never miss a DM again. ReplyHQ's AI responds to Instagram and TikTok messages 24/7, turning conversations into revenue while you sleep. Shopify integrated.",
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
    title: "ReplyHQ - AI Sales Team for Instagram & TikTok DMs",
    description:
      "Never miss a DM again. AI responds 24/7, turning conversations into revenue.",
    images: [
      {
        url: "/images/og-image.png",
        width: 1200,
        height: 630,
        alt: "ReplyHQ - AI DM Automation for Instagram & TikTok",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    site: "@replyhq",
    creator: "@replyhq",
    title: "ReplyHQ - AI Sales Team for Instagram & TikTok DMs",
    description:
      "Never miss a DM again. AI responds 24/7, turning conversations into revenue.",
    images: ["/images/og-image.png"],
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#0a0a0a" },
  ],
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
        <link rel="apple-touch-icon" href="/images/og-image.png" />
      </head>
      <body
        className={cn(
          displayFont.variable,
          bodyFont.variable,
          "font-body antialiased"
        )}
      >
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
