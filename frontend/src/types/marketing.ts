export interface NavLink {
  label: string;
  href: string;
}

export interface PainPoint {
  title: string;
  description: string;
}

export interface Feature {
  icon: "clock" | "cart" | "chart";
  title: string;
  description: string;
}

export interface Testimonial {
  quote: string;
  author: string;
  role: string;
  company: string;
  initials: string;
}

export interface PricingTier {
  name: string;
  monthlyPrice: number;
  annualPrice: number;
  description: string;
  features: string[];
  highlighted?: boolean;
  messageLimit: string;
  accountLimit: string;
}

export interface FooterColumn {
  title: string;
  links: NavLink[];
}
