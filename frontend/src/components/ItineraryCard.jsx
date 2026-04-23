import React from 'react';

const ItineraryCard = ({ itinerary }) => {
  if (!itinerary || itinerary.length === 0) return null;

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
      <h3 className="text-lg font-semibold text-gray-800 mb-5 flex items-center">
        <svg className="w-5 h-5 mr-2 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
        Itinerary
      </h3>
      <div className="space-y-6">
        {itinerary.map((dayPlan, index) => (
          <div key={index} className="relative pl-5 border-l-2 border-indigo-200">
            <div className="absolute w-3 h-3 bg-indigo-500 rounded-full -left-[7px] top-1.5 ring-4 ring-white"></div>
            <h4 className="font-medium text-gray-900 mb-2">Day {dayPlan.day}</h4>
            <ul className="space-y-2">
              {dayPlan.activities && dayPlan.activities.map((activity, actIdx) => (
                <li key={actIdx} className="text-gray-600 flex items-start text-sm">
                  <span className="mr-2 text-indigo-400 mt-0.5">•</span>
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
