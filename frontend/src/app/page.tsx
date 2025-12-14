import type { Metadata } from "next";
import {
  Navigation,
  Hero,
  Agitation,
  Solution,
  SocialProof,
  Pricing,
  FinalCTA,
  Footer,
} from "@/components/marketing";
import { JsonLd } from "@/components/seo";

export const metadata: Metadata = {
  title: "AI DM Automation for Instagram & TikTok | Turn DMs Into Sales",
  description:
    "Never miss a sale again. Our AI responds to Instagram and TikTok DMs 24/7, answers product questions instantly, and turns conversations into revenue. Free 14-day trial.",
  openGraph: {
    title: "AI DM Automation for Instagram & TikTok | Turn DMs Into Sales",
    description:
      "Never miss a sale again. Our AI responds to Instagram and TikTok DMs 24/7, answers product questions instantly, and turns conversations into revenue.",
    url: "https://replyhq.ai",
    images: [
      {
        url: "/images/og-image.png",
        width: 1200,
        height: 630,
        alt: "ReplyHQ - Turn DMs Into Sales",
      },
    ],
  },
  twitter: {
    title: "AI DM Automation for Instagram & TikTok",
    description:
      "Never miss a sale again. Our AI responds to Instagram and TikTok DMs 24/7.",
    images: ["/images/og-image.png"],
  },
  alternates: {
    canonical: "https://replyhq.ai",
  },
};

export default function HomePage() {
  return (
    <>
      <JsonLd type="organization" />
      <JsonLd type="softwareApplication" />
      <JsonLd type="offers" />
      <div className="flex min-h-screen flex-col">
        <Navigation />
        <main className="flex-1">
          <Hero />
          <Agitation />
          <Solution />
          <SocialProof />
          <Pricing />
          <FinalCTA />
        </main>
        <Footer />
      </div>
    </>
  );
}
