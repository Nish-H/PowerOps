import axios from 'axios';
import type {
  Script,
  ScriptCreateRequest,
  ScriptUpdateRequest,
  ScriptListResponse,
  Version,
  VersionListResponse,
  VersionDiff,
  Artifact,
  ArtifactListResponse,
  AutoSaveRequest,
  AutoSaveResponse,
  Statistics,
} from '@/types';

// Use environment variable for API URL, fallback to relative path for development
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add authentication token here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Scripts API
export const scriptsApi = {
  list: async (params?: {
    page?: number;
    page_size?: number;
    language?: string;
    category?: string;
    tag?: string;
  }): Promise<ScriptListResponse> => {
    const { data } = await api.get('/scripts', { params });
    return data;
  },

  get: async (id: string): Promise<Script> => {
    const { data } = await api.get(`/scripts/${id}`);
    return data;
  },

  create: async (script: ScriptCreateRequest): Promise<Script> => {
    const { data } = await api.post('/scripts', script);
    return data;
  },

  update: async (id: string, script: ScriptUpdateRequest): Promise<Script> => {
    const { data } = await api.put(`/scripts/${id}`, script);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/scripts/${id}`);
  },
};

// Versions API
export const versionsApi = {
  list: async (scriptId: string): Promise<VersionListResponse> => {
    const { data } = await api.get(`/versions/script/${scriptId}`);
    return data;
  },

  get: async (versionId: string): Promise<Version> => {
    const { data } = await api.get(`/versions/${versionId}`);
    return data;
  },

  compare: async (versionId1: string, versionId2: string): Promise<VersionDiff> => {
    const { data } = await api.get(`/versions/diff/${versionId1}/${versionId2}`);
    return data;
  },
};

// Artifacts API
export const artifactsApi = {
  list: async (params?: {
    script_id?: string;
    page?: number;
    page_size?: number;
  }): Promise<ArtifactListResponse> => {
    const { data } = await api.get('/artifacts', { params });
    return data;
  },

  get: async (id: string): Promise<Artifact> => {
    const { data } = await api.get(`/artifacts/${id}`);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/artifacts/${id}`);
  },

  upload: async (
    file: File,
    scriptId: string,
    scriptVersion: string,
    artifactType: string
  ): Promise<Artifact> => {
    const formData = new FormData();
    formData.append('file', file);

    const { data } = await api.post('/artifacts/upload', formData, {
      params: {
        script_id: scriptId,
        script_version: scriptVersion,
        artifact_type: artifactType,
      },
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return data;
  },
};

// Search API
export const searchApi = {
  search: async (query: string, limit?: number): Promise<ScriptListResponse> => {
    const { data } = await api.get('/search', {
      params: { q: query, limit },
    });
    return data;
  },
};

// Integration API
export const integrationApi = {
  autoSave: async (request: AutoSaveRequest): Promise<AutoSaveResponse> => {
    const { data } = await api.post('/integration/auto-save', request);
    return data;
  },

  stats: async (): Promise<Statistics> => {
    const { data } = await api.get('/integration/stats');
    return data.data;
  },
};

export default api;
