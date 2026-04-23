import React, { useState } from 'react';
import InputForm from '../components/InputForm';
import ItineraryCard from '../components/ItineraryCard';
import BudgetBreakdown from '../components/BudgetBreakdown';
import ValidationStatus from '../components/ValidationStatus';
import AgentLogs from '../components/AgentLogs';
import LoadingStepper from '../components/LoadingStepper';
import { planTrip } from '../api/travelApi';

const Home = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const handlePlanTrip = async (data) => {
    setIsLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await planTrip(data);
      setResult(response);
    } catch (err) {
      setError(
        err?.response?.data?.detail
          ? `Backend error: ${JSON.stringify(err.response.data.detail)}`
          : 'Could not connect to backend. Please make sure the FastAPI server is running at http://127.0.0.1:8000.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen relative overflow-hidden bg-slate-50 py-12 px-4 sm:px-6 lg:px-8 font-sans">
      {/* Background Orbs */}
      <div className="absolute top-0 -left-4 w-96 h-96 bg-purple-200 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob"></div>
      <div className="absolute top-0 -right-4 w-96 h-96 bg-indigo-200 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob" style={{ animationDelay: '2s' }}></div>
      <div className="absolute -bottom-8 left-1/2 w-96 h-96 bg-pink-200 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob" style={{ animationDelay: '4s' }}></div>

      <div className="relative max-w-6xl mx-auto space-y-10 z-10">
        
        {/* Header Section */}
        <div className="text-center space-y-4 animate-fade-in-up">
          <div className="inline-flex items-center justify-center p-1.5 bg-white/60 backdrop-blur-sm rounded-full mb-2 border border-slate-200/50 shadow-sm">
            <span className="text-indigo-600 text-xs font-semibold tracking-wider uppercase px-3">AI Powered</span>
          </div>
          <h1 className="text-4xl font-extrabold font-outfit text-slate-900 sm:text-5xl tracking-tight">
            Multi-Agent <span className="text-transparent bg-clip-text bg-gradient-to-r from-violet-600 to-indigo-600">Travel Planner</span>
          </h1>
          <p className="max-w-2xl mx-auto text-lg text-slate-500 font-medium">
            Intelligent, personalized itinerary generation designed to build your dream trip in seconds.
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded shadow-sm flex items-start max-w-3xl mx-auto">
            <svg className="h-6 w-6 text-red-500 mr-3 mt-0.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <div>
              <h3 className="text-lg font-medium text-red-800">Connection Error</h3>
              <p className="mt-1 text-sm text-red-700">{error}</p>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column: Form */}
          <div className="lg:col-span-1">
            <InputForm onSubmit={handlePlanTrip} isLoading={isLoading} />
          </div>

          {/* Right Column: Output */}
          <div className="lg:col-span-2 space-y-6">
            {isLoading && <LoadingStepper />}
            
            {!isLoading && !result && !error && (
              <div className="glass-card rounded-2xl flex flex-col items-center justify-center text-center h-full min-h-[400px] p-10 relative overflow-hidden group">
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-50/50 to-purple-50/50 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                <div className="relative z-10">
                  <div className="bg-white/80 p-5 rounded-2xl shadow-sm mb-6 inline-block transform group-hover:-translate-y-2 transition-all duration-300">
                    <svg className="w-12 h-12 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                  </div>
                  <h3 className="text-2xl font-semibold font-outfit text-slate-800 mb-3">Ready to plan</h3>
                  <p className="text-slate-500 max-w-sm mx-auto leading-relaxed">Enter your destination, days, budget, and preferences to build your ideal itinerary.</p>
                </div>
              </div>
            )}

            {!isLoading && result && (
              <div className="space-y-6">
                {/* Trip Summary Card */}
                <div className="glass-card rounded-2xl p-6 grid grid-cols-2 md:grid-cols-4 gap-4 animate-fade-in-up">
                  <div className="md:border-r border-slate-200/50 px-2">
                    <p className="text-sm text-slate-500 font-medium tracking-wide uppercase">Destination</p>
                    <p className="text-xl font-bold font-outfit text-slate-900 mt-1">{result.destination}</p>
                  </div>
                  <div className="md:border-r border-slate-200/50 px-2 md:px-4">
                    <p className="text-sm text-slate-500 font-medium tracking-wide uppercase">Duration</p>
                    <p className="text-xl font-bold font-outfit text-slate-900 mt-1">{result.days} <span className="text-lg font-medium text-slate-600">Days</span></p>
                  </div>
                  <div className="md:border-r border-slate-200/50 px-2 md:px-4">
                    <p className="text-sm text-slate-500 font-medium tracking-wide uppercase">Budget</p>
                    <p className="text-xl font-bold font-outfit text-slate-900 mt-1"><span className="text-lg font-medium text-slate-600">Rs. </span>{result.budget}</p>
                  </div>
                  <div className="px-2 md:px-4">
                    <p className="text-sm text-slate-500 font-medium tracking-wide uppercase mb-1">Preferences</p>
                    <div className="flex flex-wrap gap-1.5 mt-1">
                      {(result.preferences || []).map((p, i) => (
                        <span key={i} className="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-indigo-50/80 text-indigo-700 border border-indigo-200/60 shadow-sm">
                          {p}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <ItineraryCard itinerary={result.itinerary} />
                  
                  <div className="space-y-6 flex flex-col">
                    <BudgetBreakdown breakdown={result.cost_breakdown} total={result.total_cost} />
                    <ValidationStatus 
                      status={result.validation_status} 
                      errors={result.validation_errors} 
                      recommendedChanges={result.recommended_changes} 
                    />
                  </div>
                </div>

                {/* Planner Output Card */}
                <div className="glass-card rounded-2xl p-6">
                  <h3 className="text-xl font-semibold font-outfit text-slate-800 mb-4 flex items-center">
                    <span className="p-2 bg-purple-50 rounded-lg mr-3 text-purple-600">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
                    </span>
                    Planner Draft
                  </h3>
                  <div className="bg-white/50 p-5 rounded-xl border border-slate-200/60 shadow-inner">
                    <pre className="whitespace-pre-wrap font-sans text-sm text-slate-700 leading-relaxed max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
                      {result.planner_output || "No draft available."}
                    </pre>
                  </div>
                </div>

                <AgentLogs logs={result.logs} outputFile={result.output_file} />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
