import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { FileCode2, Plus, Clock, Tag } from 'lucide-react';
import { scriptsApi } from '@/services/api';
import { format } from 'date-fns';
import type { ScriptLanguage, ScriptCategory } from '@/types';

export default function Scripts() {
  const [filters, setFilters] = useState<{
    language?: string;
    category?: string;
    tag?: string;
  }>({});

  const { data, isLoading } = useQuery({
    queryKey: ['scripts', filters],
    queryFn: () => scriptsApi.list(filters),
  });

  return (
    <div className="space-y-6 fade-in">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold gradient-text mb-2">Scripts</h1>
          <p className="text-dark-400">
            Manage and organize your scripts
          </p>
        </div>
        <Link to="/scripts/new" className="btn-primary">
          <Plus className="w-4 h-4 mr-2" />
          New Script
        </Link>
      </div>

      {/* Filters */}
      <div className="card p-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <select
            className="input-field"
            value={filters.language || ''}
            onChange={(e) =>
              setFilters({ ...filters, language: e.target.value || undefined })
            }
          >
            <option value="">All Languages</option>
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
            <option value="bash">Bash</option>
            <option value="powershell">PowerShell</option>
            <option value="go">Go</option>
            <option value="rust">Rust</option>
          </select>

          <select
            className="input-field"
            value={filters.category || ''}
            onChange={(e) =>
              setFilters({ ...filters, category: e.target.value || undefined })
            }
          >
            <option value="">All Categories</option>
            <option value="automation">Automation</option>
            <option value="data_processing">Data Processing</option>
            <option value="web_scraping">Web Scraping</option>
            <option value="api_integration">API Integration</option>
            <option value="devops">DevOps</option>
            <option value="ai_ml">AI/ML</option>
          </select>

          <button
            onClick={() => setFilters({})}
            className="btn-secondary"
          >
            Clear Filters
          </button>
        </div>
      </div>

      {/* Scripts Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="card p-6 animate-pulse">
              <div className="h-4 bg-dark-700 rounded w-3/4 mb-3"></div>
              <div className="h-3 bg-dark-800 rounded w-full mb-2"></div>
              <div className="h-3 bg-dark-800 rounded w-2/3"></div>
            </div>
          ))}
        </div>
      ) : data?.results && data.results.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {data.results.map((script) => (
            <Link
              key={script.objectId}
              to={`/scripts/${script.objectId}`}
              className="card card-hover p-6 group"
            >
              <div className="flex justify-between items-start mb-4">
                <FileCode2 className="w-8 h-8 text-primary-500 group-hover:scale-110 transition-transform" />
                <span className="text-xs text-dark-500 font-mono">
                  v{script.version}
                </span>
              </div>

              <h3 className="text-lg font-semibold text-dark-50 mb-2 group-hover:text-primary-400 transition-colors">
                {script.name}
              </h3>

              <p className="text-sm text-dark-400 mb-4 line-clamp-2">
                {script.description || 'No description provided'}
              </p>

              <div className="flex flex-wrap gap-2 mb-4">
                <span className="text-xs px-2 py-1 rounded bg-dark-700 text-dark-300 font-mono">
                  {script.language}
                </span>
                <span className="text-xs px-2 py-1 rounded bg-dark-700 text-dark-300">
                  {script.category}
                </span>
              </div>

              {script.tags && script.tags.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-4">
                  {script.tags.slice(0, 3).map((tag) => (
                    <span
                      key={tag}
                      className="text-xs px-2 py-1 rounded bg-secondary-500/10 text-secondary-400 flex items-center gap-1"
                    >
                      <Tag className="w-3 h-3" />
                      {tag}
                    </span>
                  ))}
                  {script.tags.length > 3 && (
                    <span className="text-xs text-dark-500">
                      +{script.tags.length - 3} more
                    </span>
                  )}
                </div>
              )}

              <div className="flex items-center justify-between text-xs text-dark-500">
                <span className="flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  {format(new Date(script.updatedAt), 'MMM d, yyyy')}
                </span>
                <span className="text-dark-600">{script.created_by}</span>
              </div>
            </Link>
          ))}
        </div>
      ) : (
        <div className="card p-12 text-center">
          <FileCode2 className="w-16 h-16 text-dark-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-dark-300 mb-2">
            No scripts found
          </h3>
          <p className="text-dark-500 mb-6">
            {Object.keys(filters).length > 0
              ? 'Try adjusting your filters'
              : 'Create your first script to get started'}
          </p>
          {Object.keys(filters).length === 0 && (
            <Link to="/scripts/new" className="btn-primary inline-flex items-center">
              <Plus className="w-4 h-4 mr-2" />
              Create Script
            </Link>
          )}
        </div>
      )}
    </div>
  );
}
