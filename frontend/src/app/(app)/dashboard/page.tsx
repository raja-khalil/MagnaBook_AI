"use client";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { PlusCircle, Folder, ArrowRight } from "lucide-react";
import { projectsApi } from "@/services/api";
import { PageHeader } from "@/components/layout/PageHeader";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Spinner } from "@/components/ui/Spinner";
import type { Project } from "@/types";

const statusVariant: Record<Project["status"], "default" | "success" | "warning"> = {
  draft: "default",
  active: "success",
  archived: "warning",
};

const statusLabel: Record<Project["status"], string> = {
  draft: "Rascunho",
  active: "Ativo",
  archived: "Arquivado",
};

export default function DashboardPage() {
  const { data: projects, isLoading } = useQuery({
    queryKey: ["projects"],
    queryFn: projectsApi.list,
  });

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Dashboard"
        description="Seus projetos editoriais"
        action={
          <Link href="/projects/new">
            <Button>
              <PlusCircle size={16} />
              Novo Projeto
            </Button>
          </Link>
        }
      />

      {isLoading ? (
        <div className="flex justify-center py-20">
          <Spinner size="lg" className="text-brand-500" />
        </div>
      ) : !projects?.length ? (
        <div className="flex flex-col items-center gap-4 py-20 text-center">
          <Folder size={48} className="text-gray-300" />
          <div>
            <p className="font-medium text-gray-600">Nenhum projeto ainda</p>
            <p className="text-sm text-gray-400">Crie seu primeiro projeto para começar</p>
          </div>
          <Link href="/projects/new">
            <Button>
              <PlusCircle size={16} />
              Criar Projeto
            </Button>
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {projects.map((project) => (
            <Link key={project.id} href={`/projects/${project.id}/upload`}>
              <Card className="cursor-pointer transition-shadow hover:shadow-md">
                <CardBody>
                  <div className="flex items-start justify-between">
                    <div className="min-w-0 flex-1">
                      <p className="truncate font-semibold text-gray-900">{project.name}</p>
                      {project.description && (
                        <p className="mt-1 truncate text-sm text-gray-500">{project.description}</p>
                      )}
                    </div>
                    <ArrowRight size={16} className="ml-2 flex-shrink-0 text-gray-400" />
                  </div>
                  <div className="mt-4 flex items-center gap-2">
                    <Badge variant={statusVariant[project.status]}>{statusLabel[project.status]}</Badge>
                    <span className="text-xs text-gray-400">
                      {new Date(project.created_at).toLocaleDateString("pt-BR")}
                    </span>
                  </div>
                </CardBody>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
