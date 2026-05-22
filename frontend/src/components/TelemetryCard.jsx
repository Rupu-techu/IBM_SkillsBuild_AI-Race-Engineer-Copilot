import { motion } from "framer-motion";
import {
  Area,
  AreaChart,
  CartesianGrid,
  Legend,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";

const viewMeta = {
  pace: {
    title: "Live pace and reserve curve",
    primaryKey: "pace",
    secondaryKey: "reserve",
    primaryName: "Telemetry pace",
    secondaryName: "Tire reserve"
  },
  degradation: {
    title: "Degradation and crossover pressure",
    primaryKey: "degradation",
    secondaryKey: "reserve",
    primaryName: "Tire degradation",
    secondaryName: "Pit reserve"
  },
  weather: {
    title: "Grip energy and weather pressure",
    primaryKey: "energy",
    secondaryKey: "pace",
    primaryName: "Track energy",
    secondaryName: "Stint pace"
  },
  ai: {
    title: "AI attention and telemetry confidence",
    primaryKey: "pace",
    secondaryKey: "energy",
    primaryName: "Signal strength",
    secondaryName: "AI attention"
  }
};

export default function TelemetryCard({
  data,
  telemetryView,
  onTelemetryViewChange,
  viewOptions,
  isRunning
}) {
  const meta = viewMeta[telemetryView] ?? viewMeta.pace;
  const latest = data[data.length - 1];

  return (
    <motion.section
      whileHover={{ y: -4 }}
      transition={{ duration: 0.2 }}
      className="glass-card telemetry-surface p-5"
    >
      <div className="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
        <div>
          <div className="panel-label">Telemetry graph</div>
          <div className="panel-title">{meta.title}</div>
        </div>

        <div className="flex flex-wrap gap-2">
          {viewOptions.map((view) => (
            <motion.button
              key={view.id}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.97 }}
              type="button"
              onClick={() => onTelemetryViewChange(view.id)}
              className={`telemetry-tab ${telemetryView === view.id ? "telemetry-tab-active" : ""}`}
            >
              {view.label}
            </motion.button>
          ))}
        </div>
      </div>

      <div className="mt-5 grid gap-3 md:grid-cols-3">
        <div className="telemetry-chip">
          <div className="panel-label">Live signal</div>
          <div className="mt-3 font-mono text-2xl font-semibold text-ink">{latest?.[meta.primaryKey] ?? "--"}</div>
        </div>
        <div className="telemetry-chip">
          <div className="panel-label">Secondary trace</div>
          <div className="mt-3 font-mono text-2xl font-semibold text-ink">{latest?.[meta.secondaryKey] ?? "--"}</div>
        </div>
        <div className="telemetry-chip">
          <div className="panel-label">Feed status</div>
          <div className="mt-3 flex items-center gap-2 font-medium text-ink">
            <span className={`live-dot ${isRunning ? "is-live" : ""}`} />
            {isRunning ? "Updating live" : "Held"}
          </div>
        </div>
      </div>

      <div className="mt-4 h-80">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -18, bottom: 0 }}>
            <defs>
              <linearGradient id="telemetryPrimaryFill" x1="0" x2="0" y1="0" y2="1">
                <stop offset="0%" stopColor="#4F8CFF" stopOpacity={0.42} />
                <stop offset="100%" stopColor="#4F8CFF" stopOpacity={0.03} />
              </linearGradient>
              <linearGradient id="telemetrySecondaryFill" x1="0" x2="0" y1="0" y2="1">
                <stop offset="0%" stopColor="#6EE7FF" stopOpacity={0.28} />
                <stop offset="100%" stopColor="#6EE7FF" stopOpacity={0.02} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="rgba(120,140,180,0.12)" vertical={false} />
            <XAxis
              dataKey="lap"
              tick={{ fill: "#7B8AA5", fontSize: 12 }}
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              tick={{ fill: "#7B8AA5", fontSize: 12 }}
              tickLine={false}
              axisLine={false}
            />
            <Tooltip
              contentStyle={{
                background: "rgba(255,255,255,0.97)",
                border: "1px solid rgba(120,140,180,0.15)",
                borderRadius: 20,
                boxShadow: "0 20px 50px rgba(79, 140, 255, 0.16)"
              }}
            />
            <Legend wrapperStyle={{ fontSize: 12, color: "#7B8AA5" }} />
            <Area
              type="monotone"
              dataKey={meta.primaryKey}
              stroke="#4F8CFF"
              strokeWidth={3}
              fill="url(#telemetryPrimaryFill)"
              name={meta.primaryName}
              isAnimationActive
              animationDuration={700}
            />
            <Area
              type="monotone"
              dataKey={meta.secondaryKey}
              stroke="#6EE7FF"
              strokeWidth={2}
              fill="url(#telemetrySecondaryFill)"
              name={meta.secondaryName}
              isAnimationActive
              animationDuration={700}
            />
            <Line
              type="monotone"
              dataKey={meta.primaryKey}
              stroke="#8B5CF6"
              strokeWidth={0}
              dot={{ r: 3.5, fill: "#8B5CF6", stroke: "#ffffff", strokeWidth: 2 }}
              activeDot={{ r: 6, fill: "#4F8CFF", stroke: "#6EE7FF", strokeWidth: 3 }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </motion.section>
  );
}
