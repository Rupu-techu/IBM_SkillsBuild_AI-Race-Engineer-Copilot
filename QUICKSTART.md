# 🚀 Quick Start Guide - AI Race Engineer Copilot

Get up and running with the AI Race Engineer Copilot dashboard in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- IBM watsonx.ai account (optional for demo mode)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-race-engineer-copilot.git
cd ai-race-engineer-copilot
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment (Optional)

For full IBM Granite AI functionality:

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your IBM credentials:
# IBM_WATSONX_API_KEY=your_api_key_here
# IBM_WATSONX_PROJECT_ID=your_project_id_here
```

**Note**: The dashboard works in demo mode without IBM credentials!

## Running the Dashboard

### Option 1: Quick Start Script (Recommended)

```bash
python examples/run_dashboard.py
```

### Option 2: Direct Command

```bash
streamlit run frontend/app.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

## Using the Dashboard

### Step 1: Configure Race Conditions

In the sidebar, set:
- **Current Lap**: 25
- **Total Laps**: 50
- **Position**: 3
- **Tire Wear**: 78%
- **Tire Compound**: Medium
- **Fuel Level**: 65%
- **Weather**: Dry

### Step 2: Analyze Strategy

Click the **"🤖 ANALYZE STRATEGY"** button

### Step 3: Review Results

The AI will provide:
- ✅ Primary strategy recommendation
- 📊 Confidence score
- ⚠️ Risk assessment
- 💡 Detailed reasoning
- 🔄 Alternative strategies

### Step 4: Explore Analytics

Switch between tabs to view:
- 🛞 Tire degradation curves
- ⛽ Fuel consumption analysis
- 📈 Lap performance trends
- ⏱️ Pit strategy windows

## Example Scenarios

### Scenario 1: High Tire Wear
```
Lap: 30/50
Tire Wear: 85%
Tire Age: 18 laps
→ Expected: "PIT NOW" recommendation
```

### Scenario 2: Fuel Critical
```
Lap: 40/50
Fuel Level: 15%
→ Expected: "PIT NOW" for fuel
```

### Scenario 3: Optimal Strategy
```
Lap: 25/50
Tire Wear: 60%
Fuel Level: 70%
→ Expected: "STAY OUT" or "PIT NEXT LAP"
```

## Troubleshooting

### Dashboard won't start?
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall Streamlit
pip install --upgrade streamlit
```

### Import errors?
```bash
# Make sure you're in the project root
cd ai-race-engineer-copilot

# Reinstall all dependencies
pip install -r requirements.txt
```

### IBM Granite not working?
- Dashboard works in demo mode without credentials
- Check `.env` file exists and has correct format
- Verify API key is valid in IBM Cloud console

## Next Steps

1. **Explore Features**: Try different race scenarios
2. **Read Documentation**: Check [`docs/FRONTEND_README.md`](docs/FRONTEND_README.md)
3. **Setup Langflow**: Follow [`workflows/langflow_setup.md`](workflows/langflow_setup.md)
4. **Customize**: Modify components in `frontend/components/`

## Getting Help

- 📖 [Full Documentation](docs/)
- 🐛 [Report Issues](https://github.com/yourusername/ai-race-engineer-copilot/issues)
- 💬 [Discussions](https://github.com/yourusername/ai-race-engineer-copilot/discussions)

## Key Features to Try

✅ **Real-time Strategy Analysis** - Get instant AI recommendations  
✅ **Interactive Visualizations** - Explore tire and fuel data  
✅ **Multiple Scenarios** - Test different race conditions  
✅ **Explainable AI** - Understand every recommendation  
✅ **Professional UI** - F1-inspired racing dashboard  

---

**Ready to race? Start the dashboard and experience AI-powered strategy! 🏎️💨**

Built with ❤️ for IBM SkillsBuild AI Builders Challenge