import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { Search as SearchIcon, FileCode2, Clock } from 'lucide-react';
import { searchApi } from '@/services/api';
import { format } from 'date-fns';
import type { Script } from '@/types';

export default function Search() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Script[]>([]);

  const searchMutation = useMutation({
    mutationFn: (q: string) => searchApi.search(q),
    onSuccess: (data) => {
      setResults(data.results);
    },
  });

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      searchMutation.mutate(query);
    }
  };

  return (
    <div className="space-y-6 fade-in">
      <div>
        <h1 className="text-3xl font-bold gradient-text mb-2">Search Scripts</h1>
        <p className="text-dark-400">
          Search by name, description, content, or tags
        </p>
      </div>

      {/* Search Form */}
      <div className="card p-6">
        <form onSubmit={handleSearch} className="flex gap-4">
          <div className="flex-1 relative">
            <SearchIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-dark-500" />
            <input
              type="text"
              className="input-field pl-12"
              placeholder="Search scripts..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>
          <button
            type="submit"
            className="btn-primary"
            disabled={searchMutation.isLoading}
          >
            Search
          </button>
        </form>
      </div>

      {/* Results */}
      {searchMutation.isLoading ? (
        <div className="space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="card p-6 animate-pulse">
              <div className="h-4 bg-dark-700 rounded w-1/3 mb-3"></div>
              <div className="h-3 bg-dark-800 rounded w-2/3"></div>
            </div>
          ))}
        </div>
      ) : results.length > 0 ? (
        <div className="space-y-4">
          <p className="text-sm text-dark-400">
            Found {results.length} result{results.length !== 1 ? 's' : ''}
          </p>
          {results.map((script) => (
            <Link
              key={script.objectId}
              to={`/scripts/${script.objectId}`}
              className="card card-hover p-6 block"
            >
              <div className="flex items-start gap-4">
                <FileCode2 className="w-10 h-10 text-primary-500 flex-shrink-0" />
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-dark-50 mb-2">
                    {script.name}
                  </h3>
                  <p className="text-sm text-dark-400 mb-3 line-clamp-2">
                    {script.description || 'No description'}
                  </p>
                  <div className="flex flex-wrap gap-2 mb-3">
                    <span className="text-xs px-2 py-1 rounded bg-dark-700 text-dark-300 font-mono">
                      {script.language}
                    </span>
                    <span className="text-xs px-2 py-1 rounded bg-dark-700 text-dark-300">
                      {script.category}
                    </span>
                    {script.tags.slice(0, 3).map((tag) => (
                      <span
                        key={tag}
                        className="text-xs px-2 py-1 rounded bg-secondary-500/10 text-secondary-400"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                  <div className="flex items-center text-xs text-dark-500">
                    <Clock className="w-3 h-3 mr-1" />
                    {format(new Date(script.updatedAt), 'MMM d, yyyy')}
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      ) : query && !searchMutation.isLoading ? (
        <div className="card p-12 text-center">
          <SearchIcon className="w-16 h-16 text-dark-600 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-dark-300 mb-2">
            No results found
          </h3>
          <p className="text-dark-500">
            Try different keywords or check your spelling
          </p>
        </div>
      ) : null}
    </div>
  );
}
