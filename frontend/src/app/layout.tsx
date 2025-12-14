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
    "Instagram DM automation",
    "TikTok DM bot",
    "AI sales assistant",
    "e-commerce automation",
    "Shopify Instagram integration",
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
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
