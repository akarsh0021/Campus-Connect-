/**
 * Navbar — top navigation with role-based links, notifications, and user menu.
 */
import { useState, useEffect, useRef } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { notificationAPI } from '../../services/api';
import {
  GraduationCap,
  Bell,
  LogOut,
  User,
  ChevronDown,
  Menu,
  X,
} from 'lucide-react';
import './Navbar.css';

export default function Navbar() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [notifOpen, setNotifOpen] = useState(false);
  const dropRef = useRef(null);
  const notifRef = useRef(null);

  useEffect(() => {
    if (user) {
      notificationAPI.list().then((r) => setNotifications(r.data)).catch(() => {});
    }
  }, [user, location.pathname]);

  // Close dropdowns on outside click
  useEffect(() => {
    const handler = (e) => {
      if (dropRef.current && !dropRef.current.contains(e.target)) setDropdownOpen(false);
      if (notifRef.current && !notifRef.current.contains(e.target)) setNotifOpen(false);
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const unreadCount = notifications.filter((n) => !n.is_read).length;

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const markRead = async (id) => {
    await notificationAPI.markRead(id);
    setNotifications((prev) =>
      prev.map((n) => (n.id === id ? { ...n, is_read: true } : n))
    );
  };

  const markAllRead = async () => {
    await notificationAPI.markAllRead();
    setNotifications((prev) => prev.map((n) => ({ ...n, is_read: true })));
  };

  const navLinks = !user
    ? []
    : user.role === 'student'
      ? [
          { to: '/student', label: 'Dashboard' },
          { to: '/jobs', label: 'Jobs' },
          { to: '/student/applications', label: 'Applications' },
          { to: '/student/profile', label: 'Profile' },
        ]
      : user.role === 'company'
        ? [
            { to: '/company', label: 'Dashboard' },
            { to: '/company/post-job', label: 'Post Job' },
            { to: '/company/profile', label: 'Profile' },
          ]
        : user.role === 'admin'
          ? [
              { to: '/admin', label: 'Dashboard' },
              { to: '/admin/users', label: 'Users' },
              { to: '/admin/placements', label: 'Placements' },
            ]
          : [];

  return (
    <nav className="navbar">
      <div className="navbar-inner container">
        <Link to="/" className="navbar-brand">
          <GraduationCap size={28} />
          <span>CampusConnect</span>
        </Link>

        {/* Desktop nav */}
        <div className={`navbar-links ${menuOpen ? 'open' : ''}`}>
          {navLinks.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              className={`nav-link ${location.pathname === link.to ? 'active' : ''}`}
              onClick={() => setMenuOpen(false)}
            >
              {link.label}
            </Link>
          ))}
        </div>

        <div className="navbar-actions">
          {user ? (
            <>
              {/* Notifications */}
              <div className="notif-wrapper" ref={notifRef}>
                <button
                  className="icon-btn"
                  onClick={() => setNotifOpen(!notifOpen)}
                  id="notification-bell"
                >
                  <Bell size={20} />
                  {unreadCount > 0 && (
                    <span className="notif-badge">{unreadCount}</span>
                  )}
                </button>
                {notifOpen && (
                  <div className="notif-dropdown">
                    <div className="notif-header">
                      <h4>Notifications</h4>
                      {unreadCount > 0 && (
                        <button className="btn-ghost btn-sm" onClick={markAllRead}>
                          Mark all read
                        </button>
                      )}
                    </div>
                    <div className="notif-list">
                      {notifications.length === 0 ? (
                        <p className="notif-empty">No notifications</p>
                      ) : (
                        notifications.slice(0, 10).map((n) => (
                          <div
                            key={n.id}
                            className={`notif-item ${n.is_read ? '' : 'unread'}`}
                            onClick={() => {
                              markRead(n.id);
                              if (n.link) navigate(n.link);
                              setNotifOpen(false);
                            }}
                          >
                            <p>{n.message}</p>
                            <span className="notif-time">
                              {n.created_at?.split('T')[0]}
                            </span>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                )}
              </div>

              {/* User dropdown */}
              <div className="user-dropdown-wrapper" ref={dropRef}>
                <button
                  className="user-btn"
                  onClick={() => setDropdownOpen(!dropdownOpen)}
                  id="user-menu"
                >
                  <div className="avatar">
                    {(user.full_name || user.email || '?')[0].toUpperCase()}
                  </div>
                  <span className="user-name">{user.full_name || user.email}</span>
                  <ChevronDown size={16} />
                </button>
                {dropdownOpen && (
                  <div className="user-dropdown">
                    <div className="dropdown-info">
                      <p className="dropdown-name">{user.full_name}</p>
                      <p className="dropdown-role">{user.role}</p>
                    </div>
                    <div className="dropdown-divider" />
                    <button className="dropdown-item" onClick={handleLogout}>
                      <LogOut size={16} /> Sign out
                    </button>
                  </div>
                )}
              </div>
            </>
          ) : (
            <div className="auth-links">
              <Link to="/login" className="btn btn-ghost">Sign in</Link>
              <Link to="/register" className="btn btn-primary">Get Started</Link>
            </div>
          )}

          {/* Mobile toggle */}
          <button className="mobile-toggle" onClick={() => setMenuOpen(!menuOpen)}>
            {menuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>
    </nav>
  );
}
