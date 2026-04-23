import React from 'react';

const ValidationStatus = ({ status, errors, recommendedChanges }) => {
  const isValid = status === 'VALID';

  return (
    <div className="space-y-4 h-full flex flex-col">
      <div className={`p-5 rounded-lg shadow-sm border flex-grow ${isValid ? 'bg-emerald-50 border-emerald-200' : 'bg-red-50 border-red-200'}`}>
        <div className="flex items-center mb-3">
          {isValid ? (
            <svg className="w-6 h-6 text-emerald-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
          ) : (
            <svg className="w-6 h-6 text-red-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          )}
          <h3 className={`text-lg font-semibold ${isValid ? 'text-emerald-800' : 'text-red-800'}`}>
            Validation Status: {status}
          </h3>
        </div>
        
        {!isValid && errors && errors.length > 0 && (
          <div className="mt-2 text-sm text-red-700 bg-red-100/50 p-3 rounded">
            <p className="font-semibold mb-1">Errors Details:</p>
            <ul className="list-disc pl-4 space-y-1">
              {errors.map((err, idx) => (
                <li key={idx}>{err}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {recommendedChanges && recommendedChanges.length > 0 && (
        <div className="bg-amber-50 p-5 rounded-lg shadow-sm border border-amber-200">
          <div className="flex items-center mb-3">
            <svg className="w-5 h-5 text-amber-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            <h4 className="font-semibold text-amber-800">Recommendations</h4>
          </div>
          <ul className="list-disc pl-5 text-sm text-amber-700 space-y-1.5">
            {recommendedChanges.map((change, idx) => (
              <li key={idx}>{change}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ValidationStatus;
