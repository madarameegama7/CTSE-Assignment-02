import React from 'react';

const BudgetBreakdown = ({ breakdown, total }) => {
  if (!breakdown) return null;

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
      <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
        <svg className="w-5 h-5 mr-2 text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        Budget Breakdown
      </h3>
      <div className="space-y-3">
        {Object.entries(breakdown).map(([category, amount]) => (
          <div key={category} className="flex justify-between items-center text-sm text-gray-600">
            <span className="capitalize">{category}</span>
            <span className="font-medium text-gray-900">${amount}</span>
          </div>
        ))}
        <div className="pt-3 border-t border-gray-200 mt-4 flex justify-between items-center bg-teal-50 p-3 rounded-md">
          <span className="font-semibold text-teal-900">Total Cost</span>
          <span className="font-bold text-teal-700">${total}</span>
        </div>
      </div>
    </div>
  );
};

export default BudgetBreakdown;
