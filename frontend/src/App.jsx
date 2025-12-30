import React, { useState, useEffect } from 'react';
import axios from 'axios';
import GraphVisualizer from './components/GraphVisualizer';
import MetricsPanel from './components/MetricsPanel';
import ComparisonDashboard from './components/ComparisonDashboard';
import './App.css';

const API_BASE = 'http://localhost:5000/api';

function App() {
  const [datasets, setDatasets] = useState([]);
  const [selectedGraph, setSelectedGraph] = useState('');
  const [algorithm, setAlgorithm] = useState('label_propagation');
  const [graphElements, setGraphElements] = useState([]);
  const [communities, setCommunities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);

  // Fetch datasets on load
  useEffect(() => {
    fetchDatasets();
  }, []);

  // Fetch graph structure when selectedGraph changes
  useEffect(() => {
    if (selectedGraph) fetchGraphStructure(selectedGraph);
  }, [selectedGraph]);

  const fetchDatasets = async () => {
    try {
      const res = await axios.get(`${API_BASE}/datasets`);
      setDatasets(res.data.datasets);
      if (res.data.datasets.length > 0 && !selectedGraph) {
        setSelectedGraph(res.data.datasets[0].id);
      }
    } catch (err) {
      console.error("Error fetching datasets", err);
    }
  };

  const fetchGraphStructure = async (id) => {
    try {
      const res = await axios.get(`${API_BASE}/graph/${id}`);
      setGraphElements(res.data.elements);
      setCommunities([]); // Reset communities when changing graph
      setStatus(`Loaded ${id}.`);
    } catch (err) {
      console.error("Error fetching graph", err);
    }
  };

  const handleFileUpload = async () => {
    if (!selectedFile) return;
    const formData = new FormData();
    formData.append('file', selectedFile);
    try {
      const res = await axios.post(`${API_BASE}/upload`, formData);
      setStatus('File uploaded: ' + res.data.id);
      fetchDatasets();
    } catch (err) {
      setStatus('Upload failed');
    }
  };

  const [history, setHistory] = useState([]);

  // Fetch metrics for results
  const fetchMetrics = async (graph_id, comms, algName) => {
    try {
      const res = await axios.post(`${API_BASE}/metrics`, {
        graph_id,
        communities: comms
      });
      const newResult = {
        algorithm: algName,
        modularity: res.data.modularity,
        numCommunities: res.data.num_communities
      };
      setHistory(prev => [newResult, ...prev].slice(0, 5));
    } catch (err) {
      console.error("Metrics failed", err);
    }
  };

  const handleRunAnalysis = async () => {
    setLoading(true);
    setStatus('Running analysis in Datalog...');
    try {
      const res = await axios.post(`${API_BASE}/analyze`, {
        graph_id: selectedGraph,
        algorithm: algorithm
      });

      if (res.data.results) {
        setCommunities(res.data.results);
        const count = new Set(res.data.results.map(c => c.community)).size;
        setStatus(`Analysis complete. Found ${count} communities using ${algorithm}.`);
        fetchMetrics(selectedGraph, res.data.results, algorithm);
      }
    } catch (err) {
      console.error(err);
      setStatus('Error: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="app-header">
        <h1>🕵️ Community Detection <span className="datalog-badge">Datalog Powered</span></h1>
        <p>Analyze social networks with Answer Set Programming</p>
      </header>

      <div className="main-layout">
        <aside className="sidebar">
          <section className="control-section">
            <h3>📁 Data Source</h3>
            <div className="control-group">
              <label>Select Graph:</label>
              <select value={selectedGraph} onChange={e => setSelectedGraph(e.target.value)}>
                {datasets.map(d => (
                  <option key={d.id} value={d.id}>{d.name}</option>
                ))}
              </select>
            </div>
            <div className="upload-box">
              <input type="file" onChange={e => setSelectedFile(e.target.files[0])} />
              <button className="btn-secondary" onClick={handleFileUpload}>Upload</button>
            </div>
          </section>

          <section className="control-section">
            <h3>⚙️ Algorithm</h3>
            <div className="control-group">
              <select value={algorithm} onChange={e => setAlgorithm(e.target.value)}>
                <option value="label_propagation">Label Propagation (LPA)</option>
                <option value="modularity_exact">Modularity Exact (ASP)</option>
                <option value="clique_percolation">Clique Percolation (ASP)</option>
                <option value="louvain_baseline">Louvain Baseline (NX)</option>
              </select>
            </div>
            <button className="btn-primary" onClick={handleRunAnalysis} disabled={loading}>
              {loading ? 'Solving ASP...' : 'Run Analysis'}
            </button>
          </section>

          <MetricsPanel communities={communities} computationTime={null} />
        </aside>

        <main className="viewer-pane">
          <div className="status-banner">{status}</div>
          <GraphVisualizer elements={graphElements} communityMapping={communities} />
          {history.length > 0 && <div style={{ padding: '0 20px 20px' }}><ComparisonDashboard results={history} /></div>}
        </main>
      </div>
    </div>
  );
}

export default App;
