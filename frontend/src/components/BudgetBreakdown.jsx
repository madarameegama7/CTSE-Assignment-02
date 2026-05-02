import React from 'react';

const BudgetBreakdown = ({ breakdown, total }) => {
  if (!breakdown || Object.keys(breakdown).length === 0) return null;

  return (
    <div className="glass-card rounded-2xl p-8 relative overflow-visible">
      <div className="absolute top-0 right-0 w-32 h-32 bg-teal-500/5 rounded-full blur-2xl -mr-16 -mt-16 pointer-events-none"></div>
      <h3 className="text-2xl font-semibold font-outfit text-slate-800 mb-6 flex items-center relative z-10">
        <span className="p-2 bg-teal-50 rounded-lg mr-3 text-teal-600">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        </span>
        Budget Breakdown
      </h3>
      <div className="space-y-3.5 relative z-10">
        {Object.entries(breakdown).map(([category, amount]) => (
          <div key={category} className="flex justify-between items-center bg-gradient-to-r from-slate-50/60 to-teal-50/30 p-4 rounded-xl border border-slate-200/60 hover:border-teal-200/60 hover:shadow-md transition-all duration-200">
            <span className="capitalize text-slate-700 font-semibold text-base">{category}</span>
            <span className="font-bold font-outfit text-slate-900 text-lg">Rs. {amount.toLocaleString()}</span>
          </div>
        ))}
        <div className="pt-4 mt-6 border-t-2 border-teal-200/40 flex justify-between items-center bg-gradient-to-r from-teal-50/80 via-emerald-50/60 to-teal-50/80 p-5 rounded-xl shadow-md border border-teal-200/80">
          <span className="font-bold text-teal-900 tracking-wide text-lg">Total Cost</span>
          <span className="font-bold text-3xl font-outfit bg-gradient-to-r from-teal-700 to-emerald-600 bg-clip-text text-transparent">Rs. {total.toLocaleString()}</span>
        </div>
      </div>
    </div>
  );
};

export default BudgetBreakdown;
