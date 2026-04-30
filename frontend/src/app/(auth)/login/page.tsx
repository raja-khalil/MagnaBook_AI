"use client";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useRouter } from "next/navigation";
import { BookOpen } from "lucide-react";
import toast from "react-hot-toast";
import { authApi, extractError } from "@/services/api";
import { useAuthStore } from "@/store/auth";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Card, CardBody } from "@/components/ui/Card";

const schema = z.object({
  email: z.string().email("Email inválido"),
  password: z.string().min(6, "Mínimo 6 caracteres"),
});
type Fields = z.infer<typeof schema>;

export default function LoginPage() {
  const router = useRouter();
  const setAuth = useAuthStore((s) => s.setAuth);

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<Fields>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: Fields) => {
    try {
      const tokens = await authApi.login(data.email, data.password);
      const user = await authApi.me();
      setAuth(user, tokens.access_token, tokens.refresh_token);
      router.push("/dashboard");
    } catch (err) {
      toast.error(extractError(err));
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-brand-50 to-white p-4">
      <div className="w-full max-w-sm">
        <div className="mb-8 flex flex-col items-center gap-3">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-brand-500 shadow-lg">
            <BookOpen className="text-white" size={28} />
          </div>
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900">MagnaBook AI</h1>
            <p className="mt-1 text-sm text-gray-500">Entre na sua conta</p>
          </div>
        </div>

        <Card>
          <CardBody>
            <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
              <Input label="Email" type="email" placeholder="seu@email.com" error={errors.email?.message} {...register("email")} />
              <Input label="Senha" type="password" placeholder="••••••••" error={errors.password?.message} {...register("password")} />
              <Button type="submit" loading={isSubmitting} className="mt-2 w-full" size="lg">
                Entrar
              </Button>
            </form>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
