/**
 * Company Dashboard — manage posted jobs, view candidates.
 */
import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { jobAPI } from '../../services/api';
import {
  Plus, Briefcase, Users, Eye, Trash2, Edit, MoreVertical,
  TrendingUp, CheckCircle2,
} from 'lucide-react';
import './CompanyDashboard.css';

export default function CompanyDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState('');

  useEffect(() => {
    jobAPI.listMyJobs().then((res) => {
      setJobs(res.data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  const deleteJob = async (id) => {
    if (!window.confirm('Delete this job posting?')) return;
    try {
      await jobAPI.delete(id);
      setJobs((prev) => prev.filter((j) => j.id !== id));
      setToast('Job deleted');
      setTimeout(() => setToast(''), 3000);
    } catch { /* ignore */ }
  };

  const totalApps = jobs.reduce((sum, j) => sum + (j.application_count || 0), 0);

  if (loading) {
    return <div className="loading-screen"><div className="spinner" /><p>Loading dashboard…</p></div>;
  }

  return (
    <div className="container page-wrapper">
      {toast && <div className="toast toast-success"><CheckCircle2 size={18} /> {toast}</div>}

      <div className="page-header flex justify-between items-center">
        <div>
          <h1>Company Dashboard</h1>
          <p>Manage your job postings and review candidates</p>
        </div>
        <Link to="/company/post-job" className="btn btn-primary">
          <Plus size={18} /> Post New Job
        </Link>
      </div>

      {/* Stats */}
      <div className="grid-3 mb-24">
        <div className="stat-card animate-in">
          <div className="stat-icon" style={{ background: 'rgba(59,130,246,0.12)', color: '#60a5fa' }}>
            <Briefcase size={24} />
          </div>
          <div className="stat-value">{jobs.length}</div>
          <div className="stat-label">Posted Jobs</div>
        </div>
        <div className="stat-card animate-in animate-in-delay-1">
          <div className="stat-icon" style={{ background: 'rgba(139,92,246,0.12)', color: '#a78bfa' }}>
            <Users size={24} />
          </div>
          <div className="stat-value">{totalApps}</div>
          <div className="stat-label">Total Applications</div>
        </div>
        <div className="stat-card animate-in animate-in-delay-2">
          <div className="stat-icon" style={{ background: 'rgba(16,185,129,0.12)', color: '#34d399' }}>
            <TrendingUp size={24} />
          </div>
          <div className="stat-value">
            {jobs.filter((j) => j.status === 'active').length}
          </div>
          <div className="stat-label">Active Listings</div>
        </div>
      </div>

      {/* Job listings */}
      {jobs.length === 0 ? (
        <div className="empty-state">
          <Briefcase size={48} />
          <h3>No jobs posted yet</h3>
          <p>Create your first job posting to start receiving applications.</p>
          <Link to="/company/post-job" className="btn btn-primary mt-16">
            <Plus size={16} /> Post a Job
          </Link>
        </div>
      ) : (
        <div className="company-jobs-list">
          {jobs.map((job) => (
            <div key={job.id} className="company-job-card glass-card animate-in">
              <div className="cj-main">
                <div className="cj-info">
                  <h3>{job.title}</h3>
                  <div className="cj-meta">
                    <span className={`badge status-${job.status}`}>{job.status}</span>
                    {job.location && <span className="badge badge-gray">{job.location}</span>}
                    {job.job_type && <span className="badge badge-blue">{job.job_type}</span>}
                  </div>
                </div>
                <div className="cj-stats">
                  <div className="cj-stat">
                    <Users size={16} />
                    <span>{job.application_count} applicants</span>
                  </div>
                </div>
              </div>
              <div className="cj-actions">
                <button
                  className="btn btn-secondary btn-sm"
                  onClick={() => navigate(`/company/jobs/${job.id}/candidates`)}
                >
                  <Eye size={14} /> View Candidates
                </button>
                <button
                  className="btn btn-ghost btn-sm"
                  onClick={() => deleteJob(job.id)}
                >
                  <Trash2 size={14} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
