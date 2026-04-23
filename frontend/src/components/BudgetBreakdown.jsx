import React from 'react';

const BudgetBreakdown = ({ breakdown, total }) => {
  if (!breakdown || Object.keys(breakdown).length === 0) return null;

  return (
    <div className="glass-card rounded-2xl p-6 relative overflow-hidden">
      <div className="absolute top-0 right-0 w-32 h-32 bg-teal-500/5 rounded-full blur-2xl -mr-10 -mt-10"></div>
      <h3 className="text-xl font-semibold font-outfit text-slate-800 mb-5 flex items-center relative z-10">
        <span className="p-2 bg-teal-50 rounded-lg mr-3 text-teal-600">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        </span>
        Budget Breakdown
      </h3>
      <div className="space-y-3 relative z-10">
        {Object.entries(breakdown).map(([category, amount]) => (
          <div key={category} className="flex justify-between items-center text-sm bg-slate-50/50 p-2.5 rounded-lg border border-slate-100">
            <span className="capitalize text-slate-600 font-medium">{category}</span>
            <span className="font-semibold font-outfit text-slate-900">${amount}</span>
          </div>
        ))}
        <div className="pt-4 border-t border-slate-200/60 mt-5 flex justify-between items-center bg-gradient-to-r from-teal-50 to-emerald-50 p-4 rounded-xl shadow-sm border border-teal-100/50">
          <span className="font-semibold text-teal-900 tracking-wide">Total Cost</span>
          <span className="font-bold text-2xl font-outfit text-teal-700">${total}</span>
        </div>
      </div>
    </div>
  );
};

export default BudgetBreakdown;
