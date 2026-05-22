import { motion } from "framer-motion";
import { ArrowRight, FlagTriangleRight, Zap } from "lucide-react";

export default function StrategyPanel({ stats, timeline, activePanel, selectedPrediction }) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45, delay: 0.08 }}
      className="glass-card strategy-hero-card p-6"
    >
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div className="panel-label">Hero telemetry card</div>
          <div className="mt-3 text-3xl font-semibold tracking-[-0.05em] text-ink md:text-4xl">
            {stats.recommendation}
          </div>
          <p className="mt-4 max-w-2xl text-sm leading-7 text-muted lg:text-base">{stats.summary}</p>
        </div>

        <motion.div
          whileHover={{ y: -2 }}
          className="rounded-[30px] border border-primary/15 bg-[linear-gradient(135deg,rgba(79,140,255,0.16),rgba(110,231,255,0.14),rgba(139,92,246,0.14))] px-5 py-4 shadow-[0_18px_40px_rgba(79,140,255,0.14)]"
        >
          <div className="panel-label text-primary">Track status</div>
          <div className="mt-3 font-mono text-2xl font-semibold text-ink">P{stats.position}</div>
          <div className="mt-1 text-sm text-muted">Gap behind {stats.gapBehind}s</div>
        </motion.div>
      </div>

      <div className="mt-5 flex flex-wrap gap-2">
        <span className={`status-chip ${activePanel === "strategy" ? "status-chip-live" : ""}`}>Strategy focused</span>
        <span className="status-chip">{selectedPrediction?.title}</span>
        <span className="status-chip status-chip-info">Granite confidence {stats.confidence}%</span>
      </div>

      <div className="mt-6 grid gap-3 xl:grid-cols-4">
        {timeline.map((item) => (
          <motion.div
            key={item.phase}
            whileHover={{ y: -4 }}
            className="timeline-card rounded-[24px] border border-line bg-white/62 p-4"
          >
            <div className="flex items-center gap-2 text-primary">
              <FlagTriangleRight className="h-4 w-4" />
              <span className="panel-label text-primary">{item.phase}</span>
            </div>
            <div className="mt-3 text-sm leading-6 text-ink">{item.detail}</div>
          </motion.div>
        ))}
      </div>

      <div className="mt-6 flex items-center gap-2 text-sm font-medium text-primary">
        <Zap className="h-4 w-4" />
        Active window remains favorable through the next reaction cycle.
        <ArrowRight className="h-4 w-4" />
      </div>
    </motion.section>
  );
}
