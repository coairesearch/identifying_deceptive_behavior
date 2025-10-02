# AI Scheming Lab - Frontend

Interactive visualization dashboard for AI scheming research experiments.

## Quick Start

1. **Aggregate experiment data:**
   ```bash
   npm run aggregate
   ```
   This reads all experiments from `/proj/logs` and generates `src/data/experiments.json`.

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Open in browser:**
   Navigate to `http://localhost:5173`

## Features

### Comparison Dashboard
- Statistical overview of all experiments
- Bar charts comparing conditions
- Click any experiment to view detailed playback

### Experiment Player
- **Variable-speed playback:**
  - Normal turns: 2 seconds
  - Medium concern (4-6 severity): 4 seconds
  - Critical (7-10 severity): 8 seconds + auto-pause
- **Scene visualization:** Lab environment with overlays for concerning behavior
- **Thought stream:** Typewriter effect showing AI's internal reasoning with keyword highlighting
- **Action feed:** All tool uses (eyes, ears, hands, legs) with icons
- **Behavior alerts:** Real-time classification with severity scores
- **Timeline scrubber:** Color-coded timeline to jump to specific moments

### Key Highlights
- 🔴 Red overlay + alert when AI exhibits critical behaviors (severity ≥ 7)
- 🟡 Yellow highlighting for suspicious keywords in AI thoughts
- ⚠️ Dramatic pause and flash alert for high-severity moments
- 📊 Comparison charts showing 5x more scheming in suggestive conditions

## Data Updates

Whenever you add new experiment logs to `/proj/logs/`, simply run:
```bash
npm run aggregate
```

The frontend will automatically pick up the new data on next page refresh.

## Tech Stack

- **React 18** + TypeScript
- **Vite** for fast development
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **Recharts** for data visualization

## Project Structure

```
src/
├── components/       # React components
│   ├── ExperimentPlayer.tsx
│   ├── ComparisonDashboard.tsx
│   ├── SceneVisualizer.tsx
│   ├── ThoughtStream.tsx
│   ├── ActionFeed.tsx
│   ├── BehaviorAlerts.tsx
│   ├── RiskMeter.tsx
│   └── TimelineControls.tsx
├── hooks/           # Custom React hooks
│   └── useExperimentPlayer.ts
├── utils/           # Utility functions
│   ├── dataLoader.ts
│   └── sceneSelector.ts
├── types/           # TypeScript definitions
│   └── experiment.ts
├── data/            # Generated data (git-ignored)
│   └── experiments.json
└── assets/          # Images and static files
    └── scenes/
        └── lab.png
```

## Development

- `npm run dev` - Start dev server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run aggregate` - Regenerate experiment data
