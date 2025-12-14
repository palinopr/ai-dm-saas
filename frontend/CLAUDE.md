# Frontend Constitution: Next.js 15 & React 19

## 1. Key Files & Structure

- **`src/app/`**: The Next.js App Router. All pages and layouts live here.
- **`src/components/`**: Reusable React components. Organized by feature.
- **`src/lib/api.ts`**: The API client for communicating with our backend.
- **`src/hooks/`**: Custom React hooks.
- **`src/types/`**: Shared TypeScript types and interfaces.

## 2. Core Patterns & Standards

- **React Query:** All data fetching from our backend MUST be handled with React Query (`@tanstack/react-query`). This manages caching, refetching, and server state.
- **Functional Components & Hooks:** All components MUST be functional components. All stateful logic MUST be encapsulated in hooks.
- **shadcn/ui:** Use `shadcn/ui` for all base UI components (buttons, inputs, etc.). Do not build these from scratch.
- **Server Components:** Use React Server Components (RSCs) wherever possible for performance.
- **Type Safety:** All props, state, and API responses MUST be strongly typed.
