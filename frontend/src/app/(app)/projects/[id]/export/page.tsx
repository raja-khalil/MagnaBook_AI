"use client";
import { useState } from "react";
import { useParams } from "next/navigation";
import { Download, FileText, File } from "lucide-react";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardBody } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { exportsApi } from "@/services/api";
import type { ExportFormat } from "@/types";

const formats: { id: ExportFormat; label: string; description: string; icon: typeof FileText }[] = [
  { id: "docx", label: "Word (.docx)", description: "Compatível com Microsoft Word e LibreOffice", icon: FileText },
  { id: "txt", label: "Texto simples (.txt)", description: "Formato universal, sem formatação", icon: File },
  { id: "epub", label: "EPUB", description: "Ideal para e-readers e Kindle", icon: FileText },
  { id: "pdf", label: "PDF", description: "Pronto para impressão e distribuição", icon: File },
];

export default function ExportPage() {
  const { id: projectId } = useParams<{ id: string }>();
  const [selected, setSelected] = useState<ExportFormat>("docx");
  const [exporting, setExporting] = useState(false);
  const [exportId, setExportId] = useState<string | null>(null);

  const handleExport = async () => {
    setExporting(true);
    try {
      const result = await exportsApi.create(projectId, "latest", selected);
      setExportId(result.id);
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className="mx-auto max-w-2xl flex flex-col gap-6">
      <PageHeader title="Exportar Livro" description="Escolha o formato para download" />

      <Card>
        <CardBody>
          <p className="mb-4 font-semibold text-gray-800">Formato de exportação</p>
          <div className="grid grid-cols-2 gap-3">
            {formats.map(({ id, label, description, icon: Icon }) => (
              <button
                key={id}
                onClick={() => setSelected(id)}
                className={`flex flex-col gap-1 rounded-xl border-2 p-4 text-left transition-colors
                  ${selected === id ? "border-brand-500 bg-brand-50" : "border-gray-200 hover:border-gray-300"}`}
              >
                <div className="flex items-center gap-2">
                  <Icon size={18} className={selected === id ? "text-brand-500" : "text-gray-400"} />
                  <span className="text-sm font-medium text-gray-800">{label}</span>
                </div>
                <p className="text-xs text-gray-500">{description}</p>
              </button>
            ))}
          </div>
        </CardBody>
      </Card>

      {exportId ? (
        <Card>
          <CardBody className="flex flex-col items-center gap-4 py-8">
            <Badge variant="success" className="text-sm px-4 py-1">Exportação pronta!</Badge>
            <p className="text-sm text-gray-600 text-center">
              Seu livro foi exportado com sucesso no formato {selected.toUpperCase()}.
            </p>
            <a href={exportsApi.download(exportId)} download>
              <Button>
                <Download size={16} />
                Baixar arquivo
              </Button>
            </a>
          </CardBody>
        </Card>
      ) : (
        <div className="flex justify-end">
          <Button size="lg" loading={exporting} onClick={handleExport}>
            <Download size={16} />
            Exportar como {selected.toUpperCase()}
          </Button>
        </div>
      )}
    </div>
  );
}
