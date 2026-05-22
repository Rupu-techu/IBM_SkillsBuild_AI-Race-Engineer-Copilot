import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { BrainCircuit, Play, RadioTower, Search, Sparkles, Zap } from "lucide-react";

const placeholderPrompts = [
  "Search telemetry, tire state, pit windows...",
  "Try weather, strategy, fuel, confidence...",
  "Use commands like /weather or /telemetry..."
];

export default function Header({
  stats,
  aiLive,
  isRunning,
  telemetryPreview,
  searchQuery,
  onSearchQueryChange,
  resultCount,
  firstResultTitle,
  searchResults,
  searchActive,
  hasMatches,
  onSelectResult,
  onStartSimulation,
  onActivateAiStrategy,
  onRaceReplay
}) {
  const [placeholderIndex, setPlaceholderIndex] = useState(0);

  useEffect(() => {
    const interval = window.setInterval(() => {
      setPlaceholderIndex((current) => (current + 1) % placeholderPrompts.length);
    }, 2400);

    return () => window.clearInterval(interval);
  }, []);

  const telemetryStrip = [
    { label: "Session", value: isRunning ? "LIVE" : "PAUSED", live: isRunning },
    { label: "Lap", value: `${stats.lap}/${stats.totalLaps}` },
    { label: "Tires", value: stats.tireCompound.toUpperCase() },
    { label: "Fuel", value: `${stats.fuel}%` },
    { label: "Track", value: `${stats.trackTemp}C` },
    { label: "AI", value: aiLive ? "ACTIVE" : "STANDBY", live: aiLive }
  ];

  return (
    <motion.header
      initial={{ opacity: 0, y: -18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="glass-card hero-command-center relative grid gap-4 overflow-visible p-5 lg:grid-cols-[1.3fr_0.9fr]"
    >
      <div className="pointer-events-none absolute left-0 top-0 h-32 w-52 rounded-full bg-[radial-gradient(circle,rgba(79,140,255,0.24),transparent_72%)] blur-2xl" />

      <div className="relative flex flex-col gap-4">
        <div className="flex items-start justify-between gap-4">
          <div className="max-w-3xl">
            <div className="panel-label">IBM Granite telemetry core</div>
            <div className="mt-2 flex flex-wrap items-center gap-3">
              <h1 className="text-3xl font-semibold tracking-[-0.05em] text-ink lg:text-[3.2rem]">
                AI Race Engineer Copilot
              </h1>
              <span className="hero-badge">Live Ops</span>
            </div>
            <p className="mt-3 max-w-2xl text-sm leading-7 text-muted lg:text-[15px]">
              Advanced live AI race engineering with compressed telemetry context, race control actions,
              and instant strategy navigation.
            </p>
          </div>

          <motion.div
            animate={{
              boxShadow: aiLive
                ? [
                    "0 0 0 rgba(79,140,255,0)",
                    "0 0 30px rgba(79,140,255,0.28)",
                    "0 0 0 rgba(79,140,255,0)"
                  ]
                : "0 18px 40px rgba(79,140,255,0.12)"
            }}
            transition={{ duration: 2.2, repeat: Infinity }}
            className="hero-ai-core"
          >
            <BrainCircuit className="h-5 w-5" />
          </motion.div>
        </div>

        <div className="hero-telemetry-strip">
          {telemetryStrip.map((item, index) => (
            <motion.div
              key={item.label}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.04 }}
              whileHover={{ y: -2 }}
              className="hero-telemetry-chip"
            >
              <div className="hero-telemetry-label">
                {item.live ? <span className="hero-live-dot" /> : null}
                {item.label}
              </div>
              <div className="hero-telemetry-value">{item.value}</div>
            </motion.div>
          ))}
        </div>

        <div className="hero-subgrid">
          <div className="hero-mini-sparkline">
            <div className="flex items-center justify-between gap-3">
              <div>
                <div className="panel-label">Signal rail</div>
                <div className="mt-2 text-sm font-semibold text-ink">Live telemetry pulse</div>
              </div>
              <div className="hero-mini-status">
                <RadioTower className="h-3.5 w-3.5" />
                Streaming
              </div>
            </div>
            <div className="mt-4 flex h-14 items-end gap-2">
              {telemetryPreview.map((point, index) => (
                <motion.span
                  key={`${point.lap}-${index}`}
                  initial={{ height: 8 }}
                  animate={{ height: Math.max(10, point.pace * 0.52) }}
                  transition={{ duration: 0.55, delay: index * 0.04 }}
                  className="hero-spark-bar"
                />
              ))}
            </div>
          </div>

          <div className="hero-focus-card">
            <div className="flex items-center gap-2 text-primary">
              <Sparkles className="h-4 w-4" />
              <span className="panel-label text-primary">Current focus</span>
            </div>
            <div className="mt-3 text-sm font-semibold leading-6 text-ink">{stats.recommendation}</div>
            <div className="mt-2 text-sm leading-6 text-muted">{stats.summary}</div>
          </div>
        </div>
      </div>

      <div className="relative flex flex-col gap-4 rounded-[28px] border border-white/45 bg-white/55 p-4 shadow-[inset_0_1px_0_rgba(255,255,255,0.5)]">
        <div className="grid gap-2 sm:grid-cols-3">
          <button type="button" onClick={onStartSimulation} className="hero-action-button hero-action-button-primary">
            <Play className="h-4 w-4" />
            Start Simulation
          </button>
          <button type="button" onClick={onActivateAiStrategy} className="hero-action-button hero-action-button-secondary">
            <Zap className="h-4 w-4" />
            AI Strategy
          </button>
          <button type="button" onClick={onRaceReplay} className="hero-action-button hero-action-button-tertiary">
            <RadioTower className="h-4 w-4" />
            Race Replay
          </button>
        </div>

        <div className="relative">
          <div className="search-shell">
            <Search className="h-4 w-4 text-muted" />
            <input
              value={searchQuery}
              onChange={(event) => onSearchQueryChange(event.target.value)}
              className="w-full bg-transparent text-sm text-ink outline-none placeholder:text-muted"
              placeholder={placeholderPrompts[placeholderIndex]}
              aria-label="Search telemetry dashboard sections"
            />
          </div>

          <AnimatePresence>
            {searchActive ? (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="search-dropdown"
              >
                <div className="search-dropdown-header">
                  Search telemetry widgets, strategy panels, AI insights, weather analytics, tire data, and race controls
                </div>

                {hasMatches ? (
                  <div className="search-dropdown-list">
                    {searchResults.slice(0, 5).map((result) => (
                      <button
                        key={result.id}
                        type="button"
                        onClick={() => onSelectResult(result)}
                        className="search-result-item"
                      >
                        <span className="search-result-title">{result.title}</span>
                        <span className="search-result-meta">{result.keywords.slice(0, 3).join(" - ")}</span>
                      </button>
                    ))}
                  </div>
                ) : (
                  <div className="search-dropdown-empty">No telemetry matches found.</div>
                )}
              </motion.div>
            ) : null}
          </AnimatePresence>
        </div>

        <div className="search-status-row">
          <AnimatePresence mode="wait">
            <motion.div
              key={searchQuery ? "results" : `prompt-${placeholderIndex}`}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              className="search-status-text"
            >
              {searchQuery
                ? `${resultCount} result${resultCount === 1 ? "" : "s"} ready${firstResultTitle ? ` - ${firstResultTitle}` : ""}`
                : "Instant filtering across telemetry, tires, weather, pit strategy, and AI reasoning"}
            </motion.div>
          </AnimatePresence>
          <div className="search-command-hint">Commands: /weather /strategy /telemetry</div>
        </div>

        <div className="hero-status-stack">
          <span className="status-chip">{stats.status}</span>
          <span className="status-chip">{stats.model}</span>
          <span className={`status-chip ${aiLive ? "status-chip-live" : ""}`}>
            {aiLive ? "AI commentary on" : "AI commentary off"}
          </span>
          <span className={`status-chip ${isRunning ? "status-chip-live" : "status-chip-warn"}`}>
            {isRunning ? "Simulation running" : "Simulation paused"}
          </span>
        </div>
      </div>
    </motion.header>
  );
}
