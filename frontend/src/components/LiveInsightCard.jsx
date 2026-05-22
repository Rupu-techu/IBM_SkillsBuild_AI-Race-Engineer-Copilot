import { motion } from "framer-motion";
import { BrainCircuit } from "lucide-react";

export default function LiveInsightCard({ reasoning }) {
  return (
    <motion.section whileHover={{ y: -4 }} className="glass-card ai-reasoning-shell p-5">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="panel-label">Live reasoning</div>
          <div className="panel-title">Granite insight stream</div>
        </div>
        <motion.div
          animate={{
            boxShadow: [
              "0 0 0 rgba(110,231,255,0.0)",
              "0 0 28px rgba(110,231,255,0.30)",
              "0 0 0 rgba(110,231,255,0.0)"
            ]
          }}
          transition={{ duration: 2, repeat: Infinity }}
          className="icon-shell"
        >
          <BrainCircuit className="h-5 w-5" />
        </motion.div>
      </div>
      <div className="mt-4 flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.2em] text-cyan-500">
        <span className="live-dot is-live" />
        Live commentary
      </div>
      <div className="mt-4 space-y-3">
        {reasoning.map((item) => (
          <motion.div
            key={item}
            whileHover={{ x: 2 }}
            className="rounded-[22px] border border-cyan-300/20 bg-[linear-gradient(135deg,rgba(79,140,255,0.08),rgba(110,231,255,0.08))] p-4 text-sm leading-6 text-ink/85"
          >
            {item}
          </motion.div>
        ))}
      </div>
    </motion.section>
  );
}
