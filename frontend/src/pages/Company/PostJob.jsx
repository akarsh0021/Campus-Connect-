/**
 * Post Job page — create a new job posting.
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { jobAPI } from '../../services/api';
import { Plus, ArrowLeft, CheckCircle2 } from 'lucide-react';
import './PostJob.css';

export default function PostJob() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    title: '', description: '', requirements: '',
    required_skills: '', min_cgpa: '', experience_required: '',
    job_type: 'Full-time', location: '',
    salary_min: '', salary_max: '', deadline: '', status: 'active',
  });
  const [saving, setSaving] = useState(false);
  const [toast, setToast] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.title || !form.description) return;
    setSaving(true);
    try {
      const data = {
        ...form,
        required_skills: form.required_skills.split(',').map(s => s.trim()).filter(Boolean),
        min_cgpa: parseFloat(form.min_cgpa) || 0,
        experience_required: parseFloat(form.experience_required) || 0,
        salary_min: parseInt(form.salary_min) || 0,
        salary_max: parseInt(form.salary_max) || 0,
      };
      await jobAPI.create(data);
      setToast('Job posted successfully!');
      setTimeout(() => navigate('/company'), 1500);
    } catch {
      setToast('Failed to post job');
    } finally {
      setSaving(false);
    }
  };

  const update = (field, val) => setForm({ ...form, [field]: val });

  return (
    <div className="container page-wrapper">
      {toast && <div className="toast toast-success"><CheckCircle2 size={18} /> {toast}</div>}

      <button className="btn btn-ghost mb-16" onClick={() => navigate('/company')}>
        <ArrowLeft size={16} /> Back to Dashboard
      </button>

      <div className="post-job-card glass-card animate-in">
        <h1>Create Job Posting</h1>
        <p className="pj-subtitle">Fill in the details to attract the best candidates</p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Job Title *</label>
            <input className="form-input" placeholder="e.g. Software Engineer Intern"
              value={form.title} onChange={(e) => update('title', e.target.value)} required />
          </div>

          <div className="form-group">
            <label>Description *</label>
            <textarea className="form-textarea" placeholder="Describe the role, responsibilities, and what makes this position exciting…"
              value={form.description} onChange={(e) => update('description', e.target.value)} rows={5} required />
          </div>

          <div className="form-group">
            <label>Requirements</label>
            <textarea className="form-textarea" placeholder="List technical and non-technical requirements…"
              value={form.requirements} onChange={(e) => update('requirements', e.target.value)} rows={3} />
          </div>

          <div className="form-group">
            <label>Required Skills (comma separated)</label>
            <input className="form-input" placeholder="Python, React, SQL, Machine Learning"
              value={form.required_skills} onChange={(e) => update('required_skills', e.target.value)} />
          </div>

          <div className="grid-3">
            <div className="form-group">
              <label>Min CGPA</label>
              <input className="form-input" type="number" step="0.1" placeholder="7.0"
                value={form.min_cgpa} onChange={(e) => update('min_cgpa', e.target.value)} />
            </div>
            <div className="form-group">
              <label>Experience (Years)</label>
              <input className="form-input" type="number" step="0.5" placeholder="0"
                value={form.experience_required} onChange={(e) => update('experience_required', e.target.value)} />
            </div>
            <div className="form-group">
              <label>Job Type</label>
              <select className="form-select" value={form.job_type} onChange={(e) => update('job_type', e.target.value)}>
                <option>Full-time</option>
                <option>Part-time</option>
                <option>Internship</option>
                <option>Contract</option>
              </select>
            </div>
          </div>

          <div className="grid-3">
            <div className="form-group">
              <label>Location</label>
              <input className="form-input" placeholder="Mumbai, India"
                value={form.location} onChange={(e) => update('location', e.target.value)} />
            </div>
            <div className="form-group">
              <label>Salary Min (₹)</label>
              <input className="form-input" type="number" placeholder="400000"
                value={form.salary_min} onChange={(e) => update('salary_min', e.target.value)} />
            </div>
            <div className="form-group">
              <label>Salary Max (₹)</label>
              <input className="form-input" type="number" placeholder="800000"
                value={form.salary_max} onChange={(e) => update('salary_max', e.target.value)} />
            </div>
          </div>

          <div className="grid-2">
            <div className="form-group">
              <label>Application Deadline</label>
              <input className="form-input" type="date"
                value={form.deadline} onChange={(e) => update('deadline', e.target.value)} />
            </div>
            <div className="form-group">
              <label>Status</label>
              <select className="form-select" value={form.status} onChange={(e) => update('status', e.target.value)}>
                <option value="active">Active</option>
                <option value="draft">Draft</option>
                <option value="closed">Closed</option>
              </select>
            </div>
          </div>

          <button type="submit" className="btn btn-primary btn-lg mt-16" disabled={saving}>
            <Plus size={18} /> {saving ? 'Publishing…' : 'Publish Job'}
          </button>
        </form>
      </div>
    </div>
  );
}
