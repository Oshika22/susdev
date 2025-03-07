import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDownload, faRobot, faChartBar } from '@fortawesome/free-solid-svg-icons';

export default function Dashboard() {
    return (
        <div>
            <div>
                <h1 className="text-6xl text-[#333333] font-semibold mb-6 text-center text-shadow ">Dashboard</h1>
                <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-3 m-4'>
                    <div className='w-1/1 h-60 bg-gradient-to-b from-[#2E1F37] to-[#84589D] rounded-[15px] border-1 border-[#704886] shadow-lg p-2 font-semibold text-white transition-transform duration-300 hover:scale-105 '>City name, Map(displayed different aspects)</div>
                    <div className='w-1/1 h-60 bg-gradient-to-b from-[#2E1F37] to-[#84589D] rounded-[15px] border-1 border-[#704886] shadow-lg p-2 font-semibold text-white transition-transform duration-300 hover:scale-105 '>Air quality monitering (heat map)</div>
                    <div className='w-1/1 h-60 bg-gradient-to-b from-[#2E1F37] to-[#84589D] rounded-[15px] border-1 border-[#704886] shadow-lg p-2 font-semibold text-white transition-transform duration-300 hover:scale-105 '>Traffic Congestion Forecasting(Traffic Density Map & Time-Series Line Chart)</div>
                    <div className='w-1/1 h-60 bg-gradient-to-b from-[#2E1F37] to-[#84589D] rounded-[15px] border-1 border-[rgb(112,72,134)] shadow-lg p-2 font-semibold text-white transition-transform duration-300 hover:scale-105 '>Energy Usage Insights (tacked Area Chart )</div>
                    <div className='w-1/1 h-60 bg-gradient-to-b from-[#2E1F37] to-[#84589D] rounded-[15px] border-1 border-[#704886] shadow-lg p-2 font-semibold text-white transition-transform duration-300 hover:scale-105 '>Water Usage Optimization (Bar Chart )</div>
                    <div className='w-1/1 h-60 bg-gradient-to-b from-[#2E1F37] to-[#84589D] rounded-[15px] border-1 border-[#704886] shadow-lg p-2 font-semibold text-white transition-transform duration-300 hover:scale-105 '>WasteWaste Management Optimization (Pie Chart & Route Optimization Map)</div>
                    
                </div>
                <div className='w-1/1 h-60 bg-gradient-to-b from-[#2E1F37] to-[#84589D] rounded-[15px] border-1 border-[#704886] shadow-lg p-2 font-semibold text-white m-4 transition-transform duration-300 hover:scale-95 '>Overall</div>
            </div>
        </div>
    );
};
