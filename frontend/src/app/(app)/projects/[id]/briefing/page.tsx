"use client";
import { useState } from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import { useMutation } from "@tanstack/react-query";
import { Sparkles, ChevronDown, ChevronUp } from "lucide-react";
import toast from "react-hot-toast";
import { pipelineApi, extractError } from "@/services/api";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardBody, CardHeader } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";
import type { PhaseAResult } from "@/types";

function SectionCard({ title, children, defaultOpen = false }: { title: string; children: React.ReactNode; defaultOpen?: boolean }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <Card>
      <button
        onClick={() => setOpen((v) => !v)}
        className="flex w-full items-center justify-between px-6 py-4 text-left"
      >
        <span className="font-semibold text-gray-800">{title}</span>
        {open ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
      </button>
      {open && <CardBody className="pt-0">{children}</CardBody>}
    </Card>
  );
}

export default function BriefingPage() {
  const { id: projectId } = useParams<{ id: string }>();
  const router = useRouter();
  const sp = useSearchParams();
  const fileId = sp.get("file") ?? "";
  const [result, setResult] = useState<PhaseAResult | null>(null);

  const mutation = useMutation({
    mutationFn: () => pipelineApi.phaseA(projectId, fileId),
    onSuccess: (data) => {
      setResult(data);
      toast.success("Análise concluída!");
    },
    onError: (err) => toast.error(extractError(err)),
  });

  const proceed = () => {
    if (!result) return;
    const prd = encodeURIComponent(JSON.stringify(result.prd));
    router.push(`/projects/${projectId}/prd?prd=${prd}&file=${fileId}`);
  };

  return (
    <div className="mx-auto max-w-3xl flex flex-col gap-6">
      <PageHeader
        title="Briefing e Análise"
        description="A IA analisa o documento e extrai estrutura editorial"
      />

      {!result && (
        <Card>
          <CardBody className="flex flex-col items-center gap-5 py-12">
            {mutation.isPending ? (
              <>
                <Spinner size="lg" className="text-brand-500" />
                <div className="text-center">
                  <p className="font-medium text-gray-700">Analisando documento...</p>
                  <p className="mt-1 text-sm text-gray-400">Parsing → Estruturação → Geração de PRD</p>
                </div>
              </>
            ) : (
              <>
                <Sparkles size={48} className="text-brand-500" />
                <div className="text-center">
                  <p className="font-semibold text-gray-800">Pronto para analisar</p>
                  <p className="mt-1 text-sm text-gray-500">
                    A IA irá extrair a estrutura do documento e gerar um PRD para aprovação
                  </p>
                </div>
                <Button size="lg" onClick={() => mutation.mutate()} disabled={!fileId}>
                  <Sparkles size={16} />
                  Iniciar Análise
                </Button>
              </>
            )}
          </CardBody>
        </Card>
      )}

      {result && (
        <>
          <SectionCard title={`Documento Parseado — ${result.parsed.title ?? "Sem título"}`} defaultOpen>
            <div className="space-y-2">
              {result.parsed.sections.slice(0, 4).map((s, i) => (
                <div key={i} className="rounded-lg bg-gray-50 p-3">
                  {s.title && <p className="text-xs font-semibold text-gray-600 mb-1">{s.title}</p>}
                  <p className="text-sm text-gray-700 line-clamp-3">{s.content}</p>
                </div>
              ))}
              {result.parsed.sections.length > 4 && (
                <p className="text-xs text-gray-400">... e mais {result.parsed.sections.length - 4} seções</p>
              )}
            </div>
          </SectionCard>

          <SectionCard title="Estrutura Editorial Identificada" defaultOpen>
            <div className="grid grid-cols-2 gap-4">
              {[
                ["Tema", result.structured.theme],
                ["Gênero", result.structured.genre],
                ["Público-alvo", result.structured.target_audience],
                ["Tom", result.structured.tone],
              ].map(([k, v]) => (
                <div key={k}>
                  <p className="text-xs font-medium text-gray-500">{k}</p>
                  <p className="text-sm text-gray-800">{v}</p>
                </div>
              ))}
            </div>
            <div className="mt-4">
              <p className="text-xs font-medium text-gray-500 mb-1">Mensagens-chave</p>
              <ul className="list-disc list-inside space-y-0.5">
                {result.structured.key_messages.map((m, i) => (
                  <li key={i} className="text-sm text-gray-700">{m}</li>
                ))}
              </ul>
            </div>
          </SectionCard>

          <div className="flex justify-end">
            <Button onClick={proceed}>
              Revisar PRD
            </Button>
          </div>
        </>
      )}
    </div>
  );
}
