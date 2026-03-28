/**
 * Register page — student or company registration.
 */
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { UserPlus, Mail, Lock, User, GraduationCap, Building2 } from 'lucide-react';
import './Auth.css';

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    full_name: '',
    email: '',
    password: '',
    role: 'student',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const user = await register(form);
      if (user.role === 'student') navigate('/student/profile');
      else if (user.role === 'company') navigate('/company/profile');
      else navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-bg">
        <div className="auth-orb orb-a"></div>
        <div className="auth-orb orb-b"></div>
      </div>
      <div className="auth-card animate-in">
        <div className="auth-logo">
          <GraduationCap size={36} />
        </div>
        <h1>Create Account</h1>
        <p className="auth-subtitle">Join CampusConnect and start your journey</p>

        {error && <div className="auth-error">{error}</div>}

        {/* Role selector */}
        <div className="role-selector">
          <button
            type="button"
            className={`role-btn ${form.role === 'student' ? 'active' : ''}`}
            onClick={() => setForm({ ...form, role: 'student' })}
          >
            <GraduationCap size={20} /> Student
          </button>
          <button
            type="button"
            className={`role-btn ${form.role === 'company' ? 'active' : ''}`}
            onClick={() => setForm({ ...form, role: 'company' })}
          >
            <Building2 size={20} /> Company
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="full_name">
              {form.role === 'company' ? 'Company Name' : 'Full Name'}
            </label>
            <div className="input-icon-wrap">
              <User size={18} />
              <input
                id="full_name"
                type="text"
                className="form-input"
                placeholder={form.role === 'company' ? 'Acme Inc.' : 'John Doe'}
                value={form.full_name}
                onChange={(e) => setForm({ ...form, full_name: e.target.value })}
                required
              />
            </div>
          </div>
          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <div className="input-icon-wrap">
              <Mail size={18} />
              <input
                id="email"
                type="email"
                className="form-input"
                placeholder="you@example.com"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                required
              />
            </div>
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <div className="input-icon-wrap">
              <Lock size={18} />
              <input
                id="password"
                type="password"
                className="form-input"
                placeholder="••••••••"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                required
                minLength={6}
              />
            </div>
          </div>
          <button
            type="submit"
            className="btn btn-primary w-full btn-lg"
            disabled={loading}
            id="register-submit"
          >
            {loading ? 'Creating account…' : (
              <>
                <UserPlus size={18} /> Create Account
              </>
            )}
          </button>
        </form>

        <p className="auth-switch">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
