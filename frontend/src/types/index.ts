export type ScriptLanguage =
  | 'python'
  | 'bash'
  | 'javascript'
  | 'typescript'
  | 'powershell'
  | 'ruby'
  | 'go'
  | 'rust'
  | 'java'
  | 'cpp'
  | 'c'
  | 'other';

export type ScriptCategory =
  | 'automation'
  | 'data_processing'
  | 'web_scraping'
  | 'api_integration'
  | 'system_admin'
  | 'devops'
  | 'ai_ml'
  | 'security'
  | 'testing'
  | 'utility'
  | 'other';

export type ArtifactType =
  | 'html'
  | 'json'
  | 'csv'
  | 'xml'
  | 'log'
  | 'image'
  | 'pdf'
  | 'text'
  | 'markdown'
  | 'other';

export interface ScriptMetadata {
  size: number;
  lines: number;
  complexity?: number;
  dependencies?: string[];
  execution_time?: number;
}

export interface Script {
  objectId: string;
  name: string;
  description?: string;
  language: ScriptLanguage;
  content: string;
  version: string;
  category: ScriptCategory;
  tags: string[];
  created_by: string;
  createdAt: string;
  updatedAt: string;
  isLatest: boolean;
  parentScriptId?: string;
  metadata?: ScriptMetadata;
}

export interface ScriptCreateRequest {
  name: string;
  description?: string;
  language: ScriptLanguage;
  content: string;
  category?: ScriptCategory;
  tags?: string[];
  version?: string;
  created_by?: string;
}

export interface ScriptUpdateRequest {
  name?: string;
  description?: string;
  content?: string;
  language?: ScriptLanguage;
  category?: ScriptCategory;
  tags?: string[];
}

export interface ScriptListResponse {
  results: Script[];
  count: number;
  total: number;
  page: number;
  page_size: number;
}

export interface Version {
  objectId: string;
  scriptId: string;
  versionNumber: string;
  content: string;
  changelog?: string;
  createdBy: string;
  createdAt: string;
  hash: string;
}

export interface VersionListResponse {
  results: Version[];
  count: number;
  script_id: string;
}

export interface VersionDiff {
  old_version: string;
  new_version: string;
  diff: string;
  additions: number;
  deletions: number;
  changes: number;
}

export interface Artifact {
  objectId: string;
  scriptId: string;
  scriptVersion: string;
  name: string;
  type: ArtifactType;
  content?: string;
  file_url?: string;
  size: number;
  metadata?: Record<string, any>;
  createdAt: string;
}

export interface ArtifactListResponse {
  results: Artifact[];
  count: number;
  total: number;
  page: number;
  page_size: number;
}

export interface AutoSaveRequest {
  name: string;
  content: string;
  description?: string;
  language?: string;
  category?: string;
  tags?: string[];
  artifacts?: Array<{
    name: string;
    type: string;
    content?: string;
    file_url?: string;
    metadata?: Record<string, any>;
  }>;
}

export interface AutoSaveResponse {
  script: Script;
  artifacts: Artifact[];
  message: string;
}

export interface Statistics {
  total_scripts: number;
  total_artifacts: number;
  total_versions: number;
}
