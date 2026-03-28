/**
 * Student Dashboard — stats, AI recommendations, recent applications.
 */
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { jobAPI, applicationAPI } from '../../services/api';
import {
  Briefcase, TrendingUp, CheckCircle2, Clock, Star, ArrowRight, Sparkles,
} from 'lucide-react';
import './Dashboard.css';

export default function StudentDashboard() {
  const { user } = useAuth();
  const [applications, setApplications] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      applicationAPI.listMine().catch(() => ({ data: [] })),
      jobAPI.getRecommendations().catch(() => ({ data: [] })),
    ]).then(([appsRes, recsRes]) => {
      setApplications(appsRes.data);
      setRecommendations(recsRes.data);
      setLoading(false);
    });
  }, []);

  const stats = {
    total: applications.length,
    pending: applications.filter((a) => a.status === 'pending').length,
    shortlisted: applications.filter((a) => a.status === 'shortlisted').length,
    selected: applications.filter((a) => a.status === 'selected').length,
  };

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner" />
        <p>Loading your dashboard…</p>
      </div>
    );
  }

  return (
    <div className="dashboard container page-wrapper">
      <div className="page-header">
        <h1>Welcome back, {user?.full_name?.split(' ')[0] || 'Student'} 👋</h1>
        <p>Here's your placement overview</p>
      </div>

      {/* Stat cards */}
      <div className="grid-4 mb-24">
        <div className="stat-card animate-in">
          <div className="stat-icon" style={{ background: 'rgba(59,130,246,0.12)', color: '#60a5fa' }}>
            <Briefcase size={24} />
          </div>
          <div className="stat-value">{stats.total}</div>
          <div className="stat-label">Total Applications</div>
        </div>
        <div className="stat-card animate-in animate-in-delay-1">
          <div className="stat-icon" style={{ background: 'rgba(245,158,11,0.12)', color: '#fbbf24' }}>
            <Clock size={24} />
          </div>
          <div className="stat-value">{stats.pending}</div>
          <div className="stat-label">Pending Review</div>
        </div>
        <div className="stat-card animate-in animate-in-delay-2">
          <div className="stat-icon" style={{ background: 'rgba(139,92,246,0.12)', color: '#a78bfa' }}>
            <Star size={24} />
          </div>
          <div className="stat-value">{stats.shortlisted}</div>
          <div className="stat-label">Shortlisted</div>
        </div>
        <div className="stat-card animate-in animate-in-delay-3">
          <div className="stat-icon" style={{ background: 'rgba(16,185,129,0.12)', color: '#34d399' }}>
            <CheckCircle2 size={24} />
          </div>
          <div className="stat-value">{stats.selected}</div>
          <div className="stat-label">Selected</div>
        </div>
      </div>

      <div className="dashboard-grid">
        {/* AI Recommendations */}
        <div className="dash-section">
          <div className="section-title">
            <Sparkles size={20} className="icon-purple" />
            <h2>AI Recommended Jobs</h2>
            <Link to="/jobs" className="btn btn-ghost btn-sm">
              View All <ArrowRight size={14} />
            </Link>
          </div>
          {recommendations.length === 0 ? (
            <div className="empty-state">
              <Briefcase size={48} />
              <h3>No recommendations yet</h3>
              <p>Complete your profile and upload your resume to get AI-powered job recommendations.</p>
              <Link to="/student/profile" className="btn btn-primary mt-16">Complete Profile</Link>
            </div>
          ) : (
            <div className="rec-list">
              {recommendations.slice(0, 5).map((job) => (
                <div key={job.id} className="rec-card glass-card">
                  <div className="rec-header">
                    <div>
                      <h3>{job.title}</h3>
                      <p className="rec-company">{job.company_name}</p>
                    </div>
                    <div className="rec-score">
                      <span className="score-value">{job.match_score}%</span>
                      <span className="score-label">Match</span>
                    </div>
                  </div>
                  <div className="rec-meta">
                    {job.location && <span className="badge badge-gray">{job.location}</span>}
                    {job.job_type && <span className="badge badge-blue">{job.job_type}</span>}
                    {job.salary_max > 0 && (
                      <span className="badge badge-emerald">
                        ₹{(job.salary_min / 100000).toFixed(1)}–{(job.salary_max / 100000).toFixed(1)} LPA
                      </span>
                    )}
                  </div>
                  <div className="rec-skills">
                    {(job.required_skills || []).slice(0, 4).map((s) => (
                      <span key={s} className="skill-tag">{s}</span>
                    ))}
                  </div>
                  <Link to="/jobs" className="btn btn-primary btn-sm mt-8">Apply Now</Link>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent applications */}
        <div className="dash-section">
          <div className="section-title">
            <TrendingUp size={20} className="icon-blue" />
            <h2>Recent Applications</h2>
            <Link to="/student/applications" className="btn btn-ghost btn-sm">
              View All <ArrowRight size={14} />
            </Link>
          </div>
          {applications.length === 0 ? (
            <div className="empty-state">
              <CheckCircle2 size={48} />
              <h3>No applications yet</h3>
              <p>Start applying to jobs and track your progress here.</p>
              <Link to="/jobs" className="btn btn-primary mt-16">Browse Jobs</Link>
            </div>
          ) : (
            <div className="app-list">
              {applications.slice(0, 5).map((app) => (
                <div key={app.id} className="app-row glass-card">
                  <div className="app-info">
                    <h4>{app.job_title}</h4>
                    <p>{app.company_name}</p>
                  </div>
                  <div className="app-meta">
                    <span className={`badge status-${app.status}`}>{app.status}</span>
                    {app.ai_score > 0 && (
                      <span className="ai-score-mini">{app.ai_score}% AI</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
