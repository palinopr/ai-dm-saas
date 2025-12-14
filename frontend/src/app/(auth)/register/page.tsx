import { RegisterForm } from "@/components/auth";

export default function RegisterPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-bold tracking-tight text-gray-900">
            AI DM Automation
          </h1>
          <h2 className="mt-2 text-xl text-gray-600">
            Create your account
          </h2>
        </div>
        <div className="rounded-lg bg-white p-8 shadow">
          <RegisterForm />
        </div>
      </div>
    </div>
  );
}
