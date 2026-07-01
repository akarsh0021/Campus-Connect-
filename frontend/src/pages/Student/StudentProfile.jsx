/**
 * Student Profile page — edit profile details and upload resume.
 */
import { useState, useEffect, useRef } from 'react';
import { useAuth } from '../../context/AuthContext';
import { studentAPI, authAPI } from '../../services/api';
import {
  Upload, Save, User, BookOpen, Award, Link,
  Phone, FileText, Sparkles, CheckCircle2,
} from 'lucide-react';
import './StudentProfile.css';

const cleanSkill = (skill) => 
  skill ? skill.replace(/\s*\((?:matched_from_dictionary|detected_via_nlp|detected_via_llm)\)$/, '').trim() : '';

export default function StudentProfile() {
  const { refreshUser } = useAuth();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [toast, setToast] = useState('');
  const [form, setForm] = useState({
    department: '', cgpa: '', graduation_year: '', skills: '',
    experience_years: '', bio: '', phone: '', linkedin: '', github: '',
  });
  const fileRef = useRef(null);

  useEffect(() => {
    authAPI.getMe().then((res) => {
      const p = res.data.profile || {};
      setProfile(res.data);
      setForm({
        department: p.department || '',
        cgpa: p.cgpa || '',
        graduation_year: p.graduation_year || '',
        skills: (p.skills || []).map(cleanSkill).join(', '),
        experience_years: p.experience_years || '',
        bio: p.bio || '',
        phone: p.phone || '',
        linkedin: p.linkedin || '',
        github: p.github || '',
      });
      setLoading(false);
    });
  }, []);

  const showToast = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(''), 3000);
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const data = {
        ...form,
        cgpa: parseFloat(form.cgpa) || 0,
        graduation_year: parseInt(form.graduation_year) || 2026,
        experience_years: parseFloat(form.experience_years) || 0,
        skills: form.skills.split(',').map((s) => s.trim()).filter(Boolean),
      };
      await studentAPI.updateProfile(data);
      await refreshUser();
      showToast('Profile updated successfully!');
    } catch {
      showToast('Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const handleResumeUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setUploading(true);
    try {
      const res = await studentAPI.uploadResume(file);
      const parsed = res.data.parsed || {};

      // Fetch fresh profile to sync skills, parsed_skills, resume_path
      const meRes = await authAPI.getMe();
      const newProfile = meRes.data;
      const p = newProfile.profile || {};
      setProfile(newProfile);

      // Build auto-fill patch — only overwrite form fields with non-empty parsed values
      const filledLabels = [];
      setForm(prev => {
        const next = { ...prev };

        // Skills: always sync from freshly parsed result (replaces old noisy skills)
        const parsedSkillsClean = (parsed.skills || []).map(cleanSkill).filter(Boolean);
        if (parsedSkillsClean.length > 0) {
          next.skills = parsedSkillsClean.join(', ');
          filledLabels.push('Skills');
        }

        if (parsed.cgpa > 0) {
          next.cgpa = parsed.cgpa;
          filledLabels.push('CGPA');
        }
        if (parsed.experience_years > 0) {
          next.experience_years = parsed.experience_years;
          filledLabels.push('Experience');
        }
        if (parsed.graduation_year > 0) {
          next.graduation_year = parsed.graduation_year;
          filledLabels.push('Graduation Year');
        }
        if (parsed.department) {
          next.department = parsed.department;
          filledLabels.push('Department');
        }
        if (parsed.linkedin) {
          next.linkedin = parsed.linkedin;
          filledLabels.push('LinkedIn');
        }
        if (parsed.github) {
          next.github = parsed.github;
          filledLabels.push('GitHub');
        }
        if (parsed.phone) {
          next.phone = parsed.phone;
          filledLabels.push('Phone');
        }
        if (parsed.bio) {
          next.bio = parsed.bio;
          filledLabels.push('Bio');
        }

        return next;
      });

      const skillCount = (parsed.skills || []).length;
      if (filledLabels.length > 0) {
        showToast(`Resume parsed! Found ${skillCount} skills. Auto-filled: ${filledLabels.join(', ')}`);
      } else {
        showToast(`Resume parsed! Found ${skillCount} skills.`);
      }
    } catch {
      showToast('Failed to upload resume');
    } finally {
      setUploading(false);
      if (fileRef.current) fileRef.current.value = '';
    }
  };

  if (loading) {
    return <div className="loading-screen"><div className="spinner" /><p>Loading profile…</p></div>;
  }

  return (
    <div className="container page-wrapper">
      {toast && (
        <div className="toast toast-success">
          <CheckCircle2 size={18} /> {toast}
        </div>
      )}

      <div className="page-header">
        <h1>Your Profile</h1>
        <p>Complete your profile to improve AI matching accuracy</p>
      </div>

      <div className="profile-layout">
        {/* Profile card */}
        <div className="profile-sidebar glass-card animate-in">
          <div className="profile-avatar">
            {(profile?.full_name || '?')[0].toUpperCase()}
          </div>
          <h2>{profile?.full_name}</h2>
          <p className="profile-email">{profile?.email}</p>

          {profile?.profile?.parsed_skills?.length > 0 && (
            <div className="parsed-skills-section">
              <h4><Sparkles size={14} /> AI-Detected Skills</h4>
              <div className="parsed-skills">
                {profile.profile.parsed_skills.map((s) => (
                  <span key={s} className="skill-tag">{cleanSkill(s)}</span>
                ))}
              </div>
            </div>
          )}

          <div className="resume-section">
            <h4><FileText size={14} /> Resume</h4>
            {profile?.profile?.resume_path ? (
              <p className="resume-file">{profile.profile.resume_path}</p>
            ) : (
              <p className="resume-empty">No resume uploaded</p>
            )}
            <input
              type="file"
              accept=".pdf,.docx,.doc"
              ref={fileRef}
              onChange={handleResumeUpload}
              style={{ display: 'none' }}
            />
            <button
              className="btn btn-secondary w-full mt-8"
              onClick={() => fileRef.current?.click()}
              disabled={uploading}
            >
              <Upload size={16} /> {uploading ? 'Uploading…' : 'Upload Resume'}
            </button>
          </div>
        </div>

        {/* Edit form */}
        <form className="profile-form glass-card animate-in animate-in-delay-1" onSubmit={handleSave}>
          <h3>Edit Details</h3>
          <div className="grid-2">
            <div className="form-group">
              <label><BookOpen size={14} /> Department</label>
              <input
                className="form-input"
                placeholder="Computer Science"
                value={form.department}
                onChange={(e) => setForm({ ...form, department: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label><Award size={14} /> CGPA</label>
              <input
                className="form-input"
                type="number"
                step="0.01"
                placeholder="8.5"
                value={form.cgpa}
                onChange={(e) => setForm({ ...form, cgpa: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Graduation Year</label>
              <input
                className="form-input"
                type="number"
                placeholder="2026"
                value={form.graduation_year}
                onChange={(e) => setForm({ ...form, graduation_year: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Experience (Years)</label>
              <input
                className="form-input"
                type="number"
                step="0.5"
                placeholder="1.5"
                value={form.experience_years}
                onChange={(e) => setForm({ ...form, experience_years: e.target.value })}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Skills (comma separated)</label>
            <textarea
              className="form-textarea"
              placeholder="Python, React, Machine Learning, SQL…"
              value={form.skills}
              onChange={(e) => setForm({ ...form, skills: e.target.value })}
              rows={3}
            />
          </div>

          <div className="form-group">
            <label><User size={14} /> Bio</label>
            <textarea
              className="form-textarea"
              placeholder="Tell companies about yourself…"
              value={form.bio}
              onChange={(e) => setForm({ ...form, bio: e.target.value })}
              rows={3}
            />
          </div>

          <div className="grid-2">
            <div className="form-group">
              <label><Phone size={14} /> Phone</label>
              <input
                className="form-input"
                placeholder="+91 98765 43210"
                value={form.phone}
                onChange={(e) => setForm({ ...form, phone: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label><Link size={14} /> LinkedIn</label>
              <input
                className="form-input"
                placeholder="linkedin.com/in/username"
                value={form.linkedin}
                onChange={(e) => setForm({ ...form, linkedin: e.target.value })}
              />
            </div>
          </div>

          <div className="form-group">
            <label><Link size={14} /> GitHub</label>
            <input
              className="form-input"
              placeholder="github.com/username"
              value={form.github}
              onChange={(e) => setForm({ ...form, github: e.target.value })}
            />
          </div>

          <button type="submit" className="btn btn-primary btn-lg" disabled={saving}>
            <Save size={18} /> {saving ? 'Saving…' : 'Save Profile'}
          </button>
        </form>
      </div>
    </div>
  );
}
