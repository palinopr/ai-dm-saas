import { redirect } from 'next/navigation';

import { getUser } from '@/libs/supabase/server';

export default async function CenteredLayout(props: { children: React.ReactNode }) {
  const user = await getUser();

  if (user) {
    redirect('/dashboard');
  }

  return (
    <div className="flex min-h-screen items-center justify-center">
      {props.children}
    </div>
  );
}
