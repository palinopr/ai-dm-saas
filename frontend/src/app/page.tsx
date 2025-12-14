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

export default function HomePage() {
  return (
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
  );
}
