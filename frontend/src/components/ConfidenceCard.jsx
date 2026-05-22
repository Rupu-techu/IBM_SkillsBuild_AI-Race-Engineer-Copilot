import { motion } from "framer-motion";

export default function ConfidenceCard({ value, aiLive }) {
  return (
    <motion.section whileHover={{ y: -4 }} className="glass-card confidence-shell p-5">
      <div className="flex items-center justify-between gap-3">
        <div>
          <div className="panel-label">Confidence meter</div>
          <div className="panel-title">Decision quality</div>
        </div>
        <div className="live-pill">
          <span className={`live-dot ${aiLive ? "is-live" : ""}`} />
          {aiLive ? "AI live" : "Standby"}
        </div>
      </div>

      <div className="mt-6 flex items-center gap-5">
        <motion.div
          animate={
            aiLive
              ? {
                  boxShadow: [
                    "0 0 0 rgba(79,140,255,0.0)",
                    "0 0 35px rgba(79,140,255,0.30)",
                    "0 0 0 rgba(79,140,255,0.0)"
                  ]
                }
              : {}
          }
          transition={{ duration: 2.2, repeat: Infinity }}
          className="confidence-ring"
          style={{
            background: `conic-gradient(#4F8CFF 0 ${value * 3.6}deg, rgba(20,33,61,0.08) ${value * 3.6}deg 360deg)`
          }}
        >
          <div className="confidence-ring-inner">
            <div className="font-mono text-3xl font-semibold tracking-[-0.06em] text-ink">{value}%</div>
            <div className="panel-label mt-1">Granite</div>
          </div>
        </motion.div>

        <div className="flex-1">
          <div className="text-sm font-medium text-ink">Weighted consensus is strong across tire wear, rejoin space, and fuel burn.</div>
          <div className="mt-4 h-3 overflow-hidden rounded-full bg-slate-200/70">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${value}%` }}
              transition={{ duration: 0.7, ease: "easeOut" }}
              className="h-full rounded-full bg-[linear-gradient(90deg,#4F8CFF,#6EE7FF,#8B5CF6)] shadow-glow"
            />
          </div>
        </div>
      </div>
    </motion.section>
  );
}
