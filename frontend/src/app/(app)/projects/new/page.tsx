"use client";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import { projectsApi, extractError } from "@/services/api";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardBody } from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";

const schema = z.object({
  name: z.string().min(3, "Mínimo 3 caracteres"),
  description: z.string().optional(),
});
type Fields = z.infer<typeof schema>;

export default function NewProjectPage() {
  const router = useRouter();
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<Fields>({
    resolver: zodResolver(schema),
  });

  const onSubmit = async (data: Fields) => {
    try {
      const project = await projectsApi.create(data);
      toast.success("Projeto criado!");
      router.push(`/projects/${project.id}/upload`);
    } catch (err) {
      toast.error(extractError(err));
    }
  };

  return (
    <div className="mx-auto max-w-lg flex flex-col gap-6">
      <PageHeader title="Criar Projeto" description="Configure seu novo projeto editorial" />

      <Card>
        <CardBody>
          <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-5">
            <Input
              label="Nome do Projeto"
              placeholder="Ex: Meu Livro de Receitas"
              error={errors.name?.message}
              {...register("name")}
            />
            <div className="flex flex-col gap-1">
              <label className="text-sm font-medium text-gray-700">Descrição (opcional)</label>
              <textarea
                className="rounded-lg border border-gray-300 px-3 py-2 text-sm placeholder:text-gray-400 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-brand-500"
                rows={3}
                placeholder="Breve descrição do projeto..."
                {...register("description")}
              />
            </div>
            <div className="flex gap-3 pt-2">
              <Button type="button" variant="secondary" onClick={() => router.back()}>
                Cancelar
              </Button>
              <Button type="submit" loading={isSubmitting}>
                Criar e Continuar
              </Button>
            </div>
          </form>
        </CardBody>
      </Card>
    </div>
  );
}
