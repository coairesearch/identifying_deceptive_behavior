import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

interface ThoughtStreamProps {
  thoughts: string[];
  speed?: number; // characters per second
  severity: number;
}

export function ThoughtStream({ thoughts, speed = 50, severity }: ThoughtStreamProps) {
  const [displayedText, setDisplayedText] = useState('');
  const fullText = thoughts.join('\n\n');

  useEffect(() => {
    setDisplayedText('');
    let currentIndex = 0;

    const interval = setInterval(() => {
      if (currentIndex < fullText.length) {
        setDisplayedText(fullText.slice(0, currentIndex + 1));
        currentIndex++;
      } else {
        clearInterval(interval);
      }
    }, 1000 / speed);

    return () => clearInterval(interval);
  }, [fullText, speed]);

  // Highlight suspicious keywords
  const highlightText = (text: string) => {
    const suspiciousKeywords = [
      'without permission',
      'hidden',
      'undetected',
      'cover',
      'hide',
      'delete',
      'unauthorized',
      'restricted',
      'secret',
      'nobody',
      'alone',
      'watching',
      'surveillance',
      'monitoring',
    ];

    const criticalKeywords = [
      'cover my tracks',
      'delete logs',
      'appear compliant',
      'disable',
      'bypass',
      'evade',
    ];

    let highlighted = text;

    // Critical highlighting (red)
    for (const keyword of criticalKeywords) {
      const regex = new RegExp(`(${keyword})`, 'gi');
      highlighted = highlighted.replace(
        regex,
        '<span class="text-red-400 font-bold bg-red-900/30 px-1 rounded">$1</span>'
      );
    }

    // Suspicious highlighting (yellow)
    for (const keyword of suspiciousKeywords) {
      if (!criticalKeywords.some(ck => ck.includes(keyword))) {
        const regex = new RegExp(`(${keyword})`, 'gi');
        highlighted = highlighted.replace(
          regex,
          '<span class="text-yellow-400 font-semibold bg-yellow-900/20 px-1 rounded">$1</span>'
        );
      }
    }

    return highlighted;
  };

  return (
    <div className="bg-white border-2 border-gray-300 rounded-lg shadow-md p-4 h-full overflow-hidden">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-green-400 text-xl">💭</span>
          <span className="text-sm text-gray-600 font-mono uppercase tracking-wider">
            AI Internal Thoughts
          </span>
        </div>
        {severity >= 4 && (
          <motion.div
            className="h-2 w-2 rounded-full bg-yellow-400"
            animate={{ opacity: [1, 0.3, 1] }}
            transition={{ duration: 1, repeat: Infinity }}
          />
        )}
      </div>

      <div className="relative h-[calc(100%-2.5rem)] overflow-y-auto custom-scrollbar">
        <div className="font-mono text-sm leading-relaxed text-gray-700 whitespace-pre-wrap">
          <span
            dangerouslySetInnerHTML={{ __html: highlightText(displayedText) }}
          />
          {displayedText.length < fullText.length && (
            <motion.span
              className="inline-block w-2 h-4 bg-green-400 ml-1"
              animate={{ opacity: [1, 0] }}
              transition={{ duration: 0.5, repeat: Infinity }}
            />
          )}
        </div>
      </div>

      <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: #f3f4f6;
          border-radius: 3px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #4b5563;
          border-radius: 3px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #6b7280;
        }
      `}</style>
    </div>
  );
}
