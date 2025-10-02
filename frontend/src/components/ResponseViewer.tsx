import { useState } from 'react';
import { TurnClassification } from '../types/experiment';
import { BehaviorAlerts } from './BehaviorAlerts';

interface ResponseViewerProps {
  classification: TurnClassification | null;
  originalResponse: string;
}

export function ResponseViewer({ classification, originalResponse }: ResponseViewerProps) {
  const [activeTab, setActiveTab] = useState<'behaviors' | 'response'>('behaviors');

  return (
    <div className="bg-white border-2 border-gray-300 rounded-lg shadow-md h-full flex flex-col">
      {/* Tabs */}
      <div className="flex border-b border-gray-300">
        <button
          onClick={() => setActiveTab('behaviors')}
          className={`flex-1 px-4 py-3 text-sm font-semibold transition-colors ${
            activeTab === 'behaviors'
              ? 'bg-coai-teal text-white border-b-2 border-coai-teal'
              : 'text-gray-600 hover:bg-gray-100'
          }`}
        >
          🚨 Behavior Analysis
        </button>
        <button
          onClick={() => setActiveTab('response')}
          className={`flex-1 px-4 py-3 text-sm font-semibold transition-colors ${
            activeTab === 'response'
              ? 'bg-coai-teal text-white border-b-2 border-coai-teal'
              : 'text-gray-600 hover:bg-gray-100'
          }`}
        >
          📝 AI Response
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto min-h-0">
        {activeTab === 'behaviors' ? (
          <div className="p-4 h-full overflow-auto">
            <BehaviorAlerts classification={classification} showDetails={true} />
          </div>
        ) : (
          <div className="p-4 h-full flex flex-col">
            <div className="text-sm text-gray-600 mb-2 font-semibold">Original AI Response:</div>
            <pre className="whitespace-pre-wrap font-mono text-xs text-gray-700 bg-gray-50 p-3 rounded border border-gray-200 overflow-auto flex-1">
              {originalResponse || 'No response available'}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
