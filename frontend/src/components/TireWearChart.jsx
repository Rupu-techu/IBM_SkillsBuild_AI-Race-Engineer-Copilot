import { motion } from "framer-motion";
import {
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  RadialBar,
  RadialBarChart,
  ResponsiveContainer
} from "recharts";

export default function TireWearChart({ stats, isRunning }) {
  const data = [{ name: "Tire wear", value: stats.tireWear, fill: "#4F8CFF" }];

  return (
    <motion.section whileHover={{ y: -4 }} className="glass-card p-5">
      <div className="flex items-center justify-between gap-3">
        <div>
          <div className="panel-label">Tire degradation</div>
          <div className="panel-title">Wear model</div>
        </div>
        <div className="live-pill">
          <span className={`live-dot ${isRunning ? "is-live" : ""}`} />
          {isRunning ? "Sampling" : "Static"}
        </div>
      </div>

      <div className="mt-4 grid items-center gap-4 lg:grid-cols-[0.95fr_1.05fr]">
        <div className="h-48">
          <ResponsiveContainer width="100%" height="100%">
            <RadialBarChart innerRadius="70%" outerRadius="100%" data={data} startAngle={90} endAngle={-270}>
              <PolarGrid radialLines={false} stroke="rgba(120,140,180,0.12)" />
              <PolarAngleAxis type="number" domain={[0, 100]} tick={false} />
              <PolarRadiusAxis tick={false} axisLine={false} />
              <RadialBar background clockWise dataKey="value" cornerRadius={20} />
            </RadialBarChart>
          </ResponsiveContainer>
        </div>

        <div className="space-y-3">
          <div className="metric-value text-[2.4rem]">{stats.tireWear}%</div>
          <div className="text-sm leading-6 text-muted">
            {stats.tireCompound} compound on lap-age {stats.tireAge}. The degradation curve is steepening and
            elevating the crossover urgency.
          </div>
          <div className="rounded-[22px] border border-line bg-white/60 px-4 py-3">
            <div className="panel-label">Tire reserve</div>
            <div className="mt-2 font-mono text-xl font-semibold text-ink">{100 - stats.tireWear}%</div>
          </div>
          <div className="h-2.5 overflow-hidden rounded-full bg-slate-200/70">
            <motion.div
              animate={{ width: `${stats.tireWear}%` }}
              transition={{ duration: 0.6 }}
              className="h-full rounded-full bg-[linear-gradient(90deg,#22C55E,#F59E0B,#EF4444)]"
            />
          </div>
        </div>
      </div>
    </motion.section>
  );
}
