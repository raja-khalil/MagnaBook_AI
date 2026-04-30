"use client";
import { useState } from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import { useMutation } from "@tanstack/react-query";
import { Wand2, BookOpen, ChevronLeft, ChevronRight } from "lucide-react";
import toast from "react-hot-toast";
import { pipelineApi, extractError } from "@/services/api";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardBody } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";
import type { PRD, PhaseBResult } from "@/types";

export default function EditorPage() {
  const { id: projectId } = useParams<{ id: string }>();
  const router = useRouter();
  const sp = useSearchParams();
  const fileId = sp.get("file") ?? "";

  const prd: PRD | null = (() => {
    try {
      const raw = sp.get("prd");
      return raw ? (JSON.parse(decodeURIComponent(raw)) as PRD) : null;
    } catch { return null; }
  })();

  const [result, setResult] = useState<PhaseBResult | null>(null);
  const [activeChapter, setActiveChapter] = useState(0);

  const mutation = useMutation({
    mutationFn: () => pipelineApi.phaseB(projectId, fileId, prd!),
    onSuccess: (data) => {
      setResult(data);
      toast.success("Livro gerado e refinado!");
    },
    onError: (err) => toast.error(extractError(err)),
  });

  if (!prd) {
    return (
      <div className="flex flex-col items-center gap-4 py-20 text-center">
        <p className="text-gray-500">PRD não encontrado.</p>
        <Button variant="secondary" onClick={() => router.back()}>Voltar</Button>
      </div>
    );
  }

  const chapters = result?.refined_book.chapters ?? [];

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title={result ? result.refined_book.title : prd.book_title}
        description={result ? `${chapters.length} capítulos gerados e refinados` : "Geração do livro completo"}
      />

      {!result && (
        <Card>
          <CardBody className="flex flex-col items-center gap-5 py-12">
            {mutation.isPending ? (
              <>
                <Spinner size="lg" className="text-brand-500" />
                <div className="text-center">
                  <p className="font-medium text-gray-700">Gerando livro...</p>
                  <p className="mt-1 text-sm text-gray-400">
                    Geração → Refinamento ({prd.chapters.length} capítulos)
                  </p>
                  <p className="mt-1 text-xs text-gray-400">Isso pode levar alguns minutos</p>
                </div>
              </>
            ) : (
              <>
                <Wand2 size={48} className="text-brand-500" />
                <div className="text-center">
                  <p className="font-semibold text-gray-800">Pronto para gerar</p>
                  <p className="mt-1 text-sm text-gray-500">
                    Gerará {prd.chapters.length} capítulos (~{prd.estimated_total_words.toLocaleString("pt-BR")} palavras)
                  </p>
                </div>
                <Button size="lg" onClick={() => mutation.mutate()}>
                  <Wand2 size={16} />
                  Gerar Livro Completo
                </Button>
              </>
            )}
          </CardBody>
        </Card>
      )}

      {result && (
        <div className="flex gap-6">
          <aside className="w-56 flex-shrink-0">
            <Card>
              <CardBody className="p-3">
                <p className="mb-2 px-2 text-xs font-semibold uppercase tracking-wide text-gray-400">Capítulos</p>
                <nav className="flex flex-col gap-0.5">
                  {chapters.map((ch, i) => (
                    <button
                      key={i}
                      onClick={() => setActiveChapter(i)}
                      className={`rounded-lg px-3 py-2 text-left text-sm transition-colors ${
                        activeChapter === i ? "bg-brand-50 font-medium text-brand-600" : "text-gray-600 hover:bg-gray-50"
                      }`}
                    >
                      <span className="mr-1 text-xs text-gray-400">{i + 1}.</span>
                      {ch.title}
                    </button>
                  ))}
                </nav>
              </CardBody>
            </Card>
          </aside>

          <div className="flex-1 flex flex-col gap-4">
            <Card>
              <CardBody>
                <h2 className="mb-4 flex items-center gap-2 text-lg font-bold text-gray-900">
                  <BookOpen size={20} className="text-brand-500" />
                  {chapters[activeChapter]?.title}
                </h2>
                <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap leading-relaxed">
                  {chapters[activeChapter]?.content}
                </div>
              </CardBody>
            </Card>

            {chapters[activeChapter]?.changes_summary && (
              <Card>
                <CardBody>
                  <p className="text-xs font-medium text-gray-500 mb-1">Melhorias aplicadas no refinamento</p>
                  <p className="text-sm text-gray-600">{chapters[activeChapter].changes_summary}</p>
                </CardBody>
              </Card>
            )}

            <div className="flex justify-between">
              <Button variant="secondary" disabled={activeChapter === 0} onClick={() => setActiveChapter((v) => v - 1)}>
                <ChevronLeft size={16} /> Anterior
              </Button>
              {activeChapter < chapters.length - 1 ? (
                <Button onClick={() => setActiveChapter((v) => v + 1)}>
                  Próximo <ChevronRight size={16} />
                </Button>
              ) : (
                <Button onClick={() => router.push(`/projects/${projectId}/export`)}>
                  Exportar Livro <ChevronRight size={16} />
                </Button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
