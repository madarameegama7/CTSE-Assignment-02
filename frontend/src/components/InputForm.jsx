import React, { useState } from 'react';

const InputForm = ({ onSubmit, isLoading }) => {
  const [destination, setDestination] = useState('');
  const [days, setDays] = useState('');
  const [travelers, setTravelers] = useState('1');
  const [budget, setBudget] = useState('');
  const [preferences, setPreferences] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    if (!destination.trim()) {
      setError('Destination is required.');
      return;
    }
    if (!days || Number(days) <= 0) {
      setError('Days must be greater than 0.');
      return;
    }
    if (!travelers || Number(travelers) <= 0) {
      setError('Travelers must be greater than 0.');
      return;
    }
    if (!budget || Number(budget) <= 0) {
      setError('Budget must be greater than 0.');
      return;
    }

    const prefsArray = preferences
      .split(',')
      .map((p) => p.trim())
      .filter((p) => p.length > 0);

    onSubmit({
      destination: destination.trim(),
      days: Number(days),
      travelers: Number(travelers),
      budget: Number(budget),
      preferences: prefsArray,
    });
  };

  return (
    <div className="glass-card rounded-2xl p-8 h-full flex flex-col relative overflow-hidden">
      <div className="absolute top-0 right-0 -mr-8 -mt-8 w-32 h-32 bg-indigo-500/10 rounded-full blur-2xl"></div>
      <h2 className="text-2xl font-semibold mb-6 flex items-center font-outfit text-slate-800 tracking-tight">
        <span className="p-2 bg-indigo-50 rounded-xl mr-3 text-indigo-600 shadow-sm border border-indigo-100">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        </span>
        Plan Your Trip
      </h2>
      {error && (
        <div className="mb-4 p-3 bg-red-50 text-red-700 text-sm rounded-md border border-red-200">
          {error}
        </div>
      )}
      <form onSubmit={handleSubmit} className="space-y-5 flex-grow flex flex-col relative z-10">
        <div className="group">
          <label className="block text-sm font-semibold text-slate-700 mb-1.5 transition-colors group-focus-within:text-indigo-600">Destination</label>
          <input
            type="text"
            className="w-full px-4 py-3 bg-white/60 border border-slate-200 rounded-xl focus:ring-4 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all shadow-sm placeholder:text-slate-400 outline-none"
            placeholder="e.g., Ella, Sri Lanka"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            disabled={isLoading}
          />
        </div>
        <div className="grid grid-cols-3 gap-5">
          <div className="group">
            <label className="block text-sm font-semibold text-slate-700 mb-1.5 transition-colors group-focus-within:text-indigo-600">Days</label>
            <input
              type="number"
              className="w-full px-4 py-3 bg-white/60 border border-slate-200 rounded-xl focus:ring-4 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all shadow-sm placeholder:text-slate-400 outline-none"
              placeholder="e.g., 3"
              value={days}
              onChange={(e) => setDays(e.target.value)}
              disabled={isLoading}
            />
          </div>
          <div className="group">
            <label className="block text-sm font-semibold text-slate-700 mb-1.5 transition-colors group-focus-within:text-indigo-600">Travelers</label>
            <input
              type="number"
              className="w-full px-4 py-3 bg-white/60 border border-slate-200 rounded-xl focus:ring-4 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all shadow-sm placeholder:text-slate-400 outline-none"
              placeholder="e.g., 2"
              value={travelers}
              onChange={(e) => setTravelers(e.target.value)}
              disabled={isLoading}
            />
          </div>
          <div className="group">
            <label className="block text-sm font-semibold text-slate-700 mb-1.5 transition-colors group-focus-within:text-indigo-600">Budget (Rs.)</label>
            <input
              type="number"
              className="w-full px-4 py-3 bg-white/60 border border-slate-200 rounded-xl focus:ring-4 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all shadow-sm placeholder:text-slate-400 outline-none"
              placeholder="e.g., 500"
              value={budget}
              onChange={(e) => setBudget(e.target.value)}
              disabled={isLoading}
            />
          </div>
        </div>
        <div className="group">
          <label className="block text-sm font-semibold text-slate-700 mb-1.5 transition-colors group-focus-within:text-indigo-600">Preferences <span className="font-normal text-slate-400">(comma-separated)</span></label>
          <input
            type="text"
            className="w-full px-4 py-3 bg-white/60 border border-slate-200 rounded-xl focus:ring-4 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all shadow-sm placeholder:text-slate-400 outline-none"
            placeholder="e.g., nature, relax, historical"
            value={preferences}
            onChange={(e) => setPreferences(e.target.value)}
            disabled={isLoading}
          />
        </div>
        <div className="pt-4 mt-auto">
          <button
            type="submit"
            disabled={isLoading}
            className={`w-full py-3.5 px-4 rounded-xl shadow-lg shadow-indigo-200 text-white font-semibold text-lg tracking-wide ${
              isLoading ? 'bg-indigo-300 cursor-not-allowed opacity-70' : 'bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 hover:-translate-y-0.5 hover:shadow-indigo-300 transform'
            } transition-all duration-300 focus:outline-none focus:ring-4 focus:ring-indigo-500/40`}
          >
            {isLoading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                Planning...
              </span>
            ) : 'Generate My Dream Trip'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default InputForm;
