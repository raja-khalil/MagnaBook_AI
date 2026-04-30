export interface User {
  id: string;
  email: string;
  name: string;
  is_superuser: boolean;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export type ProjectStatus = "draft" | "active" | "archived";

export interface Project {
  id: string;
  name: string;
  description: string | null;
  status: ProjectStatus;
  owner_id: string;
  created_at: string;
  updated_at: string;
}

export type FileStatus = "pending" | "processing" | "ready" | "error";

export interface ProjectFile {
  id: string;
  project_id: string;
  filename: string;
  original_name: string;
  mime_type: string;
  file_size: number;
  status: FileStatus;
  created_at: string;
}

export interface PRDChapter {
  number: number;
  title: string;
  objective: string;
  content_requirements: string[];
  estimated_words: number;
  key_sources: string[];
}

export interface PRD {
  book_title: string;
  subtitle: string;
  objective: string;
  target_audience: string;
  tone: string;
  estimated_total_words: number;
  chapters: PRDChapter[];
  constraints: string[];
}

export interface PhaseAResult {
  parsed: { title: string | null; sections: { title: string | null; content: string }[] };
  structured: {
    theme: string;
    target_audience: string;
    genre: string;
    tone: string;
    key_messages: string[];
    chapters: { title: string; summary: string; key_points: string[]; target_words: number }[];
  };
  prd: PRD;
  phase: string;
}

export interface RefinedChapter {
  title: string;
  content: string;
  changes_summary: string;
}

export interface PhaseBResult {
  refined_book: { title: string; chapters: RefinedChapter[] };
  phase: string;
}

export type ExportFormat = "pdf" | "epub" | "docx" | "txt";

export interface Export {
  id: string;
  book_version_id: string;
  format: ExportFormat;
  status: string;
  storage_path: string | null;
  created_at: string;
}

export interface ApiError {
  detail: string;
}
