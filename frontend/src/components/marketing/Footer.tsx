"use client";

import { useState } from "react";
import Link from "next/link";
import { Sparkles, Twitter, Instagram, Linkedin, ArrowRight, Mail } from "lucide-react";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface FooterColumn {
  title: string;
  links: { label: string; href: string }[];
}

const footerColumns: FooterColumn[] = [
  {
    title: "Product",
    links: [
      { label: "Features", href: "#features" },
      { label: "Pricing", href: "#pricing" },
      { label: "Integrations", href: "#" },
      { label: "Changelog", href: "#" },
    ],
  },
  {
    title: "Company",
    links: [
      { label: "About", href: "#" },
      { label: "Blog", href: "#" },
      { label: "Careers", href: "#" },
      { label: "Contact", href: "#" },
    ],
  },
  {
    title: "Legal",
    links: [
      { label: "Privacy Policy", href: "#" },
      { label: "Terms of Service", href: "#" },
      { label: "Cookie Policy", href: "#" },
    ],
  },
];

const socialLinks = [
  { icon: Twitter, href: "#", label: "Twitter" },
  { icon: Instagram, href: "#", label: "Instagram" },
  { icon: Linkedin, href: "#", label: "LinkedIn" },
];

export function Footer() {
  const currentYear = new Date().getFullYear();
  const [email, setEmail] = useState("");
  const [subscribed, setSubscribed] = useState(false);

  const handleSubscribe = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      setSubscribed(true);
      setEmail("");
    }
  };

  return (
    <footer className="relative border-t border-border/50 bg-muted/30">
      {/* Subtle gradient */}
      <div className="absolute inset-0 bg-gradient-to-t from-background via-background to-transparent" />
      
      <div className="container relative mx-auto max-w-6xl px-4 py-12 md:py-16">
        <div className="grid gap-12 lg:grid-cols-2">
          {/* Left Side - Brand & Newsletter */}
          <div className="space-y-8">
            {/* Logo */}
            <Link href="/" className="inline-flex items-center gap-2 group">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-primary transition-transform duration-300 group-hover:scale-105">
                <Sparkles className="h-5 w-5 text-white" />
              </div>
              <span className="font-display text-2xl font-bold">ReplyHQ</span>
            </Link>
            
            <p className="max-w-sm text-muted-foreground">
              AI-powered DM automation that turns social media conversations
              into paying customers. 24/7 intelligent responses for Instagram,
              TikTok, and WhatsApp.
            </p>

            {/* Newsletter */}
            <div className="max-w-sm">
              <h4 className="font-display text-sm font-semibold mb-3 flex items-center gap-2">
                <Mail className="h-4 w-4 text-primary" />
                Stay Updated
              </h4>
              {subscribed ? (
                <div className="rounded-lg bg-gradient-primary/10 border border-primary/20 px-4 py-3">
                  <p className="text-sm font-medium text-primary">
                    Thanks for subscribing! We&apos;ll keep you posted.
                  </p>
                </div>
              ) : (
                <form onSubmit={handleSubscribe} className="flex gap-2">
                  <Input
                    type="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="flex-1 bg-background border-border/50"
                    required
                  />
                  <Button type="submit" size="icon" className="bg-gradient-primary hover:opacity-90">
                    <ArrowRight className="h-4 w-4" />
                  </Button>
                </form>
              )}
            </div>

            {/* Social Links */}
            <div className="flex gap-3">
              {socialLinks.map((social) => (
                <Link
                  key={social.label}
                  href={social.href}
                  className="flex h-10 w-10 items-center justify-center rounded-lg border border-border/50 bg-background text-muted-foreground transition-all duration-300 hover:border-primary/30 hover:text-primary hover:shadow-sm"
                  aria-label={social.label}
                >
                  <social.icon className="h-4 w-4" />
                </Link>
              ))}
            </div>
          </div>

          {/* Right Side - Links */}
          <div className="grid grid-cols-2 gap-8 sm:grid-cols-3">
            {footerColumns.map((column) => (
              <div key={column.title}>
                <h3 className="font-display text-sm font-semibold mb-4">{column.title}</h3>
                <ul className="space-y-3">
                  {column.links.map((link) => (
                    <li key={link.label}>
                      <Link
                        href={link.href}
                        className="text-sm text-muted-foreground transition-colors hover:text-foreground"
                      >
                        {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        <Separator className="my-8 bg-border/50" />

        {/* Copyright */}
        <div className="flex flex-col items-center justify-between gap-4 text-center md:flex-row md:text-left">
          <p className="text-sm text-muted-foreground">
            &copy; {currentYear} ReplyHQ. All rights reserved.
          </p>
          <p className="text-sm text-muted-foreground">
            Built with{" "}
            <span className="gradient-text font-medium">love</span>{" "}
            for e-commerce brands
          </p>
        </div>
      </div>
    </footer>
  );
}
