import { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import bgImg from "../assets/images/bg.jpg"; // Adjust the path as necessary
import { bgweb, i1, i2, i3, bg4, globe } from "../assets/images/index"; // Adjust the path as necessary
import Dashboard from './dashboard';

const Home = ({ scrollToSection, refs }) => {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <>
      <div
        className={`w-full h-[600px] flex flex-col justify-center items-center text-shadow transition-all duration-300 
        ${scrolled ? "bg-white shadow-md" : "bg-transparent"} 
        bg-cover bg-center`}
        style={{
          backgroundImage: `url(${bgImg})`,
        }}
      >
        <div className="flex flex-col justify-center items-center w-full h-screen bg-white bg-opacity-50">
        
            {/* <div className="text-[#000000] text-[40px] font-semibold font-['inter'] m-2 text-center">
              Optimizing Urban Life with AI & Data
            </div> */}
    
            <div className="flex flex-col md:flex-row justify-around items-start w-full p-6">
              <div className="m-4 md:w-1/2  text-[20px] text-center md:text-left">
                <div className="text-[40px] font-semibold font-Limelight m-2 text-center bg-gradient-to-r from-purple-950 via-purple-500 to-purple-950 text-transparent bg-clip-text">
                    UrbanOptima
                </div>
                <h1 className="text-[35px] font-semibold font-yatra mb-4 text-center  bg-gradient-to-r from-purple-700 via-slate-500 to-purple-800 text-transparent bg-clip-text">
                      Optimizing Urban Life with AI & Data
                </h1>
                <div className="text-justify font-bold text-black">
                  Welcome to our AI-Driven Sustainable Cities Dashboard, designed to revolutionize urban living through advanced technology. Our AI-powered platform predicts air quality, traffic flow, energy usage, and waste patterns, offering data-driven insights to build smarter, greener cities. With a focus on sustainability and innovation, we're here to empower city planners and communities alike. Discover how AI can shape a more efficient, eco-friendly future.
                </div>
    
                <button
                  onClick={() => scrollToSection(refs.dashRef)}
                  className="w-[120px] h-[50px] bg-gradient-to-b from-purple-800 to-purple-500 rounded-[15px] shadow-lg text-[#fff] border-2 border-zinc-300 mt-6 transition-transform duration-300 hover:scale-105 hover:from-purple-500 hover:to-purple-800"
                >
                  Get Started
                </button>
          </div>
          <div className="circicon w-[200px] h-[200px] rounded-full bg-zinc-300 hidden md:block mt-4 shadow-lg shadow-black" style={{
          backgroundImage: `url(${i1})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}></div>
          <div className="circicon w-[230px] h-[230px] rounded-full bg-zinc-300 border-3 border-white hidden md:block mt-40 shadow-lg shadow-black" style={{
          backgroundImage: `url(${i3})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}></div>
        </div>
    
          {/* Optional image or visual block */}
          {/* <div className="w-[300px] h-[300px] rounded-full bg-zinc-300 hidden md:block"></div> */}
        </div>
      </div>
    </>
  );
};

export default Home;
