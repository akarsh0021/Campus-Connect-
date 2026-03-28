/**
 * Landing Page — Hero, features, and CTA for the Campus Placement Portal.
 */
import { Link } from 'react-router-dom';
import {
  GraduationCap,
  Building2,
  BrainCircuit,
  BarChart3,
  Shield,
  Zap,
  ArrowRight,
  Users,
  Briefcase,
  TrendingUp,
} from 'lucide-react';
import './Landing.css';

const FEATURES = [
  {
    icon: <BrainCircuit size={28} />,
    title: 'AI-Powered Matching',
    desc: 'Our intelligent ranking engine analyzes skills, experience, and CGPA to match students with the best opportunities.',
    color: 'blue',
  },
  {
    icon: <BarChart3 size={28} />,
    title: 'Smart Analytics',
    desc: 'Real-time dashboards for placement officers with department-wise stats, skill trends, and placement rates.',
    color: 'purple',
  },
  {
    icon: <Zap size={28} />,
    title: 'Resume Parsing',
    desc: 'Upload your resume and let AI extract skills, experience, and education automatically.',
    color: 'amber',
  },
  {
    icon: <Shield size={28} />,
    title: 'Role-Based Access',
    desc: 'Separate dashboards for students, companies, and admins with tailored features for each.',
    color: 'emerald',
  },
];

const STATS = [
  { value: '500+', label: 'Students Placed', icon: <Users size={24} /> },
  { value: '50+', label: 'Partner Companies', icon: <Building2 size={24} /> },
  { value: '200+', label: 'Job Openings', icon: <Briefcase size={24} /> },
  { value: '92%', label: 'Placement Rate', icon: <TrendingUp size={24} /> },
];

export default function Landing() {
  return (
    <div className="landing">
      {/* ── Hero Section ──────────────────────── */}
      <section className="hero">
        <div className="hero-bg">
          <div className="hero-orb orb-1"></div>
          <div className="hero-orb orb-2"></div>
          <div className="hero-orb orb-3"></div>
        </div>
        <div className="container hero-content">
          <div className="hero-badge animate-in">
            <BrainCircuit size={16} />
            AI-Powered Campus Recruitment
          </div>
          <h1 className="hero-title animate-in animate-in-delay-1">
            Your Gateway to
            <span className="gradient-text"> Dream Careers</span>
          </h1>
          <p className="hero-subtitle animate-in animate-in-delay-2">
            CampusConnect bridges the gap between talented students and top companies
            using AI-driven shortlisting, smart analytics, and seamless placement workflows.
          </p>
          <div className="hero-actions animate-in animate-in-delay-3">
            <Link to="/register" className="btn btn-primary btn-xl">
              Get Started <ArrowRight size={20} />
            </Link>
            <Link to="/login" className="btn btn-secondary btn-xl">
              Sign In
            </Link>
          </div>
        </div>
      </section>

      {/* ── Stats Bar ─────────────────────────── */}
      <section className="stats-bar">
        <div className="container">
          <div className="stats-grid">
            {STATS.map((stat, i) => (
              <div key={i} className={`stats-item animate-in animate-in-delay-${i + 1}`}>
                <div className="stats-icon">{stat.icon}</div>
                <div>
                  <div className="stats-value">{stat.value}</div>
                  <div className="stats-label">{stat.label}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Features ──────────────────────────── */}
      <section className="features-section">
        <div className="container">
          <div className="section-header">
            <h2>Why CampusConnect?</h2>
            <p>Everything you need for a modern campus placement process</p>
          </div>
          <div className="features-grid">
            {FEATURES.map((f, i) => (
              <div key={i} className={`feature-card feature-${f.color} animate-in`}>
                <div className="feature-icon">{f.icon}</div>
                <h3>{f.title}</h3>
                <p>{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── How it works ──────────────────────── */}
      <section className="how-section">
        <div className="container">
          <div className="section-header">
            <h2>How It Works</h2>
            <p>Three simple steps to your next opportunity</p>
          </div>
          <div className="steps-grid">
            <div className="step-card animate-in">
              <div className="step-number">01</div>
              <h3>Create Your Profile</h3>
              <p>Sign up, fill in your details, and upload your resume. Our AI will extract your skills automatically.</p>
            </div>
            <div className="step-card animate-in animate-in-delay-1">
              <div className="step-number">02</div>
              <h3>Discover Opportunities</h3>
              <p>Browse AI-recommended jobs tailored to your skills, or search the full listing. Apply with one click.</p>
            </div>
            <div className="step-card animate-in animate-in-delay-2">
              <div className="step-number">03</div>
              <h3>Get Placed</h3>
              <p>Companies review AI-ranked candidates and shortlist the best matches. Track your status in real time.</p>
            </div>
          </div>
        </div>
      </section>

      {/* ── CTA ───────────────────────────────── */}
      <section className="cta-section">
        <div className="container">
          <div className="cta-box">
            <h2>Ready to Transform Campus Placements?</h2>
            <p>Join CampusConnect today and experience the future of recruitment.</p>
            <div className="cta-actions">
              <Link to="/register" className="btn btn-primary btn-xl">
                <GraduationCap size={20} /> Student Sign Up
              </Link>
              <Link to="/register" className="btn btn-success btn-xl">
                <Building2 size={20} /> Company Sign Up
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ── Footer ────────────────────────────── */}
      <footer className="landing-footer">
        <div className="container">
          <div className="footer-inner">
            <div className="footer-brand">
              <GraduationCap size={24} />
              <span>CampusConnect</span>
            </div>
            <p>&copy; {new Date().getFullYear()} CampusConnect. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
