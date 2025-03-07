// CircularLayout.jsx

import React, { useEffect, useRef } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBullseye, faFlag, faEye } from '@fortawesome/free-solid-svg-icons';

const CircularLayout = () => {
  return (
    <div className="relative py-20">
      <div className="container mx-auto">
        <h2 className="text-center text-4xl font-bold">
          Our Aim, Mission, and Vision
        </h2>
        <div className="mt-12 flex justify-between gap-2 text-justify
        ">
          <div className="text-center w-1/3">
            <FontAwesomeIcon
              icon={faBullseye}
              size="3x"
              className="text-purple-700"
            />
            <h3 className="mt-4 text-xl font-semibold">Our Aim</h3>
            <p className="text-lg opacity-80">
            To leverage AI and data-driven insights for optimizing urban sustainability, improving resource efficiency, and enhancing city living.
            </p>
          </div>
          <div className="text-center w-1/3">
            <FontAwesomeIcon
              icon={faFlag}
              size="3x"
              className="text-purple-700"
            />
            <h3 className="mt-4 text-xl font-semibold">Our Mission</h3>
            <p className="text-lg opacity-80">
            To provide an AI-powered platform that predicts environmental trends, optimizes resource usage, and offers actionable solutions for smarter, greener cities.
            </p>
          </div>
          <div className="text-center w-1/3">
            <FontAwesomeIcon
              icon={faEye}
              size="3x"
              className="text-purple-700"
            />
            <h3 className="mt-4 text-xl font-semibold">Our Vision</h3>
            <p className="text-lg opacity-80">
            To create a future where cities operate sustainably, efficiently, and intelligently, ensuring a healthier environment and improved quality of life for all.
            </p>
          </div>
        </div>
      </div>
      <div className="py-16 bg-purple-100">
        <div className="container mx-auto text-center">
          <h2 className="text-4xl font-bold text-[#3E3E3E]">Why We Care</h2>
          <p className="mt-4 text-lg text-[#3E3E3E]">
          Our goal is to enhance urban sustainability by leveraging AI-driven insights, enabling smarter resource management, reducing environmental impact, and improving city living.
          </p>
        </div>
      </div>
    </div>
  );
};

export default CircularLayout;
