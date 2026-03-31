import React, { useState, useEffect } from 'react';
import { Search, Loader2, BookOpen, CheckCircle, AlertCircle, Download, FileText, Copy, Check, Printer } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import './App.css'; // We are relying strictly on this CSS file now

// ---> PASTE YOUR AWS API GATEWAY URL HERE <---
const API_GATEWAY_URL = "https://ekp8zglhdk.execute-api.us-east-1.amazonaws.com/default"; 

function App() {
  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("idle"); 
  const [report, setReport] = useState("");
  const [executionArn, setExecutionArn] = useState(null);
  const [copied, setCopied] = useState(false);

  const startResearch = async () => {
    if (!topic) return;
    setLoading(true);
    setStatus("running");
    setReport("");

    try {
      const response = await fetch(API_GATEWAY_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: "start", topic: topic })
      });
      const data = await response.json();
      setExecutionArn(data.executionArn);
    } catch (err) {
      console.error(err);
      setStatus("failed");
      setLoading(false);
    }
  };

  useEffect(() => {
    let interval;
    if (status === "running" && executionArn) {
      interval = setInterval(async () => {
        try {
          const response = await fetch(API_GATEWAY_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: "status", executionArn: executionArn })
          });
          const data = await response.json();
          
          if (data.status === "SUCCEEDED") {
            setReport(data.final_report);
            setStatus("succeeded");
            setLoading(false);
            clearInterval(interval);
          } else if (data.status === "FAILED" || data.status === "TIMED_OUT") {
            setStatus("failed");
            setLoading(false);
            clearInterval(interval);
          }
        } catch (err) {
          console.error("Polling error:", err);
        }
      }, 5000);
    }
    return () => clearInterval(interval);
  }, [status, executionArn]);

  const handleExport = (format) => {
    if (!report) return;

    if (format === 'copy') {
      navigator.clipboard.writeText(report);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
      return;
    }

    if (format === 'pdf') {
      window.print();
      return;
    }

    let blob, filename;
    const safeTopicName = topic.replace(/[^a-z0-9]/gi, '_').toLowerCase() || 'research';

    if (format === 'md') {
      blob = new Blob([report], { type: 'text/markdown' });
      filename = `${safeTopicName}_report.md`;
    } else if (format === 'txt') {
      const plainText = report.replace(/#/g, '').replace(/\*\*/g, '');
      blob = new Blob([plainText], { type: 'text/plain' });
      filename = `${safeTopicName}_report.txt`;
    }

    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="app-wrapper">
      <div className="app-container">
        
        <header className="header no-print">
          <div className="icon-wrapper">
            <BookOpen size={40} />
          </div>
          <h1>Autonomous Research Crew</h1>
          <p>Deploy an orchestrated team of specialized AI agents to plan, search, synthesize, and fact-check complex topics in real-time.</p>
        </header>

        <div className="search-card no-print">
          <div className="input-group">
            <Search className="search-icon" size={20} />
            <input 
              type="text"
              placeholder="Enter a complex topic (e.g. The impact of solid state batteries)..."
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              disabled={loading}
              onKeyDown={(e) => e.key === 'Enter' && startResearch()}
            />
          </div>
          <button 
            className="btn-primary"
            onClick={startResearch}
            disabled={loading || !topic}
          >
            {loading ? <Loader2 className="spinner" size={20} /> : "Deploy Agents"}
          </button>
        </div>

        {status === "running" && (
          <div className="status-card running no-print">
            <Loader2 className="spinner large" size={32} />
            <h3>Agents are working...</h3>
            <p>The Step Function pipeline has been triggered. The agents are researching, synthesizing, and fact-checking.</p>
            <span className="estimate-badge">Estimated completion: ~2 minutes</span>
          </div>
        )}

        {status === "failed" && (
          <div className="status-card failed no-print">
            <AlertCircle size={28} />
            <div>
              <h3>Pipeline Execution Failed</h3>
              <p>There was an error communicating with the AWS backend or the Step Function timed out.</p>
            </div>
          </div>
        )}

        {report && status === "succeeded" && (
          <div className="report-wrapper">
            
            <div className="toolbar no-print">
              <div className="toolbar-status">
                <CheckCircle size={18} />
                <span>Report Finalized</span>
              </div>
              <div className="toolbar-actions">
                <button className="btn-secondary" onClick={() => handleExport('copy')}>
                  {copied ? <Check size={16} /> : <Copy size={16} />}
                  {copied ? "Copied!" : "Copy"}
                </button>
                <button className="btn-secondary" onClick={() => handleExport('txt')}>
                  <FileText size={16} /> Text
                </button>
                <button className="btn-secondary" onClick={() => handleExport('md')}>
                  <Download size={16} /> Markdown
                </button>
                <button className="btn-action" onClick={() => handleExport('pdf')}>
                  <Printer size={16} /> Save PDF
                </button>
              </div>
            </div>

            <div className="report-content">
              <ReactMarkdown>{report}</ReactMarkdown>
              <div className="report-footer">
                <p>Generated autonomously via AWS Step Functions</p>
                <p>Fact-checked and verified by Reviewer Agent</p>
              </div>
            </div>
            
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
