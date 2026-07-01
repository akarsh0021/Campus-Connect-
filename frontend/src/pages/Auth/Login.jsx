/**
 * Login page with a premium glassmorphism form.
 */
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { LogIn, Mail, Lock, GraduationCap } from 'lucide-react';
import './Auth.css';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const user = await login(form.email, form.password);
      if (user.role === 'student') navigate('/student');
      else if (user.role === 'company') navigate('/company');
      else if (user.role === 'admin') navigate('/admin');
      else navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid credentials');
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
        <h1>Welcome Back</h1>
        <p className="auth-subtitle">Sign in to continue to CampusConnect</p>

        {error && <div className="auth-error">{error}</div>}

        <form onSubmit={handleSubmit}>
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
              />
            </div>
          </div>
          <button
            type="submit"
            className="btn btn-primary w-full btn-lg"
            disabled={loading}
            id="login-submit"
          >
            {loading ? 'Signing in…' : (
              <>
                <LogIn size={18} /> Sign In
              </>
            )}
          </button>
        </form>

        <p className="auth-switch">
          Don't have an account? <Link to="/register">Create one</Link>
        </p>

        <div className="demo-credentials">
          <p className="demo-title">Demo Accounts</p>
          <div className="demo-grid">
            <button className="demo-btn" onClick={() => setForm({ email: 'admin@campus.edu', password: 'admin123' })}>Admin</button>
            <button className="demo-btn" onClick={() => setForm({ email: 'ria.sharma@student.edu', password: 'student123' })}>Student</button>
            <button className="demo-btn" onClick={() => setForm({ email: 'hr@techcorp.com', password: 'company123' })}>Company</button>
          </div>
        </div>
      </div>
    </div>
  );
}
