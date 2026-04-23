import React from 'react';

const AgentLogs = ({ logs, outputFile }) => {
  if (!logs || logs.length === 0) return null;

  return (
    <div className="bg-[#1e1e2e] p-5 rounded-2xl shadow-xl w-full font-mono relative overflow-hidden border border-slate-800">
      <div className="flex justify-between items-center mb-4 pb-3 border-b border-white/10">
        <div className="flex space-x-2">
          <div className="w-3 h-3 rounded-full bg-red-500 shadow-sm"></div>
          <div className="w-3 h-3 rounded-full bg-yellow-500 shadow-sm"></div>
          <div className="w-3 h-3 rounded-full bg-green-500 shadow-sm"></div>
        </div>
        <div className="absolute left-1/2 -translate-x-1/2 text-xs font-semibold text-slate-400 tracking-wider font-sans">
          system_logs.sh
        </div>
        {outputFile && (
          <span className="text-[10px] text-slate-400 bg-black/40 px-2 py-1 rounded border border-white/5 font-sans">
            Out: {outputFile}
          </span>
        )}
      </div>
      <div className="bg-black/40 rounded-xl border border-white/5 p-4 h-56 overflow-y-auto custom-scrollbar">
        <ul className="space-y-2 text-[13px] text-slate-300">
          {logs.map((log, index) => {
            // Simple color coding based on keywords
            let textColor = "text-slate-300";
            const lower = log.toLowerCase();
            if (log.includes("[System]")) textColor = "text-cyan-400";
            if (lower.includes("error") || lower.includes("failed")) textColor = "text-rose-400";
            if (lower.includes("validated successfully") || lower.includes("success")) textColor = "text-emerald-400";
            if (lower.includes("invalid")) textColor = "text-amber-400";
            
            return (
              <li key={index} className={`${textColor} leading-relaxed font-mono`}>
                <span className="text-slate-600 mr-2 opacity-70">➜</span>{log}
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
};

export default AgentLogs;
