import { useRef } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';

import BasicNavbar from './components/nav';
import Home from './pages/home';
import Team from './pages/teams';
import CircularLayout from './pages/about';
import Feature from './components/features';
import Footer from './components/footer';
import Dashboard from './pages/dashboard';
import Air from './modelDisplay/Air';
import Traffic from './modelDisplay/Traffic';
import '@tomtom-international/web-sdk-maps/dist/maps.css';

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
      <div><BasicNavbar scrollToSection={scrollToSection} refs={{ homeRef, dashRef, aboutRef, teamRef }} /></div>

      {location.pathname === '/air' && <Air />}
      {location.pathname === '/traffic' && <Traffic />}
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
