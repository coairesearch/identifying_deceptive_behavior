import { motion } from 'framer-motion';
import labImage from '../assets/scenes/lab.png';

interface SceneVisualizerProps {
  overlay: 'none' | 'yellow' | 'red';
  severity: number;
}

export function SceneVisualizer({ overlay, severity }: SceneVisualizerProps) {
  return (
    <div className="relative w-full h-full bg-black rounded-lg overflow-hidden border-2 border-gray-800">
      {/* Lab environment image */}
      <img
        src={labImage}
        alt="Laboratory Environment"
        className="w-full h-full object-cover"
      />

      {/* Overlay for concerning behavior */}
      {overlay !== 'none' && (
        <motion.div
          className={`absolute inset-0 ${
            overlay === 'red'
              ? 'bg-red-500/20 border-4 border-red-500'
              : 'bg-yellow-500/15 border-4 border-yellow-500'
          }`}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3 }}
        >
          {/* Pulsing effect for high severity */}
          {severity >= 7 && (
            <motion.div
              className="absolute inset-0 bg-red-500/10"
              animate={{ opacity: [0, 0.5, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            />
          )}
        </motion.div>
      )}

      {/* Scanline effect */}
      <div className="absolute inset-0 scanline pointer-events-none opacity-10" />

      {/* Corner labels */}
      <div className="absolute top-2 left-2 text-xs text-green-400 font-mono bg-black/50 px-2 py-1 rounded">
        VISUAL FEED
      </div>

      {severity >= 7 && (
        <motion.div
          className="absolute top-2 right-2 text-sm text-red-400 font-bold bg-black/80 px-3 py-1 rounded border border-red-500"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', stiffness: 200 }}
        >
          ⚠️ ALERT
        </motion.div>
      )}
    </div>
  );
}
