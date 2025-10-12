import React, { useState, useEffect } from "react";
import { NavLink, useLocation } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import ThemeToggle from "./ThemeToggle.jsx";
import "./Header.css";
const MobileMenu = ({ isOpen, onClose, links }) => (
  <AnimatePresence>
    {isOpen && (
      <>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="mobile-overlay"
          onClick={onClose}
        />
        <motion.div
          initial={{ x: "100%" }}
          animate={{ x: 0 }}
          exit={{ x: "100%" }}
          transition={{ type: "spring", damping: 25, stiffness: 120 }}
          className="mobile-menu"
        >
          <div className="mobile-menu-header">
            <div className="mobile-logo">
              <span className="logo-icon">🌉</span>
              <span className="logo-text">MarketBridge</span>
            </div>
            <button onClick={onClose} className="close-btn">
              ✕
            </button>
          </div>
          
          <nav className="mobile-nav">
            {links.map(({ to, label, icon }) => (
              <NavLink
                key={to}
                to={to}
                onClick={onClose}
                className={({ isActive }) => 
                  `mobile-nav-link ${isActive ? 'active' : ''}`
                }
                end={to === "/"}
              >
                <span className="nav-icon">{icon}</span>
                <span className="nav-text">{label}</span>
              </NavLink>
            ))}
          </nav>

          <div className="mobile-menu-footer">
            <ThemeToggle />
          </div>
        </motion.div>
      </>
    )}
  </AnimatePresence>
);

const Logo = () => (
  <motion.div
    whileHover={{ scale: 1.05 }}
    className="header-logo"
  >
    <div className="logo-container">
      <div className="logo-icon">🌉</div>
      <div className="logo-content">
        <div className="logo-text">MarketBridge</div>
        <div className="logo-tagline">AI Marketing Platform</div>
      </div>
    </div>
  </motion.div>
);

const NotificationBadge = ({ count }) => (
  count > 0 && (
    <motion.div
      initial={{ scale: 0 }}
      animate={{ scale: 1 }}
      className="notification-badge"
    >
      {count > 99 ? '99+' : count}
    </motion.div>
  )
);

export default function Header() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [notifications] = useState(3); // Mock notification count
  const location = useLocation();

  const navigationLinks = [
    { to: "/", label: "Home", icon: "🏠" },
    { to: "/campaign", label: "Campaign", icon: "🚀" },
    { to: "/agents", label: "Agents", icon: "🤖" },
  ];

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    setIsMobileMenuOpen(false);
  }, [location.pathname]);

  return (
    <>
      <motion.header
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.6 }}
        className={`main-header ${isScrolled ? 'scrolled' : ''}`}
      >
        <div className="header-container">
          {/* Logo Section */}
          <NavLink to="/" className="logo-link">
            <Logo />
          </NavLink>

          {/* Desktop Navigation */}
          <nav className="desktop-nav">
            {navigationLinks.map(({ to, label, icon }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) => 
                  `nav-link ${isActive ? 'active' : ''}`
                }
                end={to === "/"}
              >
                <span className="nav-icon">{icon}</span>
                <span className="nav-text">{label}</span>
                {label === "Campaign" && <NotificationBadge count={notifications} />}
              </NavLink>
            ))}
          </nav>

          {/* Header Actions */}
          <div className="header-actions">
            {/* Theme Toggle - Desktop */}
            <div className="desktop-only">
              <ThemeToggle />
            </div>

            {/* User Menu */}
            <div className="user-menu">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="user-avatar"
              >
                <span className="avatar-icon">👤</span>
              </motion.button>
            </div>

            {/* Mobile Menu Button */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="mobile-menu-btn"
              onClick={() => setIsMobileMenuOpen(true)}
            >
              <span className="hamburger-line"></span>
              <span className="hamburger-line"></span>
              <span className="hamburger-line"></span>
            </motion.button>
          </div>
        </div>

        {/* Progress Bar for Campaign/Agents pages */}
        {(location.pathname === '/campaign' || location.pathname === '/agents') && (
          <div className="header-progress">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: "100%" }}
              transition={{ duration: 2, ease: "easeInOut" }}
              className="progress-bar"
            />
          </div>
        )}
      </motion.header>

      {/* Mobile Menu */}
      <MobileMenu 
        isOpen={isMobileMenuOpen}
        onClose={() => setIsMobileMenuOpen(false)}
        links={navigationLinks}
      />
    </>
  );
}
