import { useRef } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';

import BasicNavbar from './components/nav';
import Home from './pages/home';
import Team from './pages/teams';
import CircularLayout from './pages/about';
import Feature from './components/features';
import Footer from './components/footer';
import Dashboard from './pages/dashboard';
import { Air } from './modelDisplay/Air';

function MainContent() {
  const location = useLocation();
  const homeRef = useRef(null);
  const aboutRef = useRef(null);
  const teamRef = useRef(null);
  const dashRef = useRef(null);

  const scrollToSection = (ref) => {
    ref.current.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className='bg-slate-50'>
      <BasicNavbar scrollToSection={scrollToSection} refs={{ homeRef, dashRef, aboutRef, teamRef }} />

      {/* Conditional rendering based on route */}
      {location.pathname === '/' && (
        <>
          <div ref={homeRef}>
            <Home scrollToSection={scrollToSection} refs={{ dashRef }} />
          </div>
          <div ref={aboutRef}>
            <CircularLayout />
          </div>
          <Feature />
          <div ref={dashRef}>
            <Dashboard />
          </div>
          <div ref={teamRef}>
            <Team />
          </div>
        </>
      )}

      {location.pathname === '/air' && <Air />}

      <Footer />
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="*" element={<MainContent />} />
      </Routes>
    </Router>
  );
}

export default App;
