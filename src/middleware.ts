import {
  type NextFetchEvent,
  type NextRequest,
  NextResponse,
} from 'next/server';
import createMiddleware from 'next-intl/middleware';

import { updateSession } from '@/libs/supabase/middleware';
import { AllLocales, AppConfig } from '@/utils/AppConfig';

const intlMiddleware = createMiddleware({
  locales: AllLocales,
  localePrefix: AppConfig.localePrefix,
  defaultLocale: AppConfig.defaultLocale,
});

const protectedRoutes = ['/dashboard', '/onboarding', '/api'];
const authRoutes = ['/sign-in', '/sign-up'];

function isProtectedRoute(pathname: string): boolean {
  return protectedRoutes.some(route =>
    pathname.includes(route),
  );
}

function isAuthRoute(pathname: string): boolean {
  return authRoutes.some(route =>
    pathname.includes(route),
  );
}

export default async function middleware(
  request: NextRequest,
  _event: NextFetchEvent,
) {
  const { pathname } = request.nextUrl;

  // Handle auth routes and protected routes
  if (isAuthRoute(pathname) || isProtectedRoute(pathname)) {
    const { supabaseResponse, user } = await updateSession(request);

    // If user is on auth route but already logged in, redirect to dashboard
    if (isAuthRoute(pathname) && user) {
      const locale = pathname.match(/^\/([a-z]{2})\//)?.at(1) ?? '';
      const dashboardUrl = locale ? `/${locale}/dashboard` : '/dashboard';
      return NextResponse.redirect(new URL(dashboardUrl, request.url));
    }

    // If user is on protected route but not logged in, redirect to sign-in
    if (isProtectedRoute(pathname) && !user) {
      const locale = pathname.match(/^\/([a-z]{2})\//)?.at(1) ?? '';
      const signInUrl = locale ? `/${locale}/sign-in` : '/sign-in';
      return NextResponse.redirect(new URL(signInUrl, request.url));
    }

    // Apply intl middleware to the supabase response
    const intlResponse = intlMiddleware(request);

    // Merge cookies from supabase response
    supabaseResponse.cookies.getAll().forEach((cookie) => {
      intlResponse.cookies.set(cookie.name, cookie.value, cookie);
    });

    return intlResponse;
  }

  return intlMiddleware(request);
}

export const config = {
  matcher: ['/((?!.+\\.[\\w]+$|_next|monitoring).*)', '/', '/(api|trpc)(.*)'],
};
