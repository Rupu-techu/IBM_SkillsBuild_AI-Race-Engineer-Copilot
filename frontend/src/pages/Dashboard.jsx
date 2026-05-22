import { startTransition, useDeferredValue, useEffect, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Activity, Flag, GaugeCircle, Timer } from "lucide-react";
import Header from "../components/Header";
import Sidebar from "../components/Sidebar";
import TelemetryCard from "../components/TelemetryCard";
import StrategyPanel from "../components/StrategyPanel";
import WeatherCard from "../components/WeatherCard";
import ConfidenceCard from "../components/ConfidenceCard";
import TireWearChart from "../components/TireWearChart";
import LiveInsightCard from "../components/LiveInsightCard";
import PitPredictionCard from "../components/PitPredictionCard";
import {
  createResetState,
  simulateTelemetryTick,
  telemetryViews
} from "../data/mockTelemetry";

const panelToView = {
  telemetry: "pace",
  strategy: "degradation",
  weather: "weather",
  ai: "ai",
  overview: "pace"
};

export default function Dashboard() {
  const [dashboardState, setDashboardState] = useState(() => createResetState());
  const [activePanel, setActivePanel] = useState("overview");
  const [telemetryView, setTelemetryView] = useState("pace");
  const [isRunning, setIsRunning] = useState(true);
  const [aiLive, setAiLive] = useState(true);
  const [selectedPrediction, setSelectedPrediction] = useState("one-stop-undercut");
  const [searchQuery, setSearchQuery] = useState("");
  const [flashedSectionId, setFlashedSectionId] = useState("");
  const deferredSearchQuery = useDeferredValue(searchQuery);
  const sectionRefs = useRef({});

  useEffect(() => {
    if (!isRunning) {
      return undefined;
    }

    const interval = window.setInterval(() => {
      startTransition(() => {
        setDashboardState((current) => simulateTelemetryTick(current));
      });
    }, 2600);

    return () => window.clearInterval(interval);
  }, [isRunning]);

  const stats = dashboardState.stats;
  const normalizedSearchQuery = deferredSearchQuery.trim().toLowerCase();
  const commandQuery = normalizedSearchQuery.startsWith("/") ? normalizedSearchQuery.slice(1).trim() : "";
  const topMetrics = [
    { label: "Race status", value: stats.status, icon: Activity },
    { label: "Lap progress", value: `${stats.lap}/${stats.totalLaps}`, icon: Timer },
    { label: "Track position", value: `P${stats.position}`, icon: Flag },
    { label: "Gap to leader", value: `${stats.gapAhead}s`, icon: GaugeCircle }
  ];
  const sections = [
    {
      id: "strategy",
      title: "Pit Strategy",
      keywords: ["strategy", "pit", "tires", "undercut", "track", "position"],
      panel: "strategy"
    },
    {
      id: "telemetry",
      title: "Telemetry",
      keywords: ["speed", "telemetry", "lap", "fuel", "pace", "signal"],
      panel: "telemetry",
      telemetryView: "pace"
    },
    {
      id: "tire",
      title: "Tire Wear",
      keywords: ["tire", "tires", "wear", "degradation", "compound", "grip"],
      panel: "strategy",
      telemetryView: "degradation"
    },
    {
      id: "weather",
      title: "Weather Analytics",
      keywords: ["weather", "rain", "track", "temperature", "climate", "wind"],
      panel: "weather",
      telemetryView: "weather"
    },
    {
      id: "confidence",
      title: "AI Confidence",
      keywords: ["confidence", "ai", "granite", "decision", "consensus"],
      panel: "ai",
      telemetryView: "ai"
    },
    {
      id: "pit",
      title: "Pit Predictions",
      keywords: ["pit", "strategy", "fuel", "stop", "window", "undercut"],
      panel: "strategy"
    },
    {
      id: "ai",
      title: "AI Insights",
      keywords: ["ai", "reasoning", "insight", "commentary", "confidence", "granite"],
      panel: "ai",
      telemetryView: "ai"
    }
  ];
  const filteredSections = sections.filter((section) => {
    if (!normalizedSearchQuery) {
      return true;
    }

    if (commandQuery) {
      return (
        section.id.includes(commandQuery) ||
        section.title.toLowerCase().includes(commandQuery) ||
        section.keywords.some((keyword) => keyword.includes(commandQuery))
      );
    }

    return (
      section.title.toLowerCase().includes(normalizedSearchQuery) ||
      section.keywords.some((keyword) => keyword.includes(normalizedSearchQuery))
    );
  });
  const matchingSectionIds = filteredSections.map((section) => section.id);
  const searchActive = normalizedSearchQuery.length > 0;
  const firstMatch = filteredSections[0] ?? null;
  const firstMatchId = firstMatch?.id ?? "";
  const hasMatches = filteredSections.length > 0;

  const handleSelectPanel = (panel) => {
    setActivePanel(panel);
    if (panelToView[panel]) {
      setTelemetryView(panelToView[panel]);
    }
  };

  const activePrediction =
    dashboardState.pitPredictions.find((item) => item.id === selectedPrediction) ??
    dashboardState.pitPredictions[0];

  const resetDashboard = (shouldRun = false) => {
    setDashboardState(createResetState());
    setActivePanel("overview");
    setTelemetryView("pace");
    setAiLive(true);
    setIsRunning(shouldRun);
    setSelectedPrediction("one-stop-undercut");
  };

  const startSimulation = () => {
    setIsRunning(true);
    setActivePanel("overview");
  };

  const activateAiStrategy = () => {
    setAiLive(true);
    setActivePanel("ai");
    setTelemetryView("ai");
  };

  const runRaceReplay = () => {
    resetDashboard(true);
  };

  const focusSection = (section) => {
    if (!section) {
      return;
    }

    if (section.panel) {
      setActivePanel(section.panel);
    }

    if (section.telemetryView) {
      setTelemetryView(section.telemetryView);
    }

    setFlashedSectionId(section.id);
    window.setTimeout(() => {
      setFlashedSectionId((current) => (current === section.id ? "" : current));
    }, 1600);

    const targetNode = sectionRefs.current[section.id];
    if (targetNode) {
      window.requestAnimationFrame(() => {
        targetNode.scrollIntoView({ behavior: "smooth", block: "start", inline: "nearest" });
      });
    }
  };

  useEffect(() => {
    if (!searchActive || !firstMatch) {
      return;
    }
    focusSection(firstMatch);
  }, [firstMatchId, searchActive]);

  const getSectionStateClasses = (sectionId) => {
    if (!searchActive) {
      return "";
    }

    const matches = matchingSectionIds.includes(sectionId);
    const flashed = flashedSectionId === sectionId;
    if (matches && flashed) {
      return "search-section-shell-active search-section-shell-flash";
    }
    if (matches) {
      return "search-section-shell-active";
    }
    return "search-section-shell-dimmed";
  };
  const attachSectionRef = (sectionId) => (node) => {
    if (node) {
      sectionRefs.current[sectionId] = node;
    }
  };

  return (
    <div className="min-h-screen bg-dashboard-shell">
      <div className="mx-auto flex max-w-[1600px] flex-col gap-5 px-4 py-4 lg:px-5 lg:py-5">
        <Header
          stats={stats}
          aiLive={aiLive}
          isRunning={isRunning}
          telemetryPreview={dashboardState.series.slice(-7)}
          searchQuery={searchQuery}
          onSearchQueryChange={setSearchQuery}
          resultCount={searchActive ? filteredSections.length : sections.length}
          firstResultTitle={firstMatch?.title ?? ""}
          searchResults={filteredSections}
          searchActive={searchActive}
          hasMatches={hasMatches}
          onSelectResult={focusSection}
          onStartSimulation={startSimulation}
          onActivateAiStrategy={activateAiStrategy}
          onRaceReplay={runRaceReplay}
        />

        <div className="grid gap-5 xl:grid-cols-[18fr_57fr_25fr]">
          <div className="xl:sticky xl:top-5 xl:self-start">
            <Sidebar
              activePanel={activePanel}
              onSelectPanel={handleSelectPanel}
              isRunning={isRunning}
              onRun={() => setIsRunning(true)}
              onPause={() => setIsRunning(false)}
              onReset={() => resetDashboard(false)}
              aiLive={aiLive}
              onToggleAiLive={() => setAiLive((current) => !current)}
              telemetryView={telemetryView}
            />
          </div>

          <main className="space-y-5">
            <div className={`grid gap-4 md:grid-cols-2 xl:grid-cols-4 ${searchActive ? "search-metrics-dimmed" : ""}`}>
              {topMetrics.map(({ label, value, icon: Icon }, index) => (
                <motion.section
                  key={label}
                  initial={{ opacity: 0, y: 14 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.35, delay: index * 0.05 }}
                  className="glass-card metric-card p-4"
                >
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <div className="panel-label">{label}</div>
                      <div className="mt-3 font-mono text-xl font-semibold tracking-[-0.04em] text-ink">
                        {value}
                      </div>
                    </div>
                    <div className="icon-shell">
                      <Icon className="h-4 w-4" />
                    </div>
                  </div>
                </motion.section>
              ))}
            </div>

            <motion.div ref={attachSectionRef("strategy")} className={`search-section-shell ${getSectionStateClasses("strategy")}`}>
              <div className="search-match-pill">Pit Strategy</div>
              <StrategyPanel
                stats={stats}
                timeline={dashboardState.timeline}
                activePanel={activePanel}
                selectedPrediction={activePrediction}
              />
            </motion.div>

            <motion.div ref={attachSectionRef("telemetry")} className={`search-section-shell ${getSectionStateClasses("telemetry")}`}>
              <div className="search-match-pill">Telemetry</div>
              <TelemetryCard
                data={dashboardState.series}
                telemetryView={telemetryView}
                onTelemetryViewChange={setTelemetryView}
                viewOptions={telemetryViews}
                isRunning={isRunning}
              />
            </motion.div>

            <motion.div ref={attachSectionRef("tire")} className={`search-section-shell ${getSectionStateClasses("tire")}`}>
              <div className="search-match-pill">Tire Wear</div>
              <TireWearChart stats={stats} isRunning={isRunning} />
            </motion.div>

            <motion.div className={`search-section-shell ${getSectionStateClasses("strategy")}`}>
              <div className="glass-card telemetry-timeline-card p-5">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <div className="panel-label">Strategy timeline</div>
                    <div className="panel-title">Race insights</div>
                  </div>
                  <div className="live-pill">
                    <span className={`live-dot ${isRunning ? "is-live" : ""}`} />
                    {isRunning ? "Live" : "Paused"}
                  </div>
                </div>
                <div className="mt-5 space-y-4">
                  {dashboardState.timeline.map((item, index) => (
                    <motion.button
                      type="button"
                      key={item.phase}
                      whileHover={{ x: 3 }}
                      onClick={() => handleSelectPanel("strategy")}
                      className="flex w-full gap-4 text-left"
                    >
                      <div className="flex flex-col items-center">
                        <div className="timeline-node" />
                        {index < dashboardState.timeline.length - 1 ? (
                          <div className="mt-2 h-full w-px bg-line" />
                        ) : null}
                      </div>
                      <div className="pb-4">
                        <div className="font-mono text-xs font-semibold uppercase tracking-[0.2em] text-primary">
                          {item.phase}
                        </div>
                        <div className="mt-2 text-sm leading-6 text-muted">{item.detail}</div>
                      </div>
                    </motion.button>
                  ))}
                </div>
              </div>
            </motion.div>
          </main>

          <aside className="space-y-5">
            <motion.div ref={attachSectionRef("weather")} className={`search-section-shell ${getSectionStateClasses("weather")}`}>
              <div className="search-match-pill">Weather Analytics</div>
              <WeatherCard
                stats={stats}
                signals={dashboardState.weatherSignals}
                expanded={activePanel === "weather"}
                onExpand={() => handleSelectPanel("weather")}
              />
            </motion.div>

            <motion.div ref={attachSectionRef("confidence")} className={`search-section-shell ${getSectionStateClasses("confidence")}`}>
              <div className="search-match-pill">AI Confidence</div>
              <ConfidenceCard value={stats.confidence} aiLive={aiLive} />
            </motion.div>

            <motion.div ref={attachSectionRef("pit")} className={`search-section-shell ${getSectionStateClasses("pit")}`}>
              <div className="search-match-pill">Pit Predictions</div>
              <PitPredictionCard
                predictions={dashboardState.pitPredictions}
                recommendations={dashboardState.recommendations}
                selectedId={selectedPrediction}
                onSelect={setSelectedPrediction}
              />
            </motion.div>

            <motion.div ref={attachSectionRef("ai")} className={`search-section-shell ${getSectionStateClasses("ai")}`}>
              <div className="search-match-pill">AI Insights</div>
              <AnimatePresence mode="wait">
                {aiLive ? (
                  <LiveInsightCard key="live" reasoning={dashboardState.aiReasoning} />
                ) : (
                  <motion.section
                    key="paused"
                    initial={{ opacity: 0, y: 12 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -12 }}
                    className="glass-card p-5"
                  >
                    <div className="panel-label">AI commentary</div>
                    <div className="panel-title">Live stream paused</div>
                    <div className="mt-4 text-sm leading-7 text-muted">
                      AI Live is currently off. Re-enable the commentary channel from the sidebar to resume the
                      Granite reasoning feed.
                    </div>
                  </motion.section>
                )}
              </AnimatePresence>
            </motion.div>
          </aside>
        </div>
      </div>
    </div>
  );
}
