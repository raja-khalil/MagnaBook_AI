"use client";
import { useState } from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import { CheckCircle, BookOpen, Users, Pencil } from "lucide-react";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardBody } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import type { PRD } from "@/types";

export default function PRDPage() {
  const { id: projectId } = useParams<{ id: string }>();
  const router = useRouter();
  const sp = useSearchParams();
  const fileId = sp.get("file") ?? "";

  const prd: PRD | null = (() => {
    try {
      const raw = sp.get("prd");
      return raw ? (JSON.parse(decodeURIComponent(raw)) as PRD) : null;
    } catch {
      return null;
    }
  })();

  const [approved, setApproved] = useState(false);

  if (!prd) {
    return (
      <div className="flex flex-col items-center gap-4 py-20 text-center">
        <p className="text-gray-500">PRD não encontrado. Volte ao briefing.</p>
        <Button variant="secondary" onClick={() => router.back()}>Voltar</Button>
      </div>
    );
  }

  const proceed = () => {
    const encoded = encodeURIComponent(JSON.stringify(prd));
    router.push(`/projects/${projectId}/editor?prd=${encoded}&file=${fileId}`);
  };

  return (
    <div className="mx-auto max-w-3xl flex flex-col gap-6">
      <PageHeader
        title="Revisão do PRD"
        description="Revise e aprove o Documento de Requisitos do Produto antes da geração"
      />

      <Card>
        <CardBody>
          <div className="grid grid-cols-2 gap-6">
            <div className="col-span-2">
              <p className="text-xs font-medium text-gray-500">Título</p>
              <p className="text-lg font-bold text-gray-900">{prd.book_title}</p>
              {prd.subtitle && <p className="text-sm text-gray-500">{prd.subtitle}</p>}
            </div>
            <div>
              <p className="text-xs font-medium text-gray-500 mb-1 flex items-center gap-1"><Users size={12} /> Público-alvo</p>
              <p className="text-sm text-gray-800">{prd.target_audience}</p>
            </div>
            <div>
              <p className="text-xs font-medium text-gray-500 mb-1 flex items-center gap-1"><Pencil size={12} /> Tom</p>
              <p className="text-sm text-gray-800">{prd.tone}</p>
            </div>
            <div className="col-span-2">
              <p className="text-xs font-medium text-gray-500 mb-1 flex items-center gap-1"><BookOpen size={12} /> Objetivo</p>
              <p className="text-sm text-gray-800">{prd.objective}</p>
            </div>
            <div>
              <p className="text-xs font-medium text-gray-500">Total estimado</p>
              <p className="text-sm font-medium text-gray-800">{prd.estimated_total_words.toLocaleString("pt-BR")} palavras</p>
            </div>
          </div>
        </CardBody>
      </Card>

      <Card>
        <CardBody>
          <p className="mb-4 font-semibold text-gray-800">Capítulos ({prd.chapters.length})</p>
          <div className="flex flex-col gap-4">
            {prd.chapters.map((ch) => (
              <div key={ch.number} className="rounded-lg border border-gray-100 p-4">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <p className="font-medium text-gray-800">
                      {ch.number}. {ch.title}
                    </p>
                    <p className="mt-1 text-sm text-gray-600">{ch.objective}</p>
                  </div>
                  <Badge variant="info">{ch.estimated_words.toLocaleString("pt-BR")} palavras</Badge>
                </div>
                {ch.content_requirements.length > 0 && (
                  <ul className="mt-2 list-disc list-inside space-y-0.5">
                    {ch.content_requirements.map((r, i) => (
                      <li key={i} className="text-xs text-gray-500">{r}</li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        </CardBody>
      </Card>

      {prd.constraints.length > 0 && (
        <Card>
          <CardBody>
            <p className="mb-2 font-semibold text-gray-800">Restrições</p>
            <ul className="list-disc list-inside space-y-1">
              {prd.constraints.map((c, i) => <li key={i} className="text-sm text-gray-600">{c}</li>)}
            </ul>
          </CardBody>
        </Card>
      )}

      <div className="flex items-center gap-4">
        <label className="flex items-center gap-2 cursor-pointer select-none">
          <input type="checkbox" checked={approved} onChange={(e) => setApproved(e.target.checked)} className="h-4 w-4 rounded accent-brand-500" />
          <span className="text-sm font-medium text-gray-700">Aprovei o PRD e quero gerar o livro</span>
        </label>
        <Button disabled={!approved} onClick={proceed} className="ml-auto">
          <CheckCircle size={16} />
          Gerar Livro
        </Button>
      </div>
    </div>
  );
}
