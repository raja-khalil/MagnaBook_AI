"use client";
import { useState, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import { useDropzone } from "react-dropzone";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { UploadCloud, FileText, Trash2 } from "lucide-react";
import toast from "react-hot-toast";
import { filesApi, extractError } from "@/services/api";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardBody } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Spinner } from "@/components/ui/Spinner";
import type { ProjectFile } from "@/types";

function formatBytes(bytes: number) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

const statusBadge: Record<ProjectFile["status"], { label: string; variant: "default" | "info" | "success" | "error" }> = {
  pending: { label: "Pendente", variant: "default" },
  processing: { label: "Processando", variant: "info" },
  ready: { label: "Pronto", variant: "success" },
  error: { label: "Erro", variant: "error" },
};

export default function UploadPage() {
  const { id: projectId } = useParams<{ id: string }>();
  const router = useRouter();
  const qc = useQueryClient();
  const [uploadProgress, setUploadProgress] = useState(0);

  const { data: files, isLoading } = useQuery({
    queryKey: ["files", projectId],
    queryFn: () => filesApi.list(projectId),
  });

  const uploadMutation = useMutation({
    mutationFn: (file: File) => filesApi.upload(projectId, file, setUploadProgress),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["files", projectId] });
      toast.success("Arquivo enviado!");
      setUploadProgress(0);
    },
    onError: (err) => {
      toast.error(extractError(err));
      setUploadProgress(0);
    },
  });

  const onDrop = useCallback((accepted: File[]) => {
    if (accepted[0]) uploadMutation.mutate(accepted[0]);
  }, [uploadMutation]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "text/plain": [".txt"], "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"] },
    maxFiles: 1,
    disabled: uploadMutation.isPending,
  });

  const readyFile = files?.find((f) => f.status === "ready");

  return (
    <div className="mx-auto max-w-2xl flex flex-col gap-6">
      <PageHeader title="Upload do Documento" description="Envie o documento base para geração do livro (.txt ou .docx)" />

      <Card>
        <CardBody>
          <div
            {...getRootProps()}
            className={`flex flex-col items-center gap-3 rounded-xl border-2 border-dashed p-10 text-center transition-colors cursor-pointer
              ${isDragActive ? "border-brand-400 bg-brand-50" : "border-gray-300 hover:border-brand-400 hover:bg-gray-50"}`}
          >
            <input {...getInputProps()} />
            {uploadMutation.isPending ? (
              <div className="flex flex-col items-center gap-3">
                <Spinner size="lg" className="text-brand-500" />
                <p className="text-sm text-gray-600">{uploadProgress}% enviado...</p>
              </div>
            ) : (
              <>
                <UploadCloud size={40} className="text-gray-400" />
                <div>
                  <p className="font-medium text-gray-700">
                    {isDragActive ? "Solte o arquivo aqui" : "Arraste ou clique para enviar"}
                  </p>
                  <p className="mt-1 text-xs text-gray-400">Suporta .txt e .docx — máx. 50MB</p>
                </div>
              </>
            )}
          </div>
        </CardBody>
      </Card>

      {isLoading ? (
        <div className="flex justify-center py-4"><Spinner className="text-brand-500" /></div>
      ) : files && files.length > 0 ? (
        <Card>
          <CardBody>
            <p className="mb-3 text-sm font-medium text-gray-700">Arquivos enviados</p>
            <ul className="flex flex-col gap-2">
              {files.map((file) => {
                const { label, variant } = statusBadge[file.status];
                return (
                  <li key={file.id} className="flex items-center gap-3 rounded-lg border border-gray-100 p-3">
                    <FileText size={20} className="flex-shrink-0 text-gray-400" />
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-sm font-medium text-gray-800">{file.original_name}</p>
                      <p className="text-xs text-gray-400">{formatBytes(file.file_size)}</p>
                    </div>
                    <Badge variant={variant}>{label}</Badge>
                  </li>
                );
              })}
            </ul>
          </CardBody>
        </Card>
      ) : null}

      <div className="flex justify-end">
        <Button
          disabled={!readyFile}
          onClick={() => router.push(`/projects/${projectId}/briefing?file=${readyFile?.id}`)}
        >
          Continuar para Briefing
        </Button>
      </div>
    </div>
  );
}
