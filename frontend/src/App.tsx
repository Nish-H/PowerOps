import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Scripts from './pages/Scripts';
import ScriptEditor from './pages/ScriptEditor';
import ScriptDetail from './pages/ScriptDetail';
import Artifacts from './pages/Artifacts';
import Search from './pages/Search';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="scripts" element={<Scripts />} />
        <Route path="scripts/new" element={<ScriptEditor />} />
        <Route path="scripts/:id" element={<ScriptDetail />} />
        <Route path="scripts/:id/edit" element={<ScriptEditor />} />
        <Route path="artifacts" element={<Artifacts />} />
        <Route path="search" element={<Search />} />
      </Route>
    </Routes>
  );
}

export default App;
