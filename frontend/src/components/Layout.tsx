import { Outlet, Link, useLocation } from 'react-router-dom';
import {
  FileCode2,
  Home,
  Search,
  FileBox,
  Sparkles,
  Github,
} from 'lucide-react';

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Scripts', href: '/scripts', icon: FileCode2 },
  { name: 'Artifacts', href: '/artifacts', icon: FileBox },
  { name: 'Search', href: '/search', icon: Search },
];

export default function Layout() {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-dark-950">
      {/* Header */}
      <header className="border-b border-dark-800 bg-dark-900/50 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <div className="relative">
                <Sparkles className="w-8 h-8 text-primary-500 animate-pulse-slow" />
                <div className="absolute inset-0 blur-xl bg-primary-500/30"></div>
              </div>
              <h1 className="text-2xl font-bold gradient-text">ScriptMyIdeas</h1>
              <span className="text-xs text-dark-400 font-mono">v1.0.0</span>
            </div>

            <nav className="flex items-center gap-1">
              {navigation.map((item) => {
                const isActive = location.pathname === item.href ||
                  (item.href !== '/' && location.pathname.startsWith(item.href));
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all duration-300 ${
                      isActive
                        ? 'bg-primary-500/10 text-primary-400 border border-primary-500/30'
                        : 'text-dark-400 hover:text-dark-100 hover:bg-dark-800'
                    }`}
                  >
                    <item.icon className="w-4 h-4" />
                    <span className="font-medium">{item.name}</span>
                  </Link>
                );
              })}
            </nav>

            <a
              href="https://github.com/Nish-H/ScriptMyIdeas"
              target="_blank"
              rel="noopener noreferrer"
              className="text-dark-400 hover:text-primary-400 transition-colors"
            >
              <Github className="w-5 h-5" />
            </a>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t border-dark-800 bg-dark-900/50 backdrop-blur-xl mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <p className="text-sm text-dark-400">
              Built with Claude AI • Modern Script Management Platform
            </p>
            <p className="text-sm text-dark-500">
              © 2025 ScriptMyIdeas. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
