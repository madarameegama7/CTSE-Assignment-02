import React from 'react';

const ItineraryCard = ({ itinerary }) => {
  if (!itinerary || itinerary.length === 0) return null;

  return (
    <div className="glass-card rounded-2xl p-6 relative overflow-hidden group">
      <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/5 rounded-full blur-2xl -mr-10 -mt-10"></div>
      <h3 className="text-xl font-semibold font-outfit text-slate-800 mb-6 flex items-center relative z-10">
        <span className="p-2 bg-indigo-50 rounded-lg mr-3 text-indigo-600">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
        </span>
        Your Itinerary
      </h3>
      <div className="space-y-6 relative z-10">
        {itinerary.map((dayPlan, index) => (
          <div key={index} className="relative pl-6 border-l-2 border-indigo-100 hover:border-indigo-400 transition-colors duration-300">
            <div className="absolute w-4 h-4 bg-indigo-500 rounded-full -left-[9px] top-1 ring-4 ring-white shadow-sm"></div>
            <h4 className="font-semibold text-slate-900 mb-3 font-outfit text-lg tracking-tight">Day {dayPlan.day}</h4>
            <ul className="space-y-2.5">
              {dayPlan.activities && dayPlan.activities.map((activity, actIdx) => (
                <li key={actIdx} className="text-slate-600 flex items-start text-sm leading-relaxed bg-white/40 p-2.5 rounded-lg border border-slate-100/50 hover:bg-white/70 hover:shadow-sm transition-all">
                  <span className="mr-2 text-indigo-400 mt-0.5 shrink-0 flex items-center justify-center w-5 h-5 bg-indigo-50 rounded-full">
                    <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full"></span>
                  </span>
                  <span>{activity}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ItineraryCard;
