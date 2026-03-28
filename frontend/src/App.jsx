import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar/Navbar';

// Pages
import Landing from './pages/Landing/Landing';
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import Jobs from './pages/Jobs/Jobs';

// Student Pages
import StudentDashboard from './pages/Student/StudentDashboard';
import StudentProfile from './pages/Student/StudentProfile';
import StudentApplications from './pages/Student/StudentApplications';

// Company Pages
import CompanyDashboard from './pages/Company/CompanyDashboard';
import CompanyProfile from './pages/Company/CompanyProfile';
import PostJob from './pages/Company/PostJob';
import Candidates from './pages/Company/Candidates';

// Admin Pages
import AdminDashboard from './pages/Admin/AdminDashboard';
import AdminUsers from './pages/Admin/AdminUsers';
import AdminPlacements from './pages/Admin/AdminPlacements';

// Protected Route Component
const ProtectedRoute = ({ children, role }) => {
  const { user, loading } = useAuth();

  if (loading) return <div className="loading-screen"><div className="spinner" /></div>;
  if (!user) return <Navigate to="/login" replace />;
  if (role && user.role !== role && user.role !== 'admin') {
    return <Navigate to="/" replace />;
  }
  return children;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/jobs" element={<Jobs />} />

          {/* Student Routes */}
          <Route path="/student" element={
            <ProtectedRoute role="student"><StudentDashboard /></ProtectedRoute>
          } />
          <Route path="/student/profile" element={
            <ProtectedRoute role="student"><StudentProfile /></ProtectedRoute>
          } />
          <Route path="/student/applications" element={
            <ProtectedRoute role="student"><StudentApplications /></ProtectedRoute>
          } />

          {/* Company Routes */}
          <Route path="/company" element={
            <ProtectedRoute role="company"><CompanyDashboard /></ProtectedRoute>
          } />
          <Route path="/company/profile" element={
            <ProtectedRoute role="company"><CompanyProfile /></ProtectedRoute>
          } />
          <Route path="/company/post-job" element={
            <ProtectedRoute role="company"><PostJob /></ProtectedRoute>
          } />
          <Route path="/company/jobs/:jobId/candidates" element={
            <ProtectedRoute role="company"><Candidates /></ProtectedRoute>
          } />

          {/* Admin Routes */}
          <Route path="/admin" element={
            <ProtectedRoute role="admin"><AdminDashboard /></ProtectedRoute>
          } />
          <Route path="/admin/users" element={
            <ProtectedRoute role="admin"><AdminUsers /></ProtectedRoute>
          } />
          <Route path="/admin/placements" element={
            <ProtectedRoute role="admin"><AdminPlacements /></ProtectedRoute>
          } />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
