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
    <div className="glass-card rounded-2xl p-10 flex flex-col items-center justify-center min-h-[400px] h-full relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-t from-indigo-50/30 to-transparent"></div>
      <div className="mb-12 relative z-10">
        <div className="relative">
          <div className="w-16 h-16 rounded-full border-4 border-indigo-100/50 border-t-indigo-500 animate-spin mx-auto"></div>
          <div className="absolute inset-0 flex items-center justify-center">
             <div className="w-8 h-8 bg-indigo-500/20 rounded-full blur-md animate-pulse"></div>
          </div>
        </div>
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
                <div key={index} className="flex flex-col items-center group z-10">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold shadow transition-all duration-500 ${
                    isPast ? 'bg-indigo-500 text-white border-2 border-indigo-500 scale-110' : 
                    isActive ? 'bg-white border-2 border-indigo-500 text-indigo-600 shadow-indigo-200 shadow-lg scale-110' : 'bg-white/80 border-2 border-slate-200 text-slate-400'
                  }`}>
                    {isPast ? (
                      <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"></path></svg>
                    ) : (
                      index + 1
                    )}
                  </div>
                  <div className={`mt-4 text-center absolute top-10 w-32 -ml-12 ${isActive ? 'text-indigo-600' : isPast ? 'text-slate-700' : 'text-slate-400'}`}>
                    <div className={`text-sm font-medium ${isActive ? 'font-bold' : ''}`}>{step.title}</div>
                    {isActive && <div className="text-xs mt-1 text-indigo-500/80 animate-pulse">{step.desc}</div>}
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
