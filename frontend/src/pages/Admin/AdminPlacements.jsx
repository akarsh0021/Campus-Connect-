/**
 * Admin Placements page — view all confirmed placements.
 */
import { useState, useEffect } from 'react';
import { adminAPI } from '../../services/api';
import { Award, TrendingUp } from 'lucide-react';

export default function AdminPlacements() {
  const [placements, setPlacements] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    adminAPI.listPlacements().then((res) => {
      setPlacements(res.data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="loading-screen"><div className="spinner" /><p>Loading placements…</p></div>;
  }

  return (
    <div className="container page-wrapper">
      <div className="page-header">
        <h1><Award size={28} className="icon-emerald" /> Placement Records</h1>
        <p>{placements.length} students placed successfully</p>
      </div>

      {placements.length === 0 ? (
        <div className="empty-state">
          <Award size={48} />
          <h3>No placements yet</h3>
          <p>Placements will appear here when companies select candidates.</p>
        </div>
      ) : (
        <div className="glass-card" style={{ padding: 0, overflow: 'hidden' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Student</th>
                <th>Email</th>
                <th>Department</th>
                <th>Company</th>
                <th>Job Title</th>
                <th>AI Score</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {placements.map((p) => (
                <tr key={p.id}>
                  <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{p.student_name}</td>
                  <td>{p.student_email}</td>
                  <td><span className="badge badge-purple">{p.department}</span></td>
                  <td style={{ fontWeight: 500 }}>{p.company_name}</td>
                  <td>{p.job_title}</td>
                  <td>
                    {p.ai_score > 0 && (
                      <span className="ai-score-mini">
                        <TrendingUp size={12} /> {p.ai_score}%
                      </span>
                    )}
                  </td>
                  <td style={{ fontSize: 12 }}>{p.applied_at?.split(' ')[0]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
