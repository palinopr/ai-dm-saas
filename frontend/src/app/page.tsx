import type { Metadata } from "next";
import { Suspense } from "react";
import dynamic from "next/dynamic";
import {
  Navigation,
  Hero,
  StatsBar,
  Footer,
} from "@/components/marketing";
import { JsonLd } from "@/components/seo";
import { FAQSchema } from "@/components/marketing";

// Lazy load below-the-fold components
const Agitation = dynamic(() => import("@/components/marketing").then(mod => ({ default: mod.Agitation })), {
  loading: () => <div className="h-96" />,
});

const Solution = dynamic(() => import("@/components/marketing").then(mod => ({ default: mod.Solution })), {
  loading: () => <div className="h-96" />,
});

const SocialProof = dynamic(() => import("@/components/marketing").then(mod => ({ default: mod.SocialProof })), {
  loading: () => <div className="h-96" />,
});

const Pricing = dynamic(() => import("@/components/marketing").then(mod => ({ default: mod.Pricing })), {
  loading: () => <div className="h-96" />,
});

const FAQ = dynamic(() => import("@/components/marketing").then(mod => ({ default: mod.FAQ })), {
  loading: () => <div className="h-96" />,
});

const FinalCTA = dynamic(() => import("@/components/marketing").then(mod => ({ default: mod.FinalCTA })), {
  loading: () => <div className="h-96" />,
});

export const metadata: Metadata = {
  title: "ReplyHQ - AI Sales Team for Instagram & TikTok DMs | Turn DMs Into Sales",
  description:
    "Never miss a sale again. ReplyHQ's AI responds to Instagram and TikTok DMs 24/7, answers product questions instantly, and turns conversations into revenue. Free 14-day trial.",
  openGraph: {
    title: "ReplyHQ - AI Sales Team for Instagram & TikTok DMs",
    description:
      "Never miss a sale again. AI responds to Instagram and TikTok DMs 24/7, turning conversations into revenue while you sleep.",
    url: "https://replyhq.ai",
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
    title: "ReplyHQ - AI Sales Team for Instagram & TikTok DMs",
    description:
      "Never miss a sale again. AI responds to Instagram and TikTok DMs 24/7, turning conversations into revenue.",
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
      <FAQSchema />
      <div className="flex min-h-screen flex-col">
        <Navigation />
        <main className="flex-1">
          <Hero />
          <StatsBar />
          <Suspense fallback={<div className="h-96" />}>
            <Agitation />
          </Suspense>
          <Suspense fallback={<div className="h-96" />}>
            <Solution />
          </Suspense>
          <Suspense fallback={<div className="h-96" />}>
            <SocialProof />
          </Suspense>
          <Suspense fallback={<div className="h-96" />}>
            <Pricing />
          </Suspense>
          <Suspense fallback={<div className="h-96" />}>
            <FAQ />
          </Suspense>
          <Suspense fallback={<div className="h-96" />}>
            <FinalCTA />
          </Suspense>
        </main>
        <Footer />
      </div>
    </>
  );
}
