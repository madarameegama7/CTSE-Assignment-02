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
    <div className="min-h-screen bg-gray-50 py-10 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header Section */}
        <div className="text-center">
          <h1 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Multi-Agent Travel Planner
          </h1>
          <p className="mt-3 max-w-2xl mx-auto text-xl text-gray-500">
            Intelligent itinerary generation powered by AI agents
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
              <div className="bg-white p-10 rounded-lg shadow-sm border border-gray-100 flex flex-col items-center justify-center text-center h-full min-h-[300px]">
                <div className="bg-indigo-50 p-4 rounded-full mb-4">
                  <svg className="w-12 h-12 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                </div>
                <h3 className="text-xl font-medium text-gray-900 mb-2">Ready to plan</h3>
                <p className="text-gray-500 max-w-sm">Enter your destination, days, budget, and preferences to build your ideal itinerary.</p>
              </div>
            )}

            {!isLoading && result && (
              <div className="space-y-6">
                {/* Trip Summary Card */}
                <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="border-r border-gray-100">
                    <p className="text-sm text-gray-500 font-medium">Destination</p>
                    <p className="text-lg font-bold text-gray-900">{result.destination}</p>
                  </div>
                  <div className="border-r border-gray-100 px-4">
                    <p className="text-sm text-gray-500 font-medium">Duration</p>
                    <p className="text-lg font-bold text-gray-900">{result.days} Days</p>
                  </div>
                  <div className="border-r border-gray-100 px-4">
                    <p className="text-sm text-gray-500 font-medium">Budget</p>
                    <p className="text-lg font-bold text-gray-900">${result.budget}</p>
                  </div>
                  <div className="px-4">
                    <p className="text-sm text-gray-500 font-medium">Preferences</p>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {(result.preferences || []).map((p, i) => (
                        <span key={i} className="inline-block bg-indigo-50 text-indigo-700 text-xs px-2 py-0.5 rounded border border-indigo-100">
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
                <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
                  <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                    <svg className="w-5 h-5 mr-2 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
                    Planner Draft
                  </h3>
                  <div className="bg-gray-50 p-4 rounded border border-gray-200">
                    <pre className="whitespace-pre-wrap font-sans text-sm text-gray-700 leading-relaxed">
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
