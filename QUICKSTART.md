# 🚀 Quick Start Guide

Get the **AI Race Engineer Copilot** running in **5 minutes**!

---

## 📋 Prerequisites

Before you begin, ensure you have:

- ✅ **Python 3.9+** — [Download Python](https://python.org)
- ✅ **Node.js 18+** — [Download Node.js](https://nodejs.org)
- ✅ **Git** — [Download Git](https://git-scm.com)
- ⚠️ **IBM watsonx.ai account** — Optional for demo mode

---

## ⚡ Quick Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ai-race-engineer-copilot.git
cd ai-race-engineer-copilot
```

### Step 2: Backend Setup (Python)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Frontend Setup (React)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Return to root directory
cd ..
```

### Step 4: Environment Configuration (Optional)

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your IBM credentials (optional)
# The app works in demo mode without credentials!
```

**Example `.env` file:**
```env
IBM_WATSONX_API_KEY=your_api_key_here
IBM_WATSONX_PROJECT_ID=your_project_id_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
GRANITE_MODEL_ID=ibm/granite-13b-chat-v2
```

---

## 🎮 Running the Application

### Option 1: React Frontend (Recommended) 🌟

**Best for:** Interactive dashboard experience with real-time updates

```bash
cd frontend
npm run dev
```

**Access at:** `http://localhost:5173`

**Features:**
- ✅ Modern React UI with TailwindCSS
- ✅ Real-time telemetry visualization
- ✅ Interactive strategy panels
- ✅ Live AI recommendations
- ✅ Smooth animations and transitions

---

### Option 2: Python Backend Demo

**Best for:** Testing core AI engine and strategy analysis

```bash
# Run example race analysis
python examples/analyze_race.py
```

**Output:**
```
🏎️ AI Race Engineer Copilot - Race Analysis Demo
================================================

Analyzing Race Scenario 1: Critical Tire Wear
----------------------------------------------
Lap: 28/50
Position: P3
Tire Wear: 87.5%
Tire Age: 18 laps (Medium)
Fuel: 62.0%

🤖 AI Recommendation:
Action: PIT_NOW
Confidence: 92%
Risk Level: HIGH

💡 Reasoning:
Pit now because tire degradation is critical at 87.5%...
```

---

### Option 3: Langflow Workflows (Advanced)

**Best for:** Visual AI workflow design and orchestration

```bash
# Start Langflow server
langflow run
```

**Access at:** `http://localhost:7860`

**Features:**
- ✅ Visual workflow editor
- ✅ Drag-and-drop components
- ✅ IBM Granite integration
- ✅ Real-time testing

**[📖 Langflow Setup Guide](workflows/langflow_setup.md)**

---

## 🎯 Using the Dashboard

### 1️⃣ Configure Race Conditions

In the **sidebar**, set your race parameters:

| Parameter | Example Value | Description |
|-----------|---------------|-------------|
| **Current Lap** | 28 | Current lap number |
| **Total Laps** | 50 | Total race laps |
| **Position** | 3 | Current race position |
| **Tire Wear** | 78% | Tire degradation level |
| **Tire Compound** | Medium | Current tire type |
| **Tire Age** | 15 laps | Laps on current tires |
| **Fuel Level** | 65% | Remaining fuel |
| **Weather** | Dry | Current conditions |

### 2️⃣ Analyze Strategy

Click the **"🤖 ANALYZE STRATEGY"** button

The AI will process your race conditions and generate:
- ✅ Primary recommendation (PIT NOW, STAY OUT, etc.)
- ✅ Confidence score (0-100%)
- ✅ Risk assessment (LOW, MEDIUM, HIGH, CRITICAL)
- ✅ Detailed reasoning with data support
- ✅ Expected outcome

### 3️⃣ Review AI Insights

**Strategy Panel:**
- **Action** — What to do (pit, stay out, push hard)
- **Confidence** — How certain the AI is
- **Risk Level** — Potential consequences
- **Reasoning** — Why this strategy is optimal
- **Alternatives** — Other options with trade-offs

### 4️⃣ Explore Analytics

Switch between tabs to view:

- **🛞 Tire Analysis** — Degradation curves and predictions
- **⛽ Fuel Strategy** — Consumption rates and finish projections
- **📈 Performance** — Lap times and pace analysis
- **⏱️ Pit Windows** — Optimal timing visualization

---

## 🎬 Demo Scenarios

Try these pre-configured scenarios to see the AI in action:

### Scenario 1: Critical Tire Wear 🔴

```
Lap: 30/50
Tire Wear: 88%
Tire Age: 20 laps
Compound: Soft
```

**Expected:** `PIT_NOW` recommendation with high confidence

---

### Scenario 2: Fuel Emergency ⛽

```
Lap: 42/50
Fuel Level: 12%
Tire Wear: 65%
```

**Expected:** `PIT_NOW` for fuel with critical risk warning

---

### Scenario 3: Weather Change 🌧️

```
Lap: 25/50
Weather: Light Rain
Current Tires: Slicks
Track Temp: Dropping
```

**Expected:** `PIT_NOW` for intermediate tires

---

### Scenario 4: Undercut Opportunity 🎯

```
Lap: 22/50
Position: P3
Gap to P2: 2.8s
Tire Wear: 72%
Competitor Tire Age: +5 laps
```

**Expected:** `PIT_NEXT_LAP` for undercut strategy

---

### Scenario 5: Optimal Strategy ✅

```
Lap: 25/50
Tire Wear: 58%
Fuel: 70%
Position: P2
Track: Green
```

**Expected:** `STAY_OUT` with medium confidence

---

## 🔧 Troubleshooting

### Dashboard Won't Start?

```bash
# Check Python version
python --version  # Should be 3.9+

# Check Node version
node --version    # Should be 18+

# Reinstall dependencies
pip install --upgrade -r requirements.txt
cd frontend && npm install
```

### Import Errors?

```bash
# Ensure you're in project root
pwd  # Should show: .../ai-race-engineer-copilot

# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Reinstall packages
pip install -r requirements.txt
```

### Frontend Build Errors?

```bash
cd frontend

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Try running again
npm run dev
```

### IBM Granite Not Working?

**Don't worry!** The dashboard works in **demo mode** without IBM credentials.

To enable full AI features:
1. Create IBM Cloud account at [cloud.ibm.com](https://cloud.ibm.com)
2. Set up watsonx.ai project
3. Get API key from IBM Cloud console
4. Add credentials to `.env` file

**Demo mode provides:**
- ✅ Full UI functionality
- ✅ Strategy recommendations
- ✅ Telemetry visualization
- ⚠️ Simulated AI explanations (not real Granite)

---

## 📚 Next Steps

### 🎓 Learn More

1. **[📖 Full Documentation](docs/)** — Comprehensive guides
2. **[🏗️ Architecture Overview](docs/architecture.md)** — System design
3. **[🤖 IBM Tools Usage](IBM_TOOLS_USAGE.md)** — Granite, watsonx.ai, Langflow
4. **[🎨 Frontend Guide](docs/FRONTEND_README.md)** — React dashboard details

### 🛠️ Customize

1. **Add Race Scenarios** — Create JSON files in `data/sample_races/`
2. **Modify Components** — Edit React components in `frontend/src/components/`
3. **Extend AI Logic** — Update `src/ai/granite_engine.py`
4. **Create Workflows** — Design Langflow pipelines in `workflows/`

### 🤝 Contribute

1. **[📝 Contributing Guide](CONTRIBUTING.md)** — How to contribute
2. **[🐛 Report Issues](https://github.com/yourusername/ai-race-engineer-copilot/issues)** — Bug reports
3. **[💬 Discussions](https://github.com/yourusername/ai-race-engineer-copilot/discussions)** — Questions and ideas

---

## 🎯 Key Features to Explore

### ✅ Real-Time Strategy Analysis
Get instant AI recommendations based on current race conditions

### ✅ Explainable AI Reasoning
Understand exactly why the AI recommends each strategy

### ✅ Interactive Visualizations
Explore tire wear, fuel consumption, and performance data

### ✅ Multiple Scenarios
Test different race conditions and see how strategies change

### ✅ Professional UI
Experience an F1-inspired racing dashboard

### ✅ Live Simulation
Watch dynamic race events unfold with real-time updates

---

## 💡 Pro Tips

### Tip 1: Start with Demo Scenarios
Use the pre-configured scenarios to understand how the AI analyzes different situations.

### Tip 2: Compare Strategies
Try similar conditions with small variations to see how the AI adapts its recommendations.

### Tip 3: Check Confidence Scores
Higher confidence (>80%) means the AI is very certain. Lower confidence suggests multiple viable options.

### Tip 4: Read the Reasoning
The AI's explanation shows which factors influenced the decision most.

### Tip 5: Explore Analytics
The charts reveal patterns in tire wear and fuel consumption that inform strategy.

---

## 📞 Getting Help

### Documentation
- **[README](README.md)** — Project overview
- **[Architecture](docs/architecture.md)** — Technical details
- **[Frontend Guide](docs/FRONTEND_README.md)** — UI documentation

### Community
- **[GitHub Issues](https://github.com/yourusername/ai-race-engineer-copilot/issues)** — Bug reports
- **[Discussions](https://github.com/yourusername/ai-race-engineer-copilot/discussions)** — Q&A

### Resources
- **[IBM Granite Docs](https://www.ibm.com/granite)** — AI model documentation
- **[watsonx.ai Guide](https://www.ibm.com/watsonx)** — Platform documentation
- **[Langflow Docs](https://docs.langflow.org)** — Workflow orchestration

---

## 🏁 Ready to Race!

You're all set! Start the dashboard and experience AI-powered racing strategy:

```bash
cd frontend
npm run dev
```

**Open:** `http://localhost:5173`

---

<div align="center">

### Built with ❤️ for the IBM SkillsBuild AI Builders Challenge

🏎️ **AI Race Engineer Copilot** — *Intelligent, Explainable, Real-Time*

**[⭐ Star on GitHub](https://github.com/yourusername/ai-race-engineer-copilot)** • **[📖 Read Docs](docs/)** • **[🎥 Watch Demo](#)**

</div>