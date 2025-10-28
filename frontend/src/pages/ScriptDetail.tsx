import { useParams, Link, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import {
  FileCode2,
  Edit,
  Trash2,
  Download,
  GitBranch,
  Clock,
  Tag,
  ArrowLeft,
} from 'lucide-react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { scriptsApi, versionsApi, artifactsApi } from '@/services/api';
import { format } from 'date-fns';

export default function ScriptDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: script, isLoading } = useQuery({
    queryKey: ['script', id],
    queryFn: () => scriptsApi.get(id!),
    enabled: Boolean(id),
  });

  const { data: versions } = useQuery({
    queryKey: ['versions', id],
    queryFn: () => versionsApi.list(id!),
    enabled: Boolean(id),
  });

  const { data: artifacts } = useQuery({
    queryKey: ['artifacts', id],
    queryFn: () => artifactsApi.list({ script_id: id }),
    enabled: Boolean(id),
  });

  const deleteMutation = useMutation({
    mutationFn: scriptsApi.delete,
    onSuccess: () => {
      toast.success('Script deleted successfully');
      queryClient.invalidateQueries({ queryKey: ['scripts'] });
      navigate('/scripts');
    },
    onError: () => {
      toast.error('Failed to delete script');
    },
  });

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this script?')) {
      deleteMutation.mutate(id!);
    }
  };

  const handleDownload = () => {
    if (!script) return;
    const blob = new Blob([script.content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = script.name;
    a.click();
    URL.revokeObjectURL(url);
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="card p-8 animate-pulse">
          <div className="h-8 bg-dark-700 rounded w-1/3 mb-4"></div>
          <div className="h-4 bg-dark-800 rounded w-2/3"></div>
        </div>
      </div>
    );
  }

  if (!script) {
    return (
      <div className="card p-12 text-center">
        <FileCode2 className="w-16 h-16 text-dark-600 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-dark-300 mb-2">
          Script not found
        </h3>
        <Link to="/scripts" className="btn-primary inline-flex items-center mt-4">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Scripts
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6 fade-in">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <Link
            to="/scripts"
            className="text-sm text-primary-400 hover:text-primary-300 mb-2 inline-flex items-center"
          >
            <ArrowLeft className="w-4 h-4 mr-1" />
            Back to Scripts
          </Link>
          <h1 className="text-3xl font-bold text-dark-50 mb-2">{script.name}</h1>
          <p className="text-dark-400">{script.description || 'No description'}</p>
        </div>
        <div className="flex gap-2">
          <button onClick={handleDownload} className="btn-secondary">
            <Download className="w-4 h-4 mr-2" />
            Download
          </button>
          <Link to={`/scripts/${id}/edit`} className="btn-secondary">
            <Edit className="w-4 h-4 mr-2" />
            Edit
          </Link>
          <button onClick={handleDelete} className="btn-secondary text-red-400 hover:text-red-300">
            <Trash2 className="w-4 h-4 mr-2" />
            Delete
          </button>
        </div>
      </div>

      {/* Metadata */}
      <div className="card p-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p className="text-xs text-dark-500 mb-1">Language</p>
            <p className="text-sm font-mono text-dark-200">{script.language}</p>
          </div>
          <div>
            <p className="text-xs text-dark-500 mb-1">Category</p>
            <p className="text-sm text-dark-200">{script.category}</p>
          </div>
          <div>
            <p className="text-xs text-dark-500 mb-1">Version</p>
            <p className="text-sm font-mono text-dark-200">v{script.version}</p>
          </div>
          <div>
            <p className="text-xs text-dark-500 mb-1">Created By</p>
            <p className="text-sm text-dark-200">{script.created_by}</p>
          </div>
        </div>

        {script.tags && script.tags.length > 0 && (
          <div className="mt-4">
            <p className="text-xs text-dark-500 mb-2">Tags</p>
            <div className="flex flex-wrap gap-2">
              {script.tags.map((tag) => (
                <span
                  key={tag}
                  className="text-xs px-3 py-1 rounded-full bg-secondary-500/10 text-secondary-400 flex items-center gap-1"
                >
                  <Tag className="w-3 h-3" />
                  {tag}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="mt-4 pt-4 border-t border-dark-700 flex items-center justify-between text-xs text-dark-500">
          <span className="flex items-center gap-1">
            <Clock className="w-3 h-3" />
            Updated {format(new Date(script.updatedAt), 'MMM d, yyyy HH:mm')}
          </span>
          {script.metadata && (
            <span>
              {script.metadata.lines} lines • {script.metadata.size} bytes
            </span>
          )}
        </div>
      </div>

      {/* Code */}
      <div className="card p-6">
        <h2 className="text-lg font-semibold text-dark-50 mb-4 flex items-center gap-2">
          <FileCode2 className="w-5 h-5 text-primary-500" />
          Code
        </h2>
        <div className="rounded-lg overflow-hidden border border-dark-700">
          <SyntaxHighlighter
            language={script.language}
            style={vscDarkPlus}
            customStyle={{
              margin: 0,
              borderRadius: 0,
              fontSize: '14px',
            }}
            showLineNumbers
          >
            {script.content}
          </SyntaxHighlighter>
        </div>
      </div>

      {/* Versions */}
      {versions && versions.results.length > 0 && (
        <div className="card p-6">
          <h2 className="text-lg font-semibold text-dark-50 mb-4 flex items-center gap-2">
            <GitBranch className="w-5 h-5 text-accent-500" />
            Version History ({versions.count})
          </h2>
          <div className="space-y-2">
            {versions.results.map((version) => (
              <div
                key={version.objectId}
                className="p-4 rounded-lg bg-dark-800/50 border border-dark-700"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-semibold text-dark-200 font-mono">
                      v{version.versionNumber}
                    </p>
                    <p className="text-sm text-dark-400">
                      {version.changelog || 'No changelog'}
                    </p>
                  </div>
                  <span className="text-xs text-dark-500">
                    {format(new Date(version.createdAt), 'MMM d, yyyy')}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Artifacts */}
      {artifacts && artifacts.results.length > 0 && (
        <div className="card p-6">
          <h2 className="text-lg font-semibold text-dark-50 mb-4">
            Artifacts ({artifacts.count})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {artifacts.results.map((artifact) => (
              <div
                key={artifact.objectId}
                className="p-4 rounded-lg bg-dark-800/50 border border-dark-700"
              >
                <p className="font-semibold text-dark-200">{artifact.name}</p>
                <p className="text-xs text-dark-500 mt-1">
                  {artifact.type} • {artifact.size} bytes
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
