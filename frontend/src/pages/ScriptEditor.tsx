import { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import { Save, X } from 'lucide-react';
import Editor from '@monaco-editor/react';
import { scriptsApi } from '@/services/api';
import type { ScriptCreateRequest, ScriptLanguage, ScriptCategory } from '@/types';

export default function ScriptEditor() {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);

  const [formData, setFormData] = useState<ScriptCreateRequest>({
    name: '',
    description: '',
    language: 'python' as ScriptLanguage,
    content: '',
    category: 'other' as ScriptCategory,
    tags: [],
  });

  const [tagInput, setTagInput] = useState('');

  // Load existing script if editing
  useQuery({
    queryKey: ['script', id],
    queryFn: () => scriptsApi.get(id!),
    enabled: isEdit,
    onSuccess: (data) => {
      setFormData({
        name: data.name,
        description: data.description,
        language: data.language,
        content: data.content,
        category: data.category,
        tags: data.tags,
      });
    },
  });

  const createMutation = useMutation({
    mutationFn: scriptsApi.create,
    onSuccess: () => {
      toast.success('Script created successfully!');
      queryClient.invalidateQueries({ queryKey: ['scripts'] });
      navigate('/scripts');
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create script');
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: any }) =>
      scriptsApi.update(id, data),
    onSuccess: () => {
      toast.success('Script updated successfully!');
      queryClient.invalidateQueries({ queryKey: ['scripts'] });
      navigate(`/scripts/${id}`);
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update script');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.name || !formData.content) {
      toast.error('Name and content are required');
      return;
    }

    if (isEdit) {
      updateMutation.mutate({ id: id!, data: formData });
    } else {
      createMutation.mutate(formData);
    }
  };

  const addTag = () => {
    if (tagInput && !formData.tags?.includes(tagInput)) {
      setFormData({
        ...formData,
        tags: [...(formData.tags || []), tagInput],
      });
      setTagInput('');
    }
  };

  const removeTag = (tag: string) => {
    setFormData({
      ...formData,
      tags: formData.tags?.filter((t) => t !== tag) || [],
    });
  };

  return (
    <div className="space-y-6 fade-in">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold gradient-text">
          {isEdit ? 'Edit Script' : 'Create New Script'}
        </h1>
        <button
          onClick={() => navigate(-1)}
          className="btn-secondary"
        >
          <X className="w-4 h-4 mr-2" />
          Cancel
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Info */}
        <div className="card p-6">
          <h2 className="text-lg font-semibold text-dark-50 mb-4">
            Basic Information
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-dark-300 mb-2">
                Script Name *
              </label>
              <input
                type="text"
                className="input-field"
                value={formData.name}
                onChange={(e) =>
                  setFormData({ ...formData, name: e.target.value })
                }
                placeholder="my_script.py"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-dark-300 mb-2">
                Language *
              </label>
              <select
                className="input-field"
                value={formData.language}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    language: e.target.value as ScriptLanguage,
                  })
                }
                required
              >
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="typescript">TypeScript</option>
                <option value="bash">Bash</option>
                <option value="powershell">PowerShell</option>
                <option value="go">Go</option>
                <option value="rust">Rust</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-dark-300 mb-2">
                Description
              </label>
              <textarea
                className="input-field"
                value={formData.description}
                onChange={(e) =>
                  setFormData({ ...formData, description: e.target.value })
                }
                placeholder="What does this script do?"
                rows={3}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-dark-300 mb-2">
                Category
              </label>
              <select
                className="input-field"
                value={formData.category}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    category: e.target.value as ScriptCategory,
                  })
                }
              >
                <option value="automation">Automation</option>
                <option value="data_processing">Data Processing</option>
                <option value="web_scraping">Web Scraping</option>
                <option value="api_integration">API Integration</option>
                <option value="system_admin">System Admin</option>
                <option value="devops">DevOps</option>
                <option value="ai_ml">AI/ML</option>
                <option value="security">Security</option>
                <option value="testing">Testing</option>
                <option value="utility">Utility</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-dark-300 mb-2">
                Tags
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  className="input-field"
                  value={tagInput}
                  onChange={(e) => setTagInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addTag())}
                  placeholder="Add tag"
                />
                <button
                  type="button"
                  onClick={addTag}
                  className="btn-secondary"
                >
                  Add
                </button>
              </div>
              <div className="flex flex-wrap gap-2 mt-2">
                {formData.tags?.map((tag) => (
                  <span
                    key={tag}
                    className="text-xs px-3 py-1 rounded-full bg-secondary-500/10 text-secondary-400 flex items-center gap-2"
                  >
                    {tag}
                    <button
                      type="button"
                      onClick={() => removeTag(tag)}
                      className="hover:text-secondary-300"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Code Editor */}
        <div className="card p-6">
          <h2 className="text-lg font-semibold text-dark-50 mb-4">
            Script Content *
          </h2>
          <div className="border border-dark-700 rounded-lg overflow-hidden">
            <Editor
              height="500px"
              language={formData.language}
              theme="vs-dark"
              value={formData.content}
              onChange={(value) =>
                setFormData({ ...formData, content: value || '' })
              }
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                lineNumbers: 'on',
                roundedSelection: true,
                scrollBeyondLastLine: false,
                automaticLayout: true,
              }}
            />
          </div>
        </div>

        {/* Actions */}
        <div className="flex justify-end gap-4">
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="btn-secondary"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="btn-primary"
            disabled={createMutation.isLoading || updateMutation.isLoading}
          >
            <Save className="w-4 h-4 mr-2" />
            {isEdit ? 'Update Script' : 'Create Script'}
          </button>
        </div>
      </form>
    </div>
  );
}
