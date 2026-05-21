# AI Race Engineer Copilot - Frontend Dashboard

## 🎯 Overview

A modern, real-time racing strategy dashboard powered by IBM Granite AI, built with Streamlit for an immersive Formula 1-inspired experience.

## ✨ Features

### 🎛️ Interactive Controls
- **Comprehensive Sidebar**: All race parameters in one place
- **Real-time Inputs**: Tire wear, fuel level, weather, track conditions
- **Driver Modes**: Conservative, Balanced, Aggressive strategies
- **Visual Indicators**: Color-coded status for critical parameters

### 📡 Live Telemetry
- **Race Progress**: Visual progress bar and lap counter
- **Key Metrics**: Position, tire wear, fuel, temperature
- **Status Cards**: Tire information, weather data, competitive position
- **Race Situation**: Phase analysis and resource management

### 🤖 AI-Powered Recommendations
- **IBM Granite Integration**: Advanced AI reasoning
- **Strategy Actions**: Pit now, pit next lap, stay out, push hard
- **Confidence Scores**: AI confidence in recommendations (0-100%)
- **Risk Assessment**: Low, medium, high risk evaluation
- **Explainable AI**: Clear reasoning for every decision
- **Alternative Strategies**: Multiple options with trade-offs
- **Pit Strategy Options**: One-stop, two-stop, conservative plans
- **Overtaking Analysis**: Opportunity assessment when applicable

### 📊 Advanced Analytics
- **Tire Degradation**: Historical and projected wear curves
- **Fuel Consumption**: Usage tracking and finish projections
- **Lap Performance**: Time evolution and pace analysis
- **Pit Strategy**: Timing windows and optimal pit stops

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your IBM credentials
```

### Running the Dashboard

**Option 1: Using the helper script**
```bash
python examples/run_dashboard.py
```

**Option 2: Direct Streamlit command**
```bash
streamlit run frontend/app.py
```

**Option 3: Custom configuration**
```bash
streamlit run frontend/app.py --server.port 8080 --theme.base dark
```

The dashboard will open at `http://localhost:8501`

## 🎨 User Interface

