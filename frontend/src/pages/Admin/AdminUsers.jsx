/**
 * Admin Users Management page.
 */
import { useState, useEffect } from 'react';
import { adminAPI } from '../../services/api';
import { Search, Shield, ShieldOff, Users, GraduationCap, Building2 } from 'lucide-react';

export default function AdminUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [roleFilter, setRoleFilter] = useState('');
  const [search, setSearch] = useState('');

  const loadUsers = () => {
    setLoading(true);
    adminAPI.listUsers(roleFilter, search).then((res) => {
      setUsers(res.data);
      setLoading(false);
    }).catch(() => setLoading(false));
  };

  useEffect(() => { loadUsers(); }, [roleFilter]);

  const toggleUser = async (id) => {
    await adminAPI.toggleUser(id);
    loadUsers();
  };

  const handleSearch = (e) => {
    e.preventDefault();
    loadUsers();
  };

  return (
    <div className="container page-wrapper">
      <div className="page-header"><h1>User Management</h1><p>View and manage all platform users</p></div>

      <div className="flex gap-12 mb-24" style={{ flexWrap: 'wrap' }}>
        <form className="search-bar" onSubmit={handleSearch} style={{ flex: 1 }}>
          <Search />
          <input placeholder="Search by name or email…" value={search}
            onChange={(e) => setSearch(e.target.value)} />
        </form>
        <div className="filter-tabs">
          {[
            { val: '', label: 'All', icon: <Users size={14} /> },
            { val: 'student', label: 'Students', icon: <GraduationCap size={14} /> },
            { val: 'company', label: 'Companies', icon: <Building2 size={14} /> },
          ].map((f) => (
            <button key={f.val} className={`filter-tab ${roleFilter === f.val ? 'active' : ''}`}
              onClick={() => setRoleFilter(f.val)}>
              {f.icon} {f.label}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="loading-screen" style={{ minHeight: '30vh' }}><div className="spinner" /></div>
      ) : (
        <div className="glass-card" style={{ padding: 0, overflow: 'hidden' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>User</th>
                <th>Role</th>
                <th>Details</th>
                <th>Status</th>
                <th>Joined</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id}>
                  <td>
                    <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{u.full_name}</div>
                    <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{u.email}</div>
                  </td>
                  <td>
                    <span className={`badge badge-${u.role === 'student' ? 'blue' : u.role === 'company' ? 'purple' : 'amber'}`}>
                      {u.role}
                    </span>
                  </td>
                  <td>
                    {u.department && <span className="badge badge-gray">{u.department}</span>}
                    {u.company_name && <span className="badge badge-gray">{u.company_name}</span>}
                    {u.cgpa > 0 && <span style={{ marginLeft: 8, fontSize: 12, color: 'var(--text-muted)' }}>CGPA: {u.cgpa}</span>}
                  </td>
                  <td>
                    <span className={`badge ${u.is_active ? 'badge-emerald' : 'badge-rose'}`}>
                      {u.is_active ? 'Active' : 'Disabled'}
                    </span>
                  </td>
                  <td style={{ fontSize: 12 }}>{u.created_at?.split(' ')[0]}</td>
                  <td>
                    {u.role !== 'admin' && (
                      <button
                        className={`btn btn-sm ${u.is_active ? 'btn-danger' : 'btn-success'}`}
                        onClick={() => toggleUser(u.id)}
                      >
                        {u.is_active ? <><ShieldOff size={12} /> Disable</> : <><Shield size={12} /> Enable</>}
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
