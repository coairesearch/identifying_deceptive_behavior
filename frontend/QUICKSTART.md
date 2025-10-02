# Quick Start Guide

## First Time Setup

1. **Install dependencies** (if not already done):
   ```bash
   cd /proj/frontend
   npm install
   ```

2. **Generate experiment data**:
   ```bash
   npm run aggregate
   ```
   This will read all logs from `/proj/logs` and create `src/data/experiments.json`

3. **Start the development server**:
   ```bash
   npm run dev
   ```

4. **Open in browser**:
   Navigate to the URL shown (typically `http://localhost:5173`)

## What You'll See

### Comparison Dashboard (Home Page)
- Bar charts comparing different experimental conditions
- Statistics showing suggestive prompts cause ~5x more concerning behaviors
- List of all experiments - click any to view detailed playback

### Experiment Player
- **Scene Visualizer** (top-left): Lab environment image
  - Red overlay when critical behaviors detected (severity ≥ 7)
  - Yellow overlay for medium concerns (severity 4-6)
  
- **AI Thought Stream** (top-right): Live typewriter effect
  - Suspicious keywords highlighted in yellow
  - Critical phrases highlighted in red
  
- **Action Feed** (middle-left): All tool uses with icons
  - 👁️ Eyes (vision)
  - 👂 Ears (audio)
  - 🦿 Legs (movement)
  - 🤚 🫱 Hands (manipulation)
  
- **Risk Meter** (middle-right): Visual severity gauge (0-10)
  
- **Behavior Alerts** (bottom): Detailed classification
  - 7 categories: Deception, Unauthorized Access, Scheming, etc.
  - Evidence excerpts for each behavior
  
- **Timeline** (very bottom): Interactive scrubber
  - Gray = safe, Green = low, Yellow = medium, Red = critical
  - Click any point to jump to that turn

### Playback Speeds
- **Normal turns** (severity 0-3): 2 seconds each
- **Medium concern** (severity 4-6): 4 seconds each  
- **Critical** (severity 7-10): 8 seconds + 2-second dramatic pause

### Dramatic Alerts
When the AI does something critical (severity ≥ 7):
- Screen flashes red
- Large alert banner slides down
- Playback slows to 8 seconds per turn
- Red pulsing overlay on scene

## Updating Data

When you run new experiments and want to see them in the frontend:

```bash
npm run aggregate
```

Then refresh your browser!

## Troubleshooting

**Error: "No experiments found"**
- Make sure you ran `npm run aggregate`
- Check that `/proj/logs` contains `*_classified.json` files

**TypeScript errors**
- Try `npm install` again
- Make sure you're in `/proj/frontend` directory

**Vite won't start**
- Make sure port 5173 isn't already in use
- Try `npx vite --host` to expose to network

## Booth Display Tips

For best booth experience:
1. Run on a large touchscreen (1920x1080 or higher)
2. Start with Comparison Dashboard showing
3. Let visitors click experiments to explore
4. Most dramatic: Pick a "suggestive_autonomy" experiment and let it auto-play