### Dark Racing Theme
- **Color Scheme**: Dark background with racing-inspired accents
- **Primary Colors**: Red (#e63946) and Orange (#f77f00)
- **Status Colors**: 
  - Green (#06ffa5) - Good/Safe
  - Yellow (#ffd60a) - Warning/Moderate
  - Red (#e63946) - Critical/Danger

### Layout Structure

```
┌─────────────────────────────────────────────────────────┐
│                    HEADER                                │
│              AI RACE ENGINEER COPILOT                    │
└─────────────────────────────────────────────────────────┘
┌──────────────┬──────────────────────────────────────────┐
│              │                                           │
│   SIDEBAR    │         MAIN CONTENT AREA                │
│              │                                           │
│  - Race      │  ┌─────────────────────────────────────┐ │
│    Progress  │  │     LIVE TELEMETRY PANEL            │ │
│  - Tire      │  └─────────────────────────────────────┘ │
│    Status    │                                           │
│  - Fuel      │  ┌─────────────────────────────────────┐ │
│  - Weather   │  │     RACE ANALYTICS (TABS)           │ │
│  - Position  │  │  • Tire Degradation                 │ │
│  - Track     │  │  • Fuel Analysis                    │ │
│  - Driver    │  │  • Lap Performance                  │ │
│    Mode      │  │  • Pit Strategy                     │ │
│              │  └─────────────────────────────────────┘ │
│  [ANALYZE]   │                                           │
│              │  ┌─────────────────────────────────────┐ │
│              │  │   AI RECOMMENDATIONS                │ │
│              │  │  • Primary Strategy                 │ │
│              │  │  • Confidence & Risk                │ │
│              │  │  • AI Reasoning                     │ │
│              │  │  • Expected Outcome                 │ │
│              │  │  • Alternatives                     │ │
│              │  └─────────────────────────────────────┘ │
└──────────────┴──────────────────────────────────────────┘
```

## 📖 Usage Guide

### Basic Workflow

1. **Set Race Conditions**
   - Adjust lap number and total laps
   - Set current position
   - Configure tire wear and compound
   - Set fuel level
   - Select weather conditions
   - Input competitive gaps

2. **Analyze Strategy**
   - Click "🤖 ANALYZE STRATEGY" button
   - Wait for AI processing (2-5 seconds)
   - Review recommendations

3. **Explore Results**
   - Read primary recommendation
   - Check confidence and risk scores
   - Review AI reasoning
   - Explore alternative strategies
   - Analyze visualizations

4. **Iterate**
   - Adjust parameters
   - Re-analyze
   - Compare different scenarios

### Advanced Features

**Scenario Testing**
- Test high tire wear scenarios
- Simulate fuel critical situations
- Analyze weather changes
- Compare driver aggression modes

**Strategy Comparison**
- Run analysis with different inputs
- Compare conservative vs aggressive
- Evaluate pit timing options
- Assess risk vs reward

**Data Analysis**
- Review tire degradation trends
- Monitor fuel consumption patterns
- Analyze lap time evolution
- Identify optimal pit windows

## 🔧 Configuration

### Streamlit Configuration

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#e63946"
backgroundColor = "#0a0a0a"
secondaryBackgroundColor = "#1a1a2e"
textColor = "#ffffff"
font = "monospace"

[server]
port = 8501
headless = false
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

### Environment Variables

Required in `.env`:
```env
IBM_WATSONX_API_KEY=your_api_key
IBM_WATSONX_PROJECT_ID=your_project_id
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
GRANITE_MODEL_ID=ibm/granite-13b-chat-v2
```

Optional:
```env
LANGFLOW_URL=http://localhost:7860
GRANITE_MAX_TOKENS=1024
GRANITE_TEMPERATURE=0.7
```

## 🎯 Key Components

### Sidebar (`frontend/components/sidebar.py`)
- Race condition inputs
- Visual status indicators
- Driver mode selection
- Analyze button

### Telemetry Panel (`frontend/components/telemetry.py`)
- Live race data display
- Metric cards
- Progress indicators
- Situation summary

### AI Recommendations (`frontend/components/ai_recommendations.py`)
- Strategy display
- Confidence visualization
- Risk assessment
- Explanation rendering
- Alternative options

### Visualizations (`frontend/components/visualizations.py`)
- Plotly charts
- Interactive graphs
- Tire degradation curves
- Fuel consumption plots
- Lap performance trends
- Pit strategy timelines

## 🐛 Troubleshooting

### Common Issues

**Dashboard won't start**
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall Streamlit
pip install --upgrade streamlit
```

**Import errors**
```bash
# Ensure you're in project root
cd ai-race-engineer-copilot

# Reinstall dependencies
pip install -r requirements.txt
```

**IBM Granite not working**
- Verify `.env` file exists
- Check API credentials
- Test connection: `python examples/analyze_race.py`
- Dashboard will work in demo mode without credentials

**Visualizations not showing**
```bash
# Reinstall Plotly
pip install --upgrade plotly kaleido
```

**Slow performance**
- Check internet connection (for IBM API)
- Reduce max_tokens in Granite config
- Clear Streamlit cache: `streamlit cache clear`

## 📱 Responsive Design

The dashboard is optimized for:
- **Desktop**: Full feature set (recommended)
- **Tablet**: Responsive layout
- **Mobile**: Basic functionality (limited)

Recommended minimum resolution: 1280x720

## 🚀 Performance Tips

1. **Caching**: Streamlit caches AI responses
2. **Batch Updates**: Update multiple inputs before analyzing
3. **Network**: Stable internet for IBM API calls
4. **Browser**: Use Chrome or Firefox for best performance

## 🔐 Security

- API keys stored in `.env` (not committed to git)
- No sensitive data in frontend code
- XSRF protection enabled
- Secure API communication

## 📚 Documentation

- [Frontend Setup Guide](frontend_setup.md)
- [Langflow Integration](../workflows/langflow_setup.md)
- [Architecture Overview](architecture.md)
- [IBM Granite Integration](granite_integration.md)

## 🤝 Contributing

To contribute to the frontend:

1. Follow the existing component structure
2. Maintain the racing theme aesthetic
3. Add comments for complex logic
4. Test with various race scenarios
5. Ensure responsive design

## 📄 License

MIT License - See LICENSE file

## 🏆 Acknowledgments

Built for IBM SkillsBuild AI Builders Challenge

**Technologies Used:**
- Streamlit - Web framework
- IBM Granite - AI reasoning
- Plotly - Visualizations
- Python - Backend logic

---

**Ready to race? Start the dashboard and experience AI-powered race strategy! 🏎️💨**