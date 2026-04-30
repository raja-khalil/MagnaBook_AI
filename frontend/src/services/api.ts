import axios, { AxiosError } from "axios";
import type { AuthTokens, PhaseAResult, PhaseBResult, PRD, Project, ProjectFile, User } from "@/types";

const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export const http = axios.create({ baseURL: `${BASE}/api/v1` });

// Inject access token from localStorage
http.interceptors.request.use((config) => {
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// On 401 clear auth and redirect to login
http.interceptors.response.use(
  (r) => r,
  (err: AxiosError) => {
    if (err.response?.status === 401 && typeof window !== "undefined") {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);

function extractError(err: unknown): string {
  if (axios.isAxiosError(err)) {
    const detail = (err.response?.data as { detail?: string })?.detail;
    return detail ?? err.message;
  }
  return String(err);
}

// Auth
export const authApi = {
  login: async (email: string, password: string): Promise<AuthTokens> => {
    const form = new URLSearchParams({ username: email, password });
    const { data } = await http.post<AuthTokens>("/auth/token", form, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    return data;
  },

  me: async (): Promise<User> => {
    const { data } = await http.get<User>("/auth/me");
    return data;
  },

  register: async (name: string, email: string, password: string): Promise<User> => {
    const { data } = await http.post<User>("/auth/register", { name, email, password });
    return data;
  },
};

// Projects
export const projectsApi = {
  list: async (): Promise<Project[]> => {
    const { data } = await http.get<Project[]>("/projects");
    return data;
  },

  get: async (id: string): Promise<Project> => {
    const { data } = await http.get<Project>(`/projects/${id}`);
    return data;
  },

  create: async (payload: { name: string; description?: string }): Promise<Project> => {
    const { data } = await http.post<Project>("/projects", payload);
    return data;
  },

  update: async (id: string, payload: Partial<Pick<Project, "name" | "description" | "status">>): Promise<Project> => {
    const { data } = await http.patch<Project>(`/projects/${id}`, payload);
    return data;
  },
};

// Files
export const filesApi = {
  upload: async (projectId: string, file: File, onProgress?: (pct: number) => void): Promise<ProjectFile> => {
    const form = new FormData();
    form.append("file", file);
    const { data } = await http.post<ProjectFile>(`/projects/${projectId}/files`, form, {
      headers: { "Content-Type": "multipart/form-data" },
      onUploadProgress: (e) => {
        if (onProgress && e.total) onProgress(Math.round((e.loaded / e.total) * 100));
      },
    });
    return data;
  },

  list: async (projectId: string): Promise<ProjectFile[]> => {
    const { data } = await http.get<ProjectFile[]>(`/projects/${projectId}/files`);
    return data;
  },
};

// Pipeline
export const pipelineApi = {
  phaseA: async (projectId: string, fileId: string, modelAlias?: string): Promise<PhaseAResult> => {
    const { data } = await http.post<PhaseAResult>(`/projects/${projectId}/pipeline/phase-a`, {
      file_id: fileId,
      model_alias: modelAlias ?? "claude-sonnet",
    });
    return data;
  },

  phaseB: async (projectId: string, fileId: string, approvedPrd: PRD, modelAlias?: string): Promise<PhaseBResult> => {
    const { data } = await http.post<PhaseBResult>(`/projects/${projectId}/pipeline/phase-b`, {
      file_id: fileId,
      approved_prd: approvedPrd,
      model_alias: modelAlias ?? "claude-sonnet",
    });
    return data;
  },
};

// Exports
export const exportsApi = {
  create: async (projectId: string, bookVersionId: string, format: string) => {
    const { data } = await http.post(`/projects/${projectId}/exports`, {
      book_version_id: bookVersionId,
      format,
    });
    return data;
  },

  download: (exportId: string) => `${BASE}/api/v1/exports/${exportId}/download`,
};

export { extractError };
