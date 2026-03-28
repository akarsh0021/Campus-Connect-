/**
 * Student Applications page — view all applications with status tracking.
 */
import { useState, useEffect } from 'react';
import { applicationAPI } from '../../services/api';
import { FileText, Clock, CheckCircle2, XCircle, Star, TrendingUp } from 'lucide-react';
import './Applications.css';

export default function StudentApplications() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    applicationAPI.listMine().then((res) => {
      setApplications(res.data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  const filtered = filter === 'all'
    ? applications
    : applications.filter((a) => a.status === filter);

  const statusIcon = (status) => {
    switch (status) {
      case 'shortlisted': return <Star size={16} />;
      case 'selected': return <CheckCircle2 size={16} />;
      case 'rejected': return <XCircle size={16} />;
      default: return <Clock size={16} />;
    }
  };

  if (loading) {
    return <div className="loading-screen"><div className="spinner" /><p>Loading applications…</p></div>;
  }

  return (
    <div className="container page-wrapper">
      <div className="page-header">
        <h1>My Applications</h1>
        <p>Track all your job applications and AI match scores</p>
      </div>

      {/* Filter tabs */}
      <div className="filter-tabs mb-24">
        {['all', 'pending', 'shortlisted', 'selected', 'rejected'].map((f) => (
          <button
            key={f}
            className={`filter-tab ${filter === f ? 'active' : ''}`}
            onClick={() => setFilter(f)}
          >
            {f === 'all' ? 'All' : f.charAt(0).toUpperCase() + f.slice(1)}
            <span className="filter-count">
              {f === 'all' ? applications.length : applications.filter((a) => a.status === f).length}
            </span>
          </button>
        ))}
      </div>

      {filtered.length === 0 ? (
        <div className="empty-state">
          <FileText size={48} />
          <h3>No applications found</h3>
          <p>{filter !== 'all' ? 'Try a different filter.' : 'Start applying to jobs to see them here.'}</p>
        </div>
      ) : (
        <div className="applications-grid">
          {filtered.map((app) => (
            <div key={app.id} className="application-card glass-card animate-in">
              <div className="app-card-header">
                <div>
                  <h3>{app.job_title}</h3>
                  <p className="app-company">{app.company_name}</p>
                </div>
                <div className={`status-chip status-${app.status}`}>
                  {statusIcon(app.status)}
                  {app.status}
                </div>
              </div>

              <div className="app-card-meta">
                {app.job_type && <span className="badge badge-blue">{app.job_type}</span>}
                {app.location && <span className="badge badge-gray">{app.location}</span>}
              </div>

              {app.ai_score > 0 && (
                <div className="ai-score-bar">
                  <div className="ai-score-header">
                    <TrendingUp size={14} />
                    <span>AI Match Score</span>
                    <span className="ai-score-val">{app.ai_score}%</span>
                  </div>
                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{
                        width: `${app.ai_score}%`,
                        background: app.ai_score >= 70 ? 'var(--gradient-success)' :
                          app.ai_score >= 40 ? 'var(--gradient-primary)' : 'var(--gradient-warm)',
                      }}
                    />
                  </div>
                  {app.ai_breakdown && Object.keys(app.ai_breakdown).length > 0 && (
                    <div className="breakdown-grid">
                      {Object.entries(app.ai_breakdown).map(([key, val]) => (
                        <div key={key} className="breakdown-item">
                          <span className="breakdown-key">{key.replace(/_/g, ' ')}</span>
                          <span className="breakdown-val">{val}%</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              <div className="app-card-footer">
                <span className="app-date">
                  Applied {app.applied_at?.split(' ')[0]}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
