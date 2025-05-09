import React from 'react'
import { air11, air2 } from '../assets/images'
export const Air = () => {
  return (
    <div className='flex flex-col justify-center items-center m-14 gap-8'>
        <h1 className='text-5xl mt-8 bg-gradient-to-r from-purple-900 via-slate-600 to-purple-950 text-transparent bg-clip-text'>Air Quality Analysis</h1>
        <div className='flex flex-col justify-center items-center'>
            <h1 className='font-yatra bg-gradient-to-r from-purple-900 via-slate-700 to-purple-950 text-transparent bg-clip-text m-4'>AQI Trend</h1>
            <h5>This shows predicted AQI values for a future time period (here: April 2025).
                X-axis = date
                Y-axis = predicted AQI</h5>
            <img src={air11} alt="AQI trend" />
            <h5 className='text-justify w-2/3'>The model predicts an air quality level of approximately 2.67, which corresponds to a likely category between ‘Unhealthy for Sensitive Groups’ and ‘Unhealthy’ based on our training scale.</h5>
        </div>
        <div className='flex flex-col justify-center items-center'>
            <h1 className='font-yatra bg-gradient-to-r from-purple-900 via-slate-700 to-purple-950 text-transparent bg-clip-text m-4'>Model Performance: Predicted vs Actual AQI Values</h1>
            <h5>This shows predicted v/s Actual AQI values.
                X-axis = data value
                Y-axis = sample index</h5>
            <img src={air2} alt="AQI map" />
            <h5 className='text-justify'>Model Mean Squared Error (MSE): 52.57 – indicates the average squared difference between actual and predicted AQI values.<br />

                MAE = 5.89 – indicates the average absolute difference between actual and predicted AQI values.<br />
                R<sup>2</sup> = 0.76 – indicates the proportion of variance in the actual AQI values that is predictable from the independent variables.<br />
            </h5>
        </div>
    </div>
  )
}
