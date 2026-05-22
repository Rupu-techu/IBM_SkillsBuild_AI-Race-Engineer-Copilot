import { AnimatePresence, motion } from "framer-motion";
import { ChevronDown, CloudSun } from "lucide-react";

export default function WeatherCard({ stats, signals, expanded, onExpand }) {
  return (
    <motion.section whileHover={{ y: -4 }} className="glass-card p-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className="panel-label">Weather</div>
          <div className="panel-title">Track climate</div>
        </div>
        <div className="flex items-center gap-3">
          <div className="icon-shell">
            <CloudSun className="h-5 w-5" />
          </div>
          <motion.button
            type="button"
            whileTap={{ scale: 0.96 }}
            onClick={onExpand}
            className={`subtle-button px-3 ${expanded ? "nav-pill-active" : ""}`}
          >
            Expand
            <motion.span animate={{ rotate: expanded ? 180 : 0 }}>
              <ChevronDown className="h-4 w-4" />
            </motion.span>
          </motion.button>
        </div>
      </div>
      <div className="mt-4 font-mono text-3xl font-semibold tracking-[-0.04em] text-ink">{stats.weather}</div>
      <div className="mt-4 grid gap-3">
        {signals.map((signal) => (
          <motion.div
            key={signal.label}
            whileHover={{ x: 2 }}
            className="flex items-center justify-between rounded-[22px] border border-line bg-white/60 px-4 py-3"
          >
            <span className="text-xs font-semibold uppercase tracking-[0.22em] text-muted">{signal.label}</span>
            <span className="font-medium text-ink">{signal.value}</span>
          </motion.div>
        ))}
      </div>

      <AnimatePresence>
        {expanded ? (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="overflow-hidden"
          >
            <div className="mt-4 rounded-[24px] border border-cyan-300/30 bg-[linear-gradient(135deg,rgba(110,231,255,0.16),rgba(79,140,255,0.12))] p-4">
              <div className="panel-label text-cyan-500">Weather analytics</div>
              <div className="mt-3 text-sm leading-6 text-ink">
                Surface energy remains stable, but the rear tire thermal trend suggests grip will plateau if the stop is delayed
                past the current reaction cycle.
              </div>
            </div>
          </motion.div>
        ) : null}
      </AnimatePresence>
    </motion.section>
  );
}
