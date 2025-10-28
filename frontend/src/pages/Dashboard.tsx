import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import {
  FileCode2,
  FileBox,
  GitBranch,
  TrendingUp,
  Clock,
  Zap,
} from 'lucide-react';
import { scriptsApi, integrationApi } from '@/services/api';
import { format } from 'date-fns';

export default function Dashboard() {
  const { data: stats } = useQuery({
    queryKey: ['stats'],
    queryFn: integrationApi.stats,
  });

  const { data: recentScripts } = useQuery({
    queryKey: ['scripts', 'recent'],
    queryFn: () => scriptsApi.list({ page_size: 5 }),
  });

  const statCards = [
    {
      name: 'Total Scripts',
      value: stats?.total_scripts || 0,
      icon: FileCode2,
      color: 'primary',
      change: '+12%',
    },
    {
      name: 'Artifacts',
      value: stats?.total_artifacts || 0,
      icon: FileBox,
      color: 'secondary',
      change: '+8%',
    },
    {
      name: 'Versions',
      value: stats?.total_versions || 0,
      icon: GitBranch,
      color: 'accent',
      change: '+15%',
    },
  ];

  return (
    <div className="space-y-8 fade-in">
      {/* Hero Section */}
      <div className="card card-hover p-8 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-500/10 via-secondary-500/10 to-accent-500/10"></div>
        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-4">
            <Zap className="w-10 h-10 text-primary-500 animate-pulse-slow" />
            <h1 className="text-4xl font-bold gradient-text">
              Welcome to ScriptMyIdeas
            </h1>
          </div>
          <p className="text-lg text-dark-300 mb-6 max-w-3xl">
            Your AI-powered script management platform. Create, manage, and version control
            your scripts with ease. Artifacts are automatically stored and rendered for quick access.
          </p>
          <div className="flex gap-4">
            <Link to="/scripts/new" className="btn-primary">
              <FileCode2 className="w-4 h-4 inline mr-2" />
              Create New Script
            </Link>
            <Link to="/scripts" className="btn-secondary">
              Browse Scripts
            </Link>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {statCards.map((stat) => (
          <div
            key={stat.name}
            className="card card-hover p-6 relative overflow-hidden"
          >
            <div className={`absolute top-0 right-0 w-32 h-32 bg-${stat.color}-500/5 rounded-full -mr-16 -mt-16`}></div>
            <div className="relative z-10">
              <div className="flex justify-between items-start mb-4">
                <stat.icon className={`w-8 h-8 text-${stat.color}-500`} />
                <span className="text-xs font-medium text-accent-400 flex items-center gap-1">
                  <TrendingUp className="w-3 h-3" />
                  {stat.change}
                </span>
              </div>
              <p className="text-3xl font-bold text-dark-50 mb-1">{stat.value}</p>
              <p className="text-sm text-dark-400">{stat.name}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Scripts */}
      <div className="card p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-dark-50 flex items-center gap-2">
            <Clock className="w-6 h-6 text-primary-500" />
            Recent Scripts
          </h2>
          <Link
            to="/scripts"
            className="text-sm text-primary-400 hover:text-primary-300 transition-colors"
          >
            View all →
          </Link>
        </div>

        {recentScripts?.results && recentScripts.results.length > 0 ? (
          <div className="space-y-3">
            {recentScripts.results.map((script) => (
              <Link
                key={script.objectId}
                to={`/scripts/${script.objectId}`}
                className="block p-4 rounded-lg bg-dark-800/50 border border-dark-700 hover:border-primary-500/50 transition-all duration-300 group"
              >
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h3 className="font-semibold text-dark-50 group-hover:text-primary-400 transition-colors">
                      {script.name}
                    </h3>
                    <p className="text-sm text-dark-400 line-clamp-1">
                      {script.description || 'No description'}
                    </p>
                  </div>
                  <span className="text-xs text-dark-500 font-mono">
                    v{script.version}
                  </span>
                </div>

                <div className="flex items-center gap-4 text-xs text-dark-500">
                  <span className="px-2 py-1 rounded bg-dark-700 text-dark-300 font-mono">
                    {script.language}
                  </span>
                  <span className="px-2 py-1 rounded bg-dark-700 text-dark-300">
                    {script.category}
                  </span>
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {format(new Date(script.updatedAt), 'MMM d, yyyy')}
                  </span>
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <FileCode2 className="w-12 h-12 text-dark-600 mx-auto mb-4" />
            <p className="text-dark-400">No scripts yet. Create your first one!</p>
            <Link to="/scripts/new" className="btn-primary mt-4 inline-flex items-center">
              Create Script
            </Link>
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card card-hover p-6">
          <h3 className="text-lg font-semibold text-dark-50 mb-3">Quick Actions</h3>
          <div className="space-y-2">
            <Link to="/scripts/new" className="block p-3 rounded-lg bg-dark-800/50 hover:bg-dark-800 transition-colors">
              <div className="flex items-center gap-3">
                <FileCode2 className="w-5 h-5 text-primary-500" />
                <span className="text-dark-200">Create New Script</span>
              </div>
            </Link>
            <Link to="/search" className="block p-3 rounded-lg bg-dark-800/50 hover:bg-dark-800 transition-colors">
              <div className="flex items-center gap-3">
                <Search className="w-5 h-5 text-secondary-500" />
                <span className="text-dark-200">Search Scripts</span>
              </div>
            </Link>
            <Link to="/artifacts" className="block p-3 rounded-lg bg-dark-800/50 hover:bg-dark-800 transition-colors">
              <div className="flex items-center gap-3">
                <FileBox className="w-5 h-5 text-accent-500" />
                <span className="text-dark-200">View Artifacts</span>
              </div>
            </Link>
          </div>
        </div>

        <div className="card card-hover p-6">
          <h3 className="text-lg font-semibold text-dark-50 mb-3">Features</h3>
          <ul className="space-y-2 text-sm text-dark-300">
            <li className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-primary-500"></span>
              Auto-save scripts from Claude AI conversations
            </li>
            <li className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-secondary-500"></span>
              Version control with full history
            </li>
            <li className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-accent-500"></span>
              Artifact storage and rendering
            </li>
            <li className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-primary-500"></span>
              Advanced search and filtering
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}
