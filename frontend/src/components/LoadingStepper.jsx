import React, { useState, useEffect } from 'react';

const LoadingStepper = () => {
  const steps = [
    { title: "Sending Request", desc: "Connecting to API" },
    { title: "Running Agents", desc: "Planner is thinking" },
    { title: "Preparing Result", desc: "Validating plan" }
  ];

  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    // Simulate progression of steps
    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev < steps.length - 1 ? prev + 1 : prev));
    }, 1500);

    return () => clearInterval(interval);
  }, [steps.length]);

  return (
    <div className="bg-white p-8 rounded-lg shadow-sm border border-gray-100 flex flex-col items-center justify-center min-h-[300px] h-full">
      <div className="mb-10">
        <div className="w-12 h-12 rounded-full border-4 border-indigo-100 border-t-indigo-600 animate-spin mx-auto"></div>
      </div>
      
      <div className="w-full max-w-md">
        <div className="relative">
          <div className="absolute inset-0 flex items-center" aria-hidden="true">
            <div className="w-full border-t-2 border-gray-100"></div>
          </div>
          <div className="relative flex justify-between">
            {steps.map((step, index) => {
              const isActive = index === currentStep;
              const isPast = index < currentStep;
              
              return (
                <div key={index} className="flex flex-col items-center group">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold shadow-sm transition-colors ${
                    isPast ? 'bg-indigo-600 text-white border-2 border-indigo-600' : 
                    isActive ? 'bg-white border-2 border-indigo-600 text-indigo-600' : 'bg-white border-2 border-gray-300 text-gray-400'
                  }`}>
                    {isPast ? (
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"></path></svg>
                    ) : (
                      index + 1
                    )}
                  </div>
                  <div className={`mt-3 text-center absolute top-8 w-32 -ml-12 ${isActive ? 'text-indigo-600 font-semibold' : isPast ? 'text-gray-800' : 'text-gray-400'}`}>
                    <div className="text-sm">{step.title}</div>
                    {isActive && <div className="text-xs mt-0.5 text-indigo-500 animate-pulse">{step.desc}</div>}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingStepper;
