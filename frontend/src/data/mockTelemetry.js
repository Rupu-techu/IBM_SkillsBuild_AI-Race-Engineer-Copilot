export const baseTelemetryStats = {
  session: "Grand Prix Simulation",
  model: "IBM Granite Strategy Core",
  status: "Live session",
  track: "Silverstone Circuit",
  lap: 38,
  totalLaps: 52,
  position: 3,
  gapAhead: 5.8,
  gapBehind: 1.2,
  tireWear: 71,
  tireCompound: "Medium",
  tireAge: 16,
  fuel: 42,
  weather: "Dry",
  trackTemp: 41,
  airTemp: 25,
  confidence: 87,
  recommendation: "Pit Next Lap",
  summary:
    "Undercut window is opening. Tire wear remains controllable for one push lap before the pit crossover turns negative."
};

export const baseTelemetrySeries = [
  { lap: 28, pace: 96, reserve: 54, degradation: 39, energy: 68 },
  { lap: 29, pace: 95, reserve: 52, degradation: 42, energy: 70 },
  { lap: 30, pace: 94, reserve: 49, degradation: 46, energy: 71 },
  { lap: 31, pace: 92, reserve: 47, degradation: 50, energy: 74 },
  { lap: 32, pace: 91, reserve: 44, degradation: 55, energy: 76 },
  { lap: 33, pace: 89, reserve: 40, degradation: 59, energy: 79 },
  { lap: 34, pace: 88, reserve: 36, degradation: 64, energy: 81 },
  { lap: 35, pace: 87, reserve: 34, degradation: 67, energy: 82 },
  { lap: 36, pace: 86, reserve: 31, degradation: 69, energy: 84 },
  { lap: 37, pace: 84, reserve: 29, degradation: 70, energy: 86 },
  { lap: 38, pace: 82, reserve: 27, degradation: 71, energy: 88 }
];

export const baseStrategyTimeline = [
  { phase: "Current stint", detail: "Push through lap 39 with controlled front-left load" },
  { phase: "Pit window", detail: "Box lap 39 or 40 for hard compound crossover" },
  { phase: "Rejoin target", detail: "Exit ahead of P5 traffic cluster with clean air" },
  { phase: "Final stint", detail: "Stabilize deltas and protect undercut from rear pack" }
];

export const baseWeatherSignals = [
  { label: "Track temp", value: "41 C" },
  { label: "Air temp", value: "25 C" },
  { label: "Grip state", value: "Stable high energy" },
  { label: "Wind", value: "Light crosswind" }
];

export const basePitPredictions = [
  {
    id: "one-stop-undercut",
    title: "One-stop undercut",
    copy: "Box next lap for hard tires and attack the traffic gap while rivals extend.",
    meta: "Lap target 39",
    risk: "medium"
  },
  {
    id: "late-cover-stop",
    title: "Late cover stop",
    copy: "Hold for two extra laps and cover the rear threat if pace stabilizes.",
    meta: "Lap target 41",
    risk: "warning"
  },
  {
    id: "stay-out-defense",
    title: "Stay-out defense",
    copy: "Stretch current set only if yellow flag compresses the field.",
    meta: "Conditional",
    risk: "danger"
  }
];

export const baseAiReasoning = [
  "Granite sees the strongest delta on the undercut path because rear tire decay is accelerating faster than fuel burn is helping pace.",
  "The model expects a clean rejoin window ahead of midfield congestion if the stop happens before the next rival reaction cycle.",
  "Confidence stays high while weather and sector grip remain stable."
];

export const baseRecommendations = [
  "Protect front-left temperature through the final push lap.",
  "Prepare hard compound and release target for clear air exit.",
  "Use high deployment on the out lap to deny the rival crossover."
];

export const telemetryViews = [
  { id: "pace", label: "Telemetry", description: "Pace against tire reserve" },
  { id: "degradation", label: "Strategy", description: "Degradation and pit crossover" },
  { id: "weather", label: "Weather", description: "Grip energy and climate pressure" },
  { id: "ai", label: "AI Live", description: "Live AI commentary focus" }
];

export function createResetState() {
  return {
    stats: { ...baseTelemetryStats },
    series: baseTelemetrySeries.map((point) => ({ ...point })),
    timeline: baseStrategyTimeline.map((item) => ({ ...item })),
    weatherSignals: baseWeatherSignals.map((item) => ({ ...item })),
    pitPredictions: basePitPredictions.map((item) => ({ ...item })),
    aiReasoning: [...baseAiReasoning],
    recommendations: [...baseRecommendations]
  };
}

export function simulateTelemetryTick(state) {
  const currentStats = state.stats;
  const nextLap = Math.min(currentStats.lap + 1, currentStats.totalLaps);
  const lapDelta = nextLap - currentStats.lap;

  if (lapDelta <= 0) {
    return {
      ...state,
      stats: {
        ...currentStats,
        status: "Session complete",
        summary: "Final stint complete. Telemetry feed holding terminal race state."
      }
    };
  }

  const nextWear = Math.min(98, currentStats.tireWear + 3);
  const nextFuel = Math.max(8, currentStats.fuel - 3);
  const nextGapAhead = Math.max(3.4, Number((currentStats.gapAhead - 0.2).toFixed(1)));
  const nextGapBehind = Math.max(0.8, Number((currentStats.gapBehind - 0.1).toFixed(1)));
  const nextConfidence = Math.min(95, currentStats.confidence + (currentStats.tireWear < 78 ? 1 : -1));
  const nextPace = Math.max(74, 82 - (nextWear - 71) + Math.max(0, 4 - nextGapBehind));
  const nextReserve = Math.max(12, 100 - nextWear - 2);
  const nextEnergy = Math.min(96, 88 + lapDelta * 2);
  const nextDegradation = Math.min(95, nextWear + 2);

  const newPoint = {
    lap: nextLap,
    pace: nextPace,
    reserve: nextReserve,
    degradation: nextDegradation,
    energy: nextEnergy
  };

  return {
    ...state,
    stats: {
      ...currentStats,
      lap: nextLap,
      tireWear: nextWear,
      tireAge: currentStats.tireAge + 1,
      fuel: nextFuel,
      gapAhead: nextGapAhead,
      gapBehind: nextGapBehind,
      confidence: nextConfidence,
      recommendation: nextWear > 80 ? "Box This Lap" : "Pit Next Lap",
      summary:
        nextWear > 80
          ? "Tire cliff is now active. Pit immediately to protect the position from a delta collapse."
          : "Undercut pressure is building. One more high-energy lap keeps the stop window favorable."
    },
    series: [...state.series.slice(-10), newPoint],
    weatherSignals: state.weatherSignals.map((signal) =>
      signal.label === "Track temp"
        ? { ...signal, value: `${Math.min(46, currentStats.trackTemp + 1)} C` }
        : signal
    ),
    aiReasoning: [
      `Telemetry lap ${nextLap}: rear axle load is rising while fuel mass drops, preserving undercut potential.`,
      nextWear > 80
        ? "Granite now flags tire performance cliff risk as the dominant decision factor."
        : "Granite still favors a controlled final push lap before boxing.",
      `Confidence updated to ${nextConfidence}% as sector energy stays stable.`
    ],
    recommendations: [
      nextWear > 80
        ? "Commit the stop now and prioritize a clean pit lane release."
        : "Use one more deployment-rich attack lap before pitting.",
      "Bias brake migration rearward to protect front-left surface temperature.",
      "Prepare hard compound crossover and exit map."
    ]
  };
}
