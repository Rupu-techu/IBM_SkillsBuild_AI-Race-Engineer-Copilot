import { motion } from "framer-motion";
import { ArrowDownRight, Fuel } from "lucide-react";

const riskStyles = {
  medium: "bg-primary/12 text-primary border-primary/20",
  warning: "bg-amber-500/12 text-amber-600 border-amber-300/30",
  danger: "bg-rose-500/12 text-rose-600 border-rose-300/30"
};

export default function PitPredictionCard({ predictions, recommendations, selectedId, onSelect }) {
  return (
    <motion.section whileHover={{ y: -4 }} className="glass-card p-5">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="panel-label">Pit predictions</div>
          <div className="panel-title">Stop window scenarios</div>
        </div>
        <div className="icon-shell">
          <Fuel className="h-5 w-5" />
        </div>
      </div>

      <div className="mt-4 space-y-3">
        {predictions.map((prediction) => {
          const selected = prediction.id === selectedId;
          return (
            <motion.button
              key={prediction.id}
              whileHover={{ y: -2 }}
              whileTap={{ scale: 0.98 }}
              type="button"
              onClick={() => onSelect(prediction.id)}
              className={`w-full rounded-[22px] border p-4 text-left transition-all duration-200 ${
                selected
                  ? "border-primary/30 bg-[linear-gradient(135deg,rgba(79,140,255,0.14),rgba(110,231,255,0.12))] shadow-glow"
                  : "border-line bg-white/60 hover:border-primary/20"
              }`}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="text-sm font-semibold text-ink">{prediction.title}</div>
                <span
                  className={`rounded-full border px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.2em] ${
                    riskStyles[prediction.risk]
                  }`}
                >
                  {prediction.risk}
                </span>
              </div>
              <div className="mt-2 text-sm leading-6 text-muted">{prediction.copy}</div>
              <div className="mt-3 font-mono text-xs uppercase tracking-[0.18em] text-primary">{prediction.meta}</div>
            </motion.button>
          );
        })}
      </div>

      <div className="mt-5 rounded-[24px] border border-primary/15 bg-[linear-gradient(135deg,rgba(79,140,255,0.12),rgba(110,231,255,0.12),rgba(139,92,246,0.10))] p-4">
        <div className="flex items-center gap-2 text-primary">
          <ArrowDownRight className="h-4 w-4" />
          <span className="panel-label text-primary">Strategy recommendations</span>
        </div>
        <div className="mt-3 space-y-2">
          {recommendations.map((item) => (
            <div key={item} className="rounded-[18px] bg-white/55 px-3 py-2 text-sm leading-6 text-ink">
              {item}
            </div>
          ))}
        </div>
      </div>
    </motion.section>
  );
}
