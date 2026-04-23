import React, { useState } from 'react';

const InputForm = ({ onSubmit, isLoading }) => {
  const [destination, setDestination] = useState('');
  const [days, setDays] = useState('');
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
      budget: Number(budget),
      preferences: prefsArray,
    });
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 h-full">
      <h2 className="text-xl font-semibold mb-4 text-gray-800 flex items-center">
        <svg className="w-5 h-5 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        Plan Your Trip
      </h2>
      {error && (
        <div className="mb-4 p-3 bg-red-50 text-red-700 text-sm rounded-md border border-red-200">
          {error}
        </div>
      )}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Destination</label>
          <input
            type="text"
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="e.g., Ella"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            disabled={isLoading}
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Days</label>
            <input
              type="number"
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="e.g., 2"
              value={days}
              onChange={(e) => setDays(e.target.value)}
              disabled={isLoading}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Budget ($)</label>
            <input
              type="number"
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="e.g., 400"
              value={budget}
              onChange={(e) => setBudget(e.target.value)}
              disabled={isLoading}
            />
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Preferences (comma-separated)</label>
          <input
            type="text"
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="e.g., nature, relax"
            value={preferences}
            onChange={(e) => setPreferences(e.target.value)}
            disabled={isLoading}
          />
        </div>
        <div className="pt-2">
          <button
            type="submit"
            disabled={isLoading}
            className={`w-full py-2.5 px-4 border border-transparent rounded-md shadow-sm text-white font-medium ${
              isLoading ? 'bg-indigo-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700'
            } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors`}
          >
            {isLoading ? 'Planning...' : 'Plan My Trip'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default InputForm;
