# AI Race Engineer Copilot 🏎️

[![IBM SkillsBuild](https://img.shields.io/badge/IBM-SkillsBuild_Challenge-blue)](https://skillsbuild.org)
[![Python](https://img.shields.io/badge/Python-3.9+-green)](https://python.org)
[![IBM Granite](https://img.shields.io/badge/IBM-Granite-red)](https://www.ibm.com/granite)

An AI-powered racing strategy assistant that provides intelligent, explainable race decisions using IBM Granite and watsonx.ai.

## 🎯 Problem Statement

Modern racing environments generate massive amounts of real-time data, making it difficult for teams and drivers to quickly make strategic decisions with confidence. Existing systems often provide raw telemetry without clear reasoning or explainability.

## 💡 Solution

AI Race Engineer Copilot analyzes race conditions in real-time and provides intelligent racing strategy recommendations with explainable AI reasoning, helping teams make confident decisions during critical race moments.

## ✨ Core Features

### 1. Race Condition Analysis
- **Lap-by-lap tracking**: Monitor current lap number and race progress
- **Tire wear analysis**: Real-time tire degradation monitoring
- **Weather conditions**: Track temperature, precipitation, and forecast
- **Position tracking**: Driver position and gap analysis
- **Fuel management**: Fuel level and consumption rate monitoring
- **Track conditions**: Surface temperature and grip levels

### 2. Strategy Recommendations
- **Pit stop timing**: Optimal pit window calculations
- **Tire selection**: Compound recommendations based on conditions
- **Risk analysis**: Probability-based decision scoring
- **Overtaking suggestions**: Strategic passing opportunities

### 3. Explainable AI Reasoning
Every recommendation includes clear, human-readable explanations:

> *"Pit now because tire degradation is increasing and an undercut opportunity is available within the next two laps. Current tire life: 78%, Competitor pit window: 2 laps, Success probability: 85%"*

## 🏗️ Architecture

```
┌─────────────────┐
│  Race Data      │
│  Input Layer    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Langflow       │
│  Orchestration  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  IBM Granite    │
│  AI Engine      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Strategy       │
│  Output + XAI   │
└─────────────────┘
```

## 🛠️ IBM Technologies Used

- **IBM Granite**: Core AI reasoning and decision generation
- **IBM watsonx.ai**: Model execution and experimentation platform
- **Langflow**: AI workflow orchestration and pipeline management
- **Docling**: Processing racing documents and structured knowledge

## 📁 Project Structure

```
ai-race-engineer-copilot/
├── src/
│   ├── core/                 # Core race analysis engine
│   ├── ai/                   # IBM Granite integration
│   ├── workflows/            # Langflow workflows
│   ├── api/                  # REST API endpoints
│   └── utils/                # Helper functions
├── data/
│   ├── sample_races/         # Sample race data
│   ├── telemetry/            # Telemetry datasets
│   └── knowledge_base/       # Racing strategy documents
├── notebooks/                # Jupyter notebooks for experimentation
├── tests/                    # Unit and integration tests
├── docs/                     # Documentation
├── config/                   # Configuration files
└── requirements.txt          # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- IBM Cloud account
- IBM watsonx.ai API credentials

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-race-engineer-copilot.git
cd ai-race-engineer-copilot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your IBM credentials
```

### Configuration

Create a `.env` file with your IBM credentials:

```env
IBM_WATSONX_API_KEY=your_api_key_here
IBM_WATSONX_PROJECT_ID=your_project_id_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
GRANITE_MODEL_ID=ibm/granite-13b-chat-v2
```

### Running the Application

**Option 1: Run the Streamlit Dashboard (Recommended)**
```bash
# Quick start with helper script
python examples/run_dashboard.py

# Or run directly
streamlit run frontend/app.py
```

**Option 2: Run a Sample Analysis**
```bash
# Test the backend engine
python examples/analyze_race.py
```

**Option 3: Start Langflow (Optional)**
```bash
# Start Langflow for advanced workflows
langflow run
```

## 📊 Sample Usage

```python
from src.core.race_analyzer import RaceAnalyzer
from src.ai.granite_engine import GraniteEngine

# Initialize the race engineer
analyzer = RaceAnalyzer()
ai_engine = GraniteEngine()

# Define race conditions
race_data = {
    "lap_number": 25,
    "total_laps": 50,
    "tire_wear": 78,
    "tire_compound": "medium",
    "weather": "dry",
    "track_temp": 42,
    "position": 3,
    "fuel_level": 65,
    "gap_to_leader": 8.5,
    "gap_to_behind": 3.2
}

# Get strategy recommendation
recommendation = analyzer.analyze_strategy(race_data)
explanation = ai_engine.explain_decision(recommendation)

print(f"Recommendation: {recommendation['action']}")
print(f"Reasoning: {explanation}")
```

## 🎓 Development Roadmap

### Phase 1: Foundation ✅
- [x] Project setup and architecture design
- [x] IBM Granite integration
- [x] Basic race data models
- [x] Sample dataset creation

### Phase 2: Core Features ✅
- [x] Race condition analyzer
- [x] Strategy recommendation engine
- [x] Explainable AI module
- [x] Langflow workflow design

### Phase 3: Frontend & Integration ✅
- [x] Streamlit dashboard development
- [x] Real-time AI recommendations
- [x] Interactive visualizations
- [x] Langflow integration

### Phase 4: Polish & Documentation ✅
- [x] Comprehensive documentation
- [x] Frontend setup guide
- [x] Langflow workflow guide
- [x] Example scripts and demos

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test suite
pytest tests/test_race_analyzer.py

# Run with coverage
pytest --cov=src tests/
```

## 📖 Documentation

Detailed documentation is available in the [`docs/`](docs/) directory:

- [Architecture Overview](docs/architecture.md)
- [IBM Granite Integration Guide](docs/granite_integration.md)
- [Frontend Dashboard Guide](docs/FRONTEND_README.md)
- [Frontend Setup Instructions](docs/frontend_setup.md)
- [Langflow Workflow Setup](workflows/langflow_setup.md)
- [Development Roadmap](docs/development_roadmap.md)

## 🎯 Hackathon Presentation Tips

1. **Start with the problem**: Show real racing scenarios where decisions are critical
2. **Demo the explainability**: Highlight how AI reasoning is transparent
3. **Show IBM tech integration**: Emphasize Granite, watsonx.ai, and Langflow usage
4. **Live demo**: Run a real-time race scenario analysis
5. **Impact metrics**: Show how AI improves decision confidence

## 🤝 Contributing

This is a hackathon project, but contributions and suggestions are welcome!

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🏆 IBM SkillsBuild AI Builders Challenge

This project is submitted for the IBM SkillsBuild AI Builders Challenge, demonstrating the power of IBM Granite and watsonx.ai in solving real-world decision-making problems with explainable AI.

## 📧 Contact

For questions or collaboration opportunities, please reach out through GitHub issues.

---

**Built with ❤️ using IBM Granite and watsonx.ai**