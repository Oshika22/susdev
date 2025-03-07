import { useState, useEffect } from "react";
import { Link } from 'react-router-dom';
import Dashboard from './dashboard';

const Home = ({ scrollToSection, refs }) => {
      const [scroll, setScroll] = useState(false);
    
      useEffect(() => {
        const handleScroll = () => {
          if (window.scrollY > 50) {
            setScroll(true);
          } else {
            setScroll(false);
          }
        };
    
        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
      }, []);
    return(
        <>
        <div className='w-full flex flex-col justify-center items-center text-shadow'>
            <div className="text-[#3E3E3E] text-[40px] font-semibold font-['inter'] m-4">Optimizing Urban Life with AI & Data</div>
            <div className='flex justify-around items-start w-full'>
                <div className='text-[#333333] m-4'>
                    <div className='w-3/4 text-justify'>
                    Welcome to our AI-Driven Sustainable Cities Dashboard — designed to revolutionize urban living through advanced technology. Our AI-powered platform predicts air quality, traffic flow, energy usage, and waste patterns — offering data-driven insights to build smarter, greener cities. With a focus on sustainability and innovation, we're here to empower city planners and communities alike. Discover how AI can shape a more efficient, eco-friendly future.
                    </div>
                    
                    <button onClick={() => scrollToSection(refs.dashRef)} className="w-[120px] h-[50px] bg-gradient-to-b from-purple-800 to-purple-500 rounded-[15px] shadow-lg font-semibold text-[#333333] m-4 transition-transform duration-300 hover:scale-105 hover:from-purple-500 hover:to-purple-800">Get Started</button>
                    
                    
                </div>
                <div className='w-[500px] h-[300px] bg-zinc-300 rounded-l-full'></div>

            </div>
        </div>
        </>
    );
};

export default Home;