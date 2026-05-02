import React from 'react';

const ValidationStatus = ({ status, errors, recommendedChanges }) => {
  if (!status) return null;
  const isValid = status === 'VALID';

  return (
    <div className="space-y-4 h-full flex flex-col">
      <div className={`p-6 rounded-2xl shadow-sm border flex-grow ${isValid ? 'bg-emerald-50/80 border-emerald-200/60' : 'bg-red-50/80 border-red-200/60'}`}>
        <div className="flex items-center mb-4">
          <span className={`p-2 rounded-xl mr-3 ${isValid ? 'bg-emerald-100/50 text-emerald-600' : 'bg-red-100/50 text-red-600'}`}>
            {isValid ? (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
            ) : (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            )}
          </span>
          <h3 className={`text-xl font-semibold font-outfit ${isValid ? 'text-emerald-800' : 'text-red-800'}`}>
            Validation Status: {status}
          </h3>
        </div>
        
        {!isValid && errors && errors.length > 0 && (
          <div className="mt-3 text-sm text-red-700 bg-red-100/30 p-4 rounded-xl border border-red-100/50">
            <p className="font-semibold mb-2">Errors Details:</p>
            <ul className="list-disc pl-5 space-y-1.5 opacity-90">
              {errors.map((err, idx) => (
                <li key={idx}>{err}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {recommendedChanges && recommendedChanges.length > 0 && (
        <div className="bg-amber-50/80 p-6 rounded-2xl shadow-sm border border-amber-200/60">
          <div className="flex items-center mb-4">
            <span className="p-2 bg-amber-100/50 rounded-xl mr-3 text-amber-600">
              <svg className="w-5 h-5 cursor-pointer" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            </span>
            <h4 className="font-semibold font-outfit text-lg text-amber-800">Recommendations</h4>
          </div>
          <ul className="list-disc pl-5 text-sm text-amber-700/90 space-y-2">
            {recommendedChanges.map((change, idx) => (
              <li key={idx} className="leading-relaxed">{change}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ValidationStatus;
