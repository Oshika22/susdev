import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faWind, faCarOn, faPlug, faArrowUpFromWaterPump, faDumpsterFire } from '@fortawesome/free-solid-svg-icons';
import { air1 } from '../assets/images/index.js';
import { useNavigate } from 'react-router-dom';
import { Button } from 'react-bootstrap';
export default function Dashboard() {
    const navigate = useNavigate();
    return (
        <div>
            <div>
                <h1 className="text-6xl text-[#333333] font-semibold mb-6 text-center">Dashboard</h1>
                <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-3 m-4'>
                    <div className='w-1/1 h-60 bg-gradient-to-b from-slate-700 to-purple-700 rounded-[15px] border-1 border-[#704886] shadow-lg p-2 font-semibold text-white transition-transform duration-300 hover:scale-105 '>City name, Map(displayed different aspects)</div>
                    <button 
                    onClick={() => navigate('/air')}
                    className='flex flex-col justify-center items-center w-1/1 h-60 bg-gradient-to-b from-slate-700 to-purple-700 rounded-[15px] border-1 border-[#704886] shadow-lg p-2 font-semibold text-white transition-transform duration-300 hover:scale-105 '
                    >
                        <h2 className='m-2 font-semibold text-purple-100'>Air Quality</h2>
                        <FontAwesomeIcon icon={faWind} size='5x' className='m-2 text-purple-500'/>
                        <h4 className='text-purple-100'>Air Quality Index: 2.61 (Sensitive)</h4>
                    </button>
                    <button 
                    className='w-1/1 h-60 bg-gradient-to-b from-slate-700 to-purple-700 rounded-[15px] border-1 border-[#704886] shadow-lg p-2 font-semibold text-white transition-transform duration-300 hover:scale-105 '>
                        <h3 className='m-2 font-semibold text-purple-100'>Traffic Congestion Forecasting</h3>
                        <FontAwesomeIcon icon={faCarOn} size='5x' className='m-2 text-purple-500'/>
                        <h4>Traffic Density Map & Time-Series Line Chart</h4></button>
                    <button 
                    className='w-1/1 h-60 bg-gradient-to-b from-slate-700 to-purple-700 rounded-[15px] border-1 border-[rgb(112,72,134)] shadow-lg p-2 font-semibold text-white transition-transform duration-300 hover:scale-105 '>
                        <h3 className='m-2 font-semibold text-purple-100'>Energy Usuage</h3>
                        <FontAwesomeIcon icon={faPlug} size='5x' className='m-2 text-purple-500'/>
                        <h4>Insights (tacked Area Chart )</h4></button>
                    <button 
                    className='w-1/1 h-60 bg-gradient-to-b from-slate-700 to-purple-700 rounded-[15px] border-1 border-[#704886] shadow-lg p-2 font-semibold text-white transition-transform duration-300 hover:scale-105 '>
                        <h3 className='m-2 font-semibold text-purple-100'>Water Usuage</h3>
                        <FontAwesomeIcon icon={faArrowUpFromWaterPump} size='5x' className='m-2 text-purple-500'/>
                        
                        <h4>Water Usage Optimization (Bar Chart )</h4></button>
                    <button 
                    className='w-1/1 h-60 bg-gradient-to-b from-slate-700 to-purple-700 rounded-[15px] border-1 border-[#704886] shadow-lg p-2 font-semibold text-white transition-transform duration-300 hover:scale-105 '>
                        <h4 className='m-2 font-semibold text-purple-100'>WasteWaste Management Optimization</h4>
                        <FontAwesomeIcon icon={faDumpsterFire} size='5x' className='m-2 text-purple-500'/>
                        
                        <h4>Pie Chart & Route Optimization Map</h4>
                        </button>
                    
                </div>
                <div className='w-1/1 h-60 bg-gradient-to-b from-slate-700 to-purple-700 rounded-[15px] border-1 border-[#704886] shadow-lg p-2 font-semibold text-white m-4 transition-transform duration-300 hover:scale-95 '>Overall</div>
            </div>
        </div>
    );
};
