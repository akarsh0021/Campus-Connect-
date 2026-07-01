/**
 * AI Candidate Ranking page — view all applicants for a job, ranked by AI.
 */
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { jobAPI, applicationAPI } from '../../services/api';
import {
  ArrowLeft, Crown, Star, CheckCircle2, XCircle, Clock,
  TrendingUp, User, Award,
} from 'lucide-react';
import './Candidates.css';

export default function Candidates() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(null);
  const [toast, setToast] = useState('');

  useEffect(() => {
    jobAPI.getCandidates(jobId).then((res) => {
      setData(res.data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, [jobId]);

  const updateStatus = async (appId, status) => {
    setUpdating(appId);
    try {
      await applicationAPI.updateStatus(appId, status);
      setData((prev) => ({
        ...prev,
        candidates: prev.candidates.map((c) =>
          c.application_id === appId ? { ...c, status } : c
        ),
      }));
      setToast(`Candidate ${status}`);
      setTimeout(() => setToast(''), 3000);
    } catch { /* ignore */ }
    setUpdating(null);
  };

  const getScoreColor = (score) => {
    if (score >= 75) return '#34d399';
    if (score >= 50) return '#60a5fa';
    if (score >= 25) return '#fbbf24';
    return '#fb7185';
  };

  if (loading) {
    return <div className="loading-screen"><div className="spinner" /><p>Loading candidates…</p></div>;
  }

  return (
    <div className="container page-wrapper">
      {toast && <div className="toast toast-success"><CheckCircle2 size={18} /> {toast}</div>}

      <button className="btn btn-ghost mb-16" onClick={() => navigate('/company')}>
        <ArrowLeft size={16} /> Back to Dashboard
      </button>

      <div className="page-header">
        <h1>
          <TrendingUp size={28} className="icon-blue" />
          AI-Ranked Candidates
        </h1>
        <p>{data?.job?.title} — {data?.total || 0} applicants</p>
      </div>

      {!data?.candidates?.length ? (
        <div className="empty-state">
          <User size={48} />
          <h3>No applications yet</h3>
          <p>Share your job listing to receive applications.</p>
        </div>
      ) : (
        <div className="candidates-list">
          {data.candidates.map((c, idx) => (
            <div key={c.application_id} className="candidate-card glass-card animate-in">
              <div className="cand-rank">
                {idx === 0 ? <Crown size={20} className="gold" /> : `#${idx + 1}`}
              </div>

              <div className="cand-info">
                <div className="cand-header">
                  <div className="cand-avatar">{(c.name || '?')[0].toUpperCase()}</div>
                  <div>
                    <h3>{c.name}</h3>
                    <p>{c.email}</p>
                  </div>
                </div>
                <div className="cand-details">
                  {c.department && <span className="badge badge-purple">{c.department}</span>}
                  {c.cgpa > 0 && <span className="badge badge-amber">CGPA: {c.cgpa}</span>}
                  {c.experience_years > 0 && <span className="badge badge-cyan">{c.experience_years}yr exp</span>}
                  {c.graduation_year && <span className="badge badge-gray">{c.graduation_year}</span>}
                </div>
                {(c.skills || []).length > 0 && (
                  <div className="cand-skills">
                    {c.skills.slice(0, 6).map((s) => (
                      <span key={s} className="skill-tag">{s}</span>
                    ))}
                    {c.skills.length > 6 && <span className="skill-tag">+{c.skills.length - 6}</span>}
                  </div>
                )}
              </div>

              <div className="cand-score-section">
                <div className="cand-score-circle" style={{ borderColor: getScoreColor(c.ai_score) }}>
                  <span className="cand-score-value" style={{ color: getScoreColor(c.ai_score) }}>
                    {c.ai_score}
                  </span>
                  <span className="cand-score-label">AI Score</span>
                </div>
                {c.ai_breakdown && (
                  <div className="cand-breakdown">
                    {Object.entries(c.ai_breakdown).map(([k, v]) => (
                      <div key={k} className="mini-bar">
                        <span>{k.replace(/_/g, ' ')}</span>
                        <div className="mini-bar-track">
                          <div className="mini-bar-fill" style={{ width: `${v}%`, background: getScoreColor(v) }} />
                        </div>
                        <span className="mini-bar-val">{v}%</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="cand-actions">
                <span className={`badge status-${c.status}`} style={{ marginBottom: '8px' }}>
                  {c.status}
                </span>
                {(c.status === 'applied' || c.status === 'pending') && (
                  <>
                    <button
                      className="btn btn-success btn-sm"
                      onClick={() => updateStatus(c.application_id, 'shortlisted')}
                      disabled={updating === c.application_id}
                    >
                      <Star size={14} /> Shortlist
                    </button>
                    <button
                      className="btn btn-danger btn-sm"
                      onClick={() => updateStatus(c.application_id, 'rejected')}
                      disabled={updating === c.application_id}
                    >
                      <XCircle size={14} /> Reject
                    </button>
                  </>
                )}
                {c.status === 'shortlisted' && (
                  <button
                    className="btn btn-primary btn-sm"
                    onClick={() => updateStatus(c.application_id, 'selected')}
                    disabled={updating === c.application_id}
                  >
                    <Award size={14} /> Select
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
