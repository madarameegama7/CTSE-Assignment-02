import React from 'react';

const AgentLogs = ({ logs, outputFile }) => {
  if (!logs || logs.length === 0) return null;

  return (
    <div className="bg-gray-900 p-6 rounded-lg shadow-sm w-full font-mono">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-100 flex items-center">
          <svg className="w-5 h-5 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
          System Logs
        </h3>
        {outputFile && (
          <span className="text-xs text-gray-400 bg-gray-800 px-2 py-1 rounded border border-gray-700">
            Output: {outputFile}
          </span>
        )}
      </div>
      <div className="bg-black rounded border border-gray-800 p-4 h-48 overflow-y-auto">
        <ul className="space-y-1.5 text-xs text-gray-300">
          {logs.map((log, index) => {
            // Simple color coding based on keywords
            let textColor = "text-gray-300";
            if (log.includes("[System]")) textColor = "text-blue-400";
            if (log.toLowerCase().includes("error") || log.toLowerCase().includes("failed")) textColor = "text-red-400";
            if (log.toLowerCase().includes("valid") || log.toLowerCase().includes("success")) textColor = "text-green-400";
            
            return (
              <li key={index} className={textColor}>
                <span className="text-gray-600 mr-2">{'>'}</span>{log}
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
};

export default AgentLogs;
