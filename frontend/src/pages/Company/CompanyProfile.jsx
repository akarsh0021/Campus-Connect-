/**
 * Company Profile page — edit company details.
 */
import { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { companyAPI, authAPI } from '../../services/api';
import { Save, Building2, Globe, MapPin, Users, CheckCircle2 } from 'lucide-react';

export default function CompanyProfile() {
  const { refreshUser } = useAuth();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [toast, setToast] = useState('');
  const [form, setForm] = useState({
    company_name: '', industry: '', website: '',
    description: '', location: '', employee_count: '',
  });

  useEffect(() => {
    authAPI.getMe().then((res) => {
      const p = res.data.profile || {};
      setForm({
        company_name: p.company_name || '',
        industry: p.industry || '',
        website: p.website || '',
        description: p.description || '',
        location: p.location || '',
        employee_count: p.employee_count || '',
      });
      setLoading(false);
    });
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await companyAPI.updateProfile(form);
      await refreshUser();
      setToast('Profile updated!');
      setTimeout(() => setToast(''), 3000);
    } catch { setToast('Failed to update'); }
    setSaving(false);
  };

  if (loading) {
    return <div className="loading-screen"><div className="spinner" /><p>Loading…</p></div>;
  }

  return (
    <div className="container page-wrapper">
      {toast && <div className="toast toast-success"><CheckCircle2 size={18} /> {toast}</div>}
      <div className="page-header"><h1>Company Profile</h1><p>Update your company information</p></div>
      <form className="glass-card animate-in" style={{ maxWidth: 700, padding: 40 }} onSubmit={handleSave}>
        <div className="grid-2">
          <div className="form-group">
            <label><Building2 size={14} /> Company Name</label>
            <input className="form-input" value={form.company_name}
              onChange={(e) => setForm({ ...form, company_name: e.target.value })} />
          </div>
          <div className="form-group">
            <label>Industry</label>
            <input className="form-input" placeholder="Technology" value={form.industry}
              onChange={(e) => setForm({ ...form, industry: e.target.value })} />
          </div>
        </div>
        <div className="grid-2">
          <div className="form-group">
            <label><Globe size={14} /> Website</label>
            <input className="form-input" placeholder="https://example.com" value={form.website}
              onChange={(e) => setForm({ ...form, website: e.target.value })} />
          </div>
          <div className="form-group">
            <label><MapPin size={14} /> Location</label>
            <input className="form-input" placeholder="Mumbai, India" value={form.location}
              onChange={(e) => setForm({ ...form, location: e.target.value })} />
          </div>
        </div>
        <div className="form-group">
          <label><Users size={14} /> Employee Count</label>
          <input className="form-input" placeholder="500-1000" value={form.employee_count}
            onChange={(e) => setForm({ ...form, employee_count: e.target.value })} />
        </div>
        <div className="form-group">
          <label>Description</label>
          <textarea className="form-textarea" rows={4} placeholder="Tell students about your company…"
            value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
        </div>
        <button type="submit" className="btn btn-primary btn-lg" disabled={saving}>
          <Save size={18} /> {saving ? 'Saving…' : 'Save Profile'}
        </button>
      </form>
    </div>
  );
}
