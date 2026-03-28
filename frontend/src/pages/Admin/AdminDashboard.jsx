/**
 * Admin Dashboard — analytics with charts, overview stats.
 */
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { adminAPI } from '../../services/api';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend,
} from 'recharts';
import {
  Users, Briefcase, Building2, TrendingUp, Award, CheckCircle2,
  XCircle, Clock, ArrowRight, BarChart3,
} from 'lucide-react';
import './AdminDashboard.css';

const COLORS = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#f43f5e', '#06b6d4'];

export default function AdminDashboard() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    adminAPI.getAnalytics().then((res) => {
      setAnalytics(res.data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="loading-screen"><div className="spinner" /><p>Loading analytics…</p></div>;
  }

  const o = analytics?.overview || {};
  const deptData = Object.entries(analytics?.departments || {}).map(([name, value]) => ({ name, value }));
  const statusData = Object.entries(analytics?.status_distribution || {}).map(([name, value]) => ({ name, value }));
  const skillData = (analytics?.top_skills || []).slice(0, 10);

  return (
    <div className="container page-wrapper">
      <div className="page-header">
        <h1>Admin Dashboard</h1>
        <p>Platform-wide analytics and management</p>
      </div>

      {/* Overview stat cards */}
      <div className="grid-4 mb-24">
        {[
          { icon: <Users size={24} />, value: o.total_students, label: 'Students', color: 'blue' },
          { icon: <Building2 size={24} />, value: o.total_companies, label: 'Companies', color: 'purple' },
          { icon: <Briefcase size={24} />, value: o.total_jobs, label: 'Jobs', color: 'amber' },
          { icon: <CheckCircle2 size={24} />, value: o.total_applications, label: 'Applications', color: 'emerald' },
        ].map((s, i) => (
          <div key={i} className={`stat-card animate-in animate-in-delay-${i + 1}`}>
            <div className="stat-icon" style={{
              background: `rgba(${s.color === 'blue' ? '59,130,246' : s.color === 'purple' ? '139,92,246' : s.color === 'amber' ? '245,158,11' : '16,185,129'},0.12)`,
              color: s.color === 'blue' ? '#60a5fa' : s.color === 'purple' ? '#a78bfa' : s.color === 'amber' ? '#fbbf24' : '#34d399',
            }}>{s.icon}</div>
            <div className="stat-value">{s.value}</div>
            <div className="stat-label">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Secondary stats */}
      <div className="grid-3 mb-24">
        <div className="stat-card animate-in">
          <div className="stat-icon" style={{ background: 'rgba(16,185,129,0.12)', color: '#34d399' }}>
            <Award size={24} />
          </div>
          <div className="stat-value">{o.placement_rate}%</div>
          <div className="stat-label">Placement Rate</div>
        </div>
        <div className="stat-card animate-in animate-in-delay-1">
          <div className="stat-icon" style={{ background: 'rgba(59,130,246,0.12)', color: '#60a5fa' }}>
            <TrendingUp size={24} />
          </div>
          <div className="stat-value">{o.avg_ai_score}%</div>
          <div className="stat-label">Avg AI Score</div>
        </div>
        <div className="stat-card animate-in animate-in-delay-2">
          <div className="stat-icon" style={{ background: 'rgba(244,63,94,0.12)', color: '#fb7185' }}>
            <XCircle size={24} />
          </div>
          <div className="stat-value">{o.total_selected}</div>
          <div className="stat-label">Total Selected</div>
        </div>
      </div>

      {/* Charts row */}
      <div className="dashboard-grid mb-24">
        {/* Department distribution */}
        <div className="dash-section">
          <div className="section-title">
            <BarChart3 size={20} className="icon-blue" />
            <h2>Students by Department</h2>
          </div>
          {deptData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={deptData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} />
                <Tooltip
                  contentStyle={{
                    background: '#1e293b',
                    border: '1px solid rgba(255,255,255,0.1)',
                    borderRadius: '8px',
                    color: '#f1f5f9',
                  }}
                />
                <Bar dataKey="value" fill="#3b82f6" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="empty-state" style={{ padding: '40px' }}>No department data</p>
          )}
        </div>

        {/* Application status pie */}
        <div className="dash-section">
          <div className="section-title">
            <Clock size={20} className="icon-amber" />
            <h2>Application Status</h2>
          </div>
          {statusData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={statusData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={4}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}`}
                >
                  {statusData.map((_, index) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    background: '#1e293b',
                    border: '1px solid rgba(255,255,255,0.1)',
                    borderRadius: '8px',
                    color: '#f1f5f9',
                  }}
                />
                <Legend formatter={(value) => <span style={{ color: '#94a3b8' }}>{value}</span>} />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="empty-state" style={{ padding: '40px' }}>No status data</p>
          )}
        </div>
      </div>

      {/* Top Skills */}
      <div className="dash-section mb-24 animate-in">
        <div className="section-title">
          <Award size={20} className="icon-purple" />
          <h2>Top Skills Across Students</h2>
        </div>
        {skillData.length > 0 ? (
          <div className="skills-bar-list">
            {skillData.map((s, i) => (
              <div key={s.skill} className="skill-bar-row">
                <span className="skill-bar-name">{s.skill}</span>
                <div className="skill-bar-track">
                  <div
                    className="skill-bar-fill"
                    style={{
                      width: `${(s.count / skillData[0].count) * 100}%`,
                      background: COLORS[i % COLORS.length],
                    }}
                  />
                </div>
                <span className="skill-bar-count">{s.count}</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="empty-state">No skill data</p>
        )}
      </div>

      {/* Quick links */}
      <div className="grid-2">
        <Link to="/admin/users" className="admin-link-card glass-card">
          <Users size={24} />
          <div>
            <h3>User Management</h3>
            <p>View, search, and toggle user accounts</p>
          </div>
          <ArrowRight size={20} />
        </Link>
        <Link to="/admin/placements" className="admin-link-card glass-card">
          <Award size={24} />
          <div>
            <h3>Placement Records</h3>
            <p>View all confirmed placements</p>
          </div>
          <ArrowRight size={20} />
        </Link>
      </div>
    </div>
  );
}
