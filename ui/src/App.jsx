import { useState, useRef } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import './App.css';

import BasicNavbar from './components/nav';
import Home from './pages/home';
import Team from './pages/teams';
import CircularLayout from './pages/about';
import Feature from './components/features';
import Footer from './components/footer';
import Dashboard from './pages/dashboard';
function App() {
  // References to sections
  const homeRef = useRef(null);
  const aboutRef = useRef(null);
  const teamRef = useRef(null);
  const dashRef = useRef(null);

  // Function to scroll to a section
  const scrollToSection = (ref) => {
    ref.current.scrollIntoView({ behavior: 'smooth' });
  };
  // const response = await axios.post('http://127.0.0.1:5000/predict', formData);

  // const fetchPrediction = async (data) => {
  //   const response = await axios.post('http://127.0.0.1:8000/api/predict', data);
  //   return response.data;
  // };
  return (
    <Router>
      <BasicNavbar scrollToSection={scrollToSection} refs={{ homeRef,dashRef, aboutRef, teamRef }} />
      
      {/* Define routes */}
      {/* <Routes>
        <Route path="/" element={<FormPage />} />
      </Routes> */}
      <div className="h-8"></div>
      <div ref={homeRef}>
        <Home />
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
       
      
      <Footer />
    </Router>
  );
}

export default App;
