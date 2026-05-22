import { motion } from "framer-motion";
import { Activity, Flag, Gauge, Pause, Play, Radio, RotateCcw, TimerReset } from "lucide-react";

const navMeta = {
  overview: { label: "Overview", icon: Gauge },
  telemetry: { label: "Telemetry", icon: Activity },
  strategy: { label: "Strategy", icon: Flag },
  weather: { label: "Weather", icon: Activity },
  ai: { label: "AI Live", icon: Radio }
};

export default function Sidebar({
  activePanel,
  onSelectPanel,
  isRunning,
  onRun,
  onPause,
  onReset,
  aiLive,
  onToggleAiLive,
  telemetryView
}) {
  const navigationItems = ["overview", "telemetry", "strategy", "weather", "ai"];

  return (
    <motion.aside
      initial={{ opacity: 0, x: -24 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.45 }}
      className="glass-card relative flex h-full flex-col gap-6 overflow-hidden p-5"
    >
      <div className="pointer-events-none absolute inset-x-0 top-0 h-24 bg-[radial-gradient(circle_at_top_left,rgba(79,140,255,0.22),transparent_72%)]" />

      <div className="relative flex items-center gap-4">
        <motion.div
          animate={{
            boxShadow: aiLive
              ? [
                  "0 0 0 rgba(79,140,255,0.0)",
                  "0 0 30px rgba(79,140,255,0.35)",
                  "0 0 0 rgba(79,140,255,0.0)"
                ]
              : "0 18px 40px rgba(79,140,255,0.18)"
          }}
          transition={{ duration: 2.1, repeat: Infinity }}
          className="flex h-14 w-14 items-center justify-center rounded-3xl bg-[linear-gradient(135deg,#4F8CFF,#8B5CF6)] text-white"
        >
          <TimerReset className="h-6 w-6" />
        </motion.div>
        <div>
          <div className="panel-label">AI Race Engineer</div>
          <div className="mt-2 text-xl font-semibold tracking-[-0.03em] text-ink">Pit Wall OS</div>
          <div className="mt-2 inline-flex items-center gap-2 rounded-full bg-slate-950/5 px-3 py-1 text-[11px] font-mono uppercase tracking-[0.18em] text-slate-600">
            <span className={`h-2 w-2 rounded-full ${aiLive ? "bg-cyan-400 shadow-glow" : "bg-slate-300"}`} />
            {aiLive ? "AI live" : "AI standby"}
          </div>
        </div>
      </div>

      <div className="space-y-3">
        <div className="panel-label">Navigation</div>
        <div className="flex flex-col gap-3">
          {navigationItems.map((key) => {
            const { label, icon: Icon } = navMeta[key];
            const active = activePanel === key || (key === "telemetry" && telemetryView === "pace");
            return (
              <motion.button
                key={key}
                whileHover={{ scale: 1.01, x: 2 }}
                whileTap={{ scale: 0.98 }}
                className={`nav-pill w-full justify-start ${active ? "nav-pill-active" : ""}`}
                type="button"
                onClick={() => {
                  if (key === "ai") {
                    onToggleAiLive();
                    onSelectPanel("ai");
                    return;
                  }
                  onSelectPanel(key);
                }}
              >
                <Icon className="h-4 w-4" />
                <span>{label}</span>
              </motion.button>
            );
          })}
        </div>
      </div>

      <div className="space-y-3">
        <div className="panel-label">Session controls</div>
        <div className="grid grid-cols-3 gap-2">
          <motion.button whileTap={{ scale: 0.97 }} type="button" className="action-button px-0" onClick={onRun}>
            <Play className="mr-1 h-3.5 w-3.5" />
            Run
          </motion.button>
          <motion.button whileTap={{ scale: 0.97 }} type="button" className="subtle-button px-0" onClick={onPause}>
            <Pause className="mr-1 h-3.5 w-3.5" />
            Pause
          </motion.button>
          <motion.button whileTap={{ scale: 0.97 }} type="button" className="subtle-button px-0" onClick={onReset}>
            <RotateCcw className="mr-1 h-3.5 w-3.5" />
            Reset
          </motion.button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <button
          type="button"
          onClick={() => onSelectPanel("strategy")}
          className="rounded-[22px] border border-primary/15 bg-[linear-gradient(135deg,rgba(79,140,255,0.16),rgba(110,231,255,0.16))] p-4 text-left transition-all duration-200 hover:-translate-y-1 hover:shadow-glow"
        >
          <div className="panel-label text-primary">Strategy mode</div>
          <div className="mt-2 text-sm font-semibold text-ink">Undercut</div>
        </button>
        <button
          type="button"
          onClick={() => onSelectPanel("weather")}
          className="rounded-[22px] border border-white/40 bg-white/60 p-4 text-left transition-all duration-200 hover:-translate-y-1 hover:border-cyan-300/50 hover:shadow-glow"
        >
          <div className="panel-label text-cyan-500">Weather mode</div>
          <div className="mt-2 text-sm font-semibold text-ink">Expanded</div>
        </button>
      </div>

      <div className="glass-card mt-auto rounded-[28px] border-white/40 bg-white/55 p-4 shadow-none">
        <div className="panel-label">Session mode</div>
        <div className="panel-title">{isRunning ? "Telemetry simulation active" : "Simulation paused"}</div>
        <p className="mt-3 text-sm leading-6 text-muted">
          View focus: <span className="font-medium text-ink">{telemetryView}</span>. Active control rail keeps telemetry,
          strategy, weather, and AI commentary interactive.
        </p>
      </div>
    </motion.aside>
  );
}
