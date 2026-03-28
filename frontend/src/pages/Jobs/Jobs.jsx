/**
 * Jobs Listing page — browse, search, and apply to jobs.
 */
import { useState, useEffect } from 'react';
import { jobAPI, applicationAPI } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import {
  Search, MapPin, Briefcase, DollarSign, Clock, CheckCircle2,
  Building2, Filter, Send, X,
} from 'lucide-react';
import './Jobs.css';

export default function Jobs() {
  const { user } = useAuth();
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [applying, setApplying] = useState(null);
  const [coverLetter, setCoverLetter] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [selectedJob, setSelectedJob] = useState(null);
  const [toast, setToast] = useState({ msg: '', type: '' });

  useEffect(() => {
    loadJobs();
  }, []);

  const loadJobs = (q = '') => {
    setLoading(true);
    jobAPI.list('active', q).then((res) => {
      setJobs(res.data);
      setLoading(false);
    }).catch(() => setLoading(false));
  };

  const handleSearch = (e) => {
    e.preventDefault();
    loadJobs(search);
  };

  const openApply = (job) => {
    setSelectedJob(job);
    setCoverLetter('');
    setShowModal(true);
  };

  const handleApply = async () => {
    if (!selectedJob) return;
    setApplying(selectedJob.id);
    try {
      const res = await applicationAPI.apply({
        job_id: selectedJob.id,
        cover_letter: coverLetter,
      });
      setToast({ msg: `Applied! AI Match: ${res.data.ai_score}%`, type: 'success' });
      setShowModal(false);
      loadJobs(search);
    } catch (err) {
      setToast({ msg: err.response?.data?.detail || 'Failed to apply', type: 'error' });
    } finally {
      setApplying(null);
    }
    setTimeout(() => setToast({ msg: '', type: '' }), 4000);
  };

  return (
    <div className="container page-wrapper">
      {toast.msg && (
        <div className={`toast toast-${toast.type}`}>
          <CheckCircle2 size={18} /> {toast.msg}
        </div>
      )}

      <div className="page-header">
        <h1>Job Openings</h1>
        <p>Discover opportunities matching your skills</p>
      </div>

      {/* Search */}
      <form className="jobs-search mb-24" onSubmit={handleSearch}>
        <div className="search-bar" style={{ maxWidth: '100%', flex: 1 }}>
          <Search />
          <input
            placeholder="Search jobs by title, description, or skills…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <button type="submit" className="btn btn-primary">
          <Filter size={16} /> Search
        </button>
      </form>

      {loading ? (
        <div className="loading-screen" style={{ minHeight: '40vh' }}>
          <div className="spinner" /><p>Loading jobs…</p>
        </div>
      ) : jobs.length === 0 ? (
        <div className="empty-state">
          <Briefcase size={48} />
          <h3>No jobs found</h3>
          <p>Try adjusting your search or check back later.</p>
        </div>
      ) : (
        <div className="jobs-grid">
          {jobs.map((job) => (
            <div key={job.id} className="job-card glass-card animate-in">
              <div className="job-card-top">
                <div className="job-company-icon">
                  <Building2 size={20} />
                </div>
                <div>
                  <h3>{job.title}</h3>
                  <p className="job-company">{job.company_name}</p>
                </div>
              </div>

              <p className="job-desc">
                {job.description?.substring(0, 150)}
                {(job.description?.length || 0) > 150 ? '…' : ''}
              </p>

              <div className="job-tags">
                {job.location && (
                  <span className="job-tag"><MapPin size={12} /> {job.location}</span>
                )}
                {job.job_type && (
                  <span className="job-tag"><Briefcase size={12} /> {job.job_type}</span>
                )}
                {job.salary_max > 0 && (
                  <span className="job-tag"><DollarSign size={12} /> ₹{(job.salary_min / 100000).toFixed(1)}–{(job.salary_max / 100000).toFixed(1)} LPA</span>
                )}
                {job.deadline && (
                  <span className="job-tag"><Clock size={12} /> {job.deadline.split(' ')[0]}</span>
                )}
              </div>

              {(job.required_skills || []).length > 0 && (
                <div className="job-skills">
                  {job.required_skills.slice(0, 5).map((s) => (
                    <span key={s} className="skill-tag">{s}</span>
                  ))}
                  {job.required_skills.length > 5 && (
                    <span className="skill-tag">+{job.required_skills.length - 5}</span>
                  )}
                </div>
              )}

              <div className="job-card-footer">
                <span className="job-apps">{job.application_count} applicants</span>
                {user?.role === 'student' && (
                  <button
                    className="btn btn-primary btn-sm"
                    onClick={() => openApply(job)}
                  >
                    <Send size={14} /> Apply
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Apply Modal */}
      {showModal && selectedJob && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-box" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Apply to {selectedJob.title}</h2>
              <button className="modal-close" onClick={() => setShowModal(false)}>
                <X size={20} />
              </button>
            </div>
            <p style={{ color: 'var(--text-secondary)', marginBottom: '20px' }}>
              {selectedJob.company_name} • {selectedJob.location}
            </p>
            <div className="form-group">
              <label>Cover Letter (optional)</label>
              <textarea
                className="form-textarea"
                placeholder="Tell the recruiter why you're a great fit…"
                value={coverLetter}
                onChange={(e) => setCoverLetter(e.target.value)}
                rows={5}
              />
            </div>
            <div className="flex gap-12">
              <button className="btn btn-secondary" onClick={() => setShowModal(false)}>
                Cancel
              </button>
              <button
                className="btn btn-primary"
                onClick={handleApply}
                disabled={applying === selectedJob.id}
              >
                {applying === selectedJob.id ? 'Submitting…' : (
                  <><Send size={16} /> Submit Application</>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
