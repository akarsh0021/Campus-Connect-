import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function ProtectedRoute({ children, role }) {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="loading-screen"><div className="spinner" /></div>;
  }

  if (!user) {
    return <Navigate to="/login" />;
  }

  if (role && user.role !== role && user.role !== 'admin') {
    return <Navigate to="/" />; // Admins can bypass some constraints or we just redirect
  }

  return children;
}
