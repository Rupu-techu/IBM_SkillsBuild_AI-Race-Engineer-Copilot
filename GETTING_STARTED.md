# Getting Started with AI Race Engineer Copilot

## 🚀 Quick Start Guide

This guide will help you set up and run the AI Race Engineer Copilot in under 10 minutes.

## Prerequisites

Before you begin, ensure you have:
- ✅ Python 3.9 or higher installed
- ✅ Git installed
- ✅ IBM Cloud account (free tier available)
- ✅ Text editor or IDE (VS Code recommended)

## Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-race-engineer-copilot.git

# Navigate to project directory
cd ai-race-engineer-copilot
```

## Step 2: Set Up Python Environment

### On Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip
```

### On macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

## Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**Note**: This may take 2-3 minutes depending on your internet connection.

## Step 4: Set Up IBM watsonx.ai Credentials

### 4.1 Create IBM Cloud Account
1. Visit [cloud.ibm.com](https://cloud.ibm.com)
2. Click "Create an account" (free tier available)
3. Complete registration and verify email

### 4.2 Set Up watsonx.ai
1. Log in to IBM Cloud Console
2. Go to **Catalog** → **AI / Machine Learning**
3. Select **watsonx.ai**
4. Click **Create** (choose Lite/Free plan for testing)
5. Wait for provisioning (1-2 minutes)

### 4.3 Get API Credentials
1. Go to your watsonx.ai instance
2. Click **Manage** → **Access (IAM)**
3. Click **API keys** → **Create**
4. Name it: `race-engineer-copilot`
5. **Copy the API key immediately** (you won't see it again!)

### 4.4 Get Project ID
1. In watsonx.ai, go to **Projects**
2. Create a new project or select existing
3. Copy the **Project ID** from the URL or settings

### 4.5 Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your credentials
# On Windows: notepad .env
# On macOS/Linux: nano .env
```

Add your credentials to `.env`:
```env
IBM_WATSONX_API_KEY=your_actual_api_key_here
IBM_WATSONX_PROJECT_ID=your_actual_project_id_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
GRANITE_MODEL_ID=ibm/granite-13b-chat-v2
```

**Important**: Never commit the `.env` file to Git!

## Step 5: Test Your Setup

### 5.1 Test IBM Granite Connection
```bash
python -c "from src.ai.granite_engine import GraniteEngine; engine = GraniteEngine(); print('✓ Connection successful!')"
```

**Expected Output**:
```
✓ IBM Granite engine initialized: ibm/granite-13b-chat-v2
✓ Connection successful!
```

### 5.2 Run the Demo
```bash
python examples/analyze_race.py
```

**Expected Output**: You'll see 4 race scenarios analyzed with AI recommendations and explanations.

## Step 6: Explore the Project

### Project Structure
```
ai-race-engineer-copilot/
├── src/                    # Source code
│   ├── core/              # Race analysis engine
│   └── ai/                # IBM Granite integration
├── examples/              # Demo scripts
├── data/                  # Sample race data
├── docs/                  # Documentation
└── tests/                 # Test files
```

### Key Files to Explore

1. **[`src/core/race_analyzer.py`](src/core/race_analyzer.py)**
   - Core race analysis logic
   - Strategy recommendation engine
   - Tire and fuel management

2. **[`src/ai/granite_engine.py`](src/ai/granite_engine.py)**
   - IBM Granite integration
   - Explainable AI reasoning
   - Scenario analysis

3. **[`examples/analyze_race.py`](examples/analyze_race.py)**
   - Demo script with 4 scenarios
   - Shows complete workflow
   - Interactive examples

4. **[`docs/architecture.md`](docs/architecture.md)**
   - System architecture overview
   - Component descriptions
   - Design patterns

## Step 7: Try Different Scenarios

### Scenario 1: Critical Tire Degradation
```python
from src.core.race_analyzer import RaceAnalyzer, RaceConditions, TireCompound, WeatherCondition

conditions = RaceConditions(
    lap_number=28,
    total_laps=50,
    tire_wear=87.5,
    tire_compound=TireCompound.MEDIUM,
    tire_age=18,
    weather=WeatherCondition.DRY,
    track_temp=45.0,
    air_temp=28.0,
    position=3,
    fuel_level=62.0,
    gap_to_leader=12.3,
    gap_to_behind=4.8,
    track_conditions="green"
)

analyzer = RaceAnalyzer()
recommendation = analyzer.analyze_strategy(conditions)

print(f"Action: {recommendation.action.value}")
print(f"Reasoning: {recommendation.reasoning}")
```

### Scenario 2: Weather Change
```python
conditions = RaceConditions(
    lap_number=15,
    total_laps=50,
    tire_wear=45.0,
    tire_compound=TireCompound.SOFT,
    tire_age=8,
    weather=WeatherCondition.LIGHT_RAIN,  # Rain approaching!
    track_temp=32.0,
    air_temp=22.0,
    position=5,
    fuel_level=78.0,
    gap_to_leader=18.5,
    gap_to_behind=2.1,
    track_conditions="green"
)

recommendation = analyzer.analyze_strategy(conditions)
print(f"Weather Strategy: {recommendation.action.value}")
print(f"Tire Recommendation: {recommendation.tire_recommendation.value}")
```

## Step 8: Run Tests

```bash
# Install test dependencies (if not already installed)
pip install pytest pytest-cov

# Run all tests
pytest tests/

# Run with coverage report
pytest --cov=src tests/

# Run specific test file
pytest tests/test_race_analyzer.py -v
```

## Common Issues & Solutions

### Issue 1: Import Errors
**Error**: `ModuleNotFoundError: No module named 'src'`

**Solution**:
```bash
# Make sure you're in the project root directory
cd ai-race-engineer-copilot

# Ensure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 2: IBM Credentials Error
**Error**: `Invalid API key` or `Project not found`

**Solution**:
1. Verify credentials in `.env` file
2. Check for extra spaces or quotes
3. Ensure API key is active in IBM Cloud
4. Verify project ID is correct
5. Check regional URL matches your instance

### Issue 3: Python Version
**Error**: `Python 3.9 or higher required`

**Solution**:
```bash
# Check Python version
python --version

# If version is too old, install Python 3.9+
# Download from: https://www.python.org/downloads/
```

### Issue 4: Permission Errors (Windows)
**Error**: `Access denied` when activating venv

**Solution**:
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate venv
venv\Scripts\activate
```

## Next Steps

### 1. Explore Documentation
- 📖 [Architecture Overview](docs/architecture.md)
- 🔧 [IBM Granite Integration Guide](docs/granite_integration.md)
- 🗺️ [Development Roadmap](docs/development_roadmap.md)

### 2. Customize the System
- Modify tire degradation thresholds
- Add new strategy types
- Create custom race scenarios
- Adjust AI prompt templates

### 3. Extend Functionality
- Add API endpoints (FastAPI)
- Create Langflow workflows
- Build web dashboard
- Integrate real telemetry data

### 4. Contribute
- Report issues on GitHub
- Submit pull requests
- Share your improvements
- Help with documentation

## Learning Resources

### IBM Technologies
- [IBM Granite Models](https://www.ibm.com/granite)
- [watsonx.ai Documentation](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [IBM Cloud Getting Started](https://cloud.ibm.com/docs)

### Racing Strategy
- Formula 1 strategy basics
- Tire compound characteristics
- Weather impact on racing
- Pit stop optimization

### Python & AI
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Langchain Documentation](https://python.langchain.com/)
- [Pydantic Guide](https://docs.pydantic.dev/)

## Getting Help

### Support Channels
1. **GitHub Issues**: Report bugs or request features
2. **IBM Developer Community**: Ask IBM-specific questions
3. **Documentation**: Check docs/ folder for guides
4. **Stack Overflow**: Tag questions with `ibm-watsonx`

### Useful Commands

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Deactivate virtual environment
deactivate

# Update dependencies
pip install --upgrade -r requirements.txt

# Run specific example
python examples/analyze_race.py

# Check code style
black src/ --check
flake8 src/

# Run type checking
mypy src/
```

## Project Status

✅ **Completed**:
- Core race analysis engine
- IBM Granite integration
- Explainable AI reasoning
- Sample race scenarios
- Comprehensive documentation

🚧 **In Progress**:
- Langflow workflow design
- API endpoints

📋 **Planned**:
- Web dashboard
- Real-time telemetry integration
- Advanced ML models

## Success Checklist

Before proceeding, ensure:
- ✅ Virtual environment activated
- ✅ Dependencies installed
- ✅ IBM credentials configured
- ✅ Demo script runs successfully
- ✅ Tests pass
- ✅ Documentation reviewed

## Ready to Build!

You're now ready to start building with the AI Race Engineer Copilot! 

**Recommended First Steps**:
1. Run the demo script to see it in action
2. Read the architecture documentation
3. Experiment with different race scenarios
4. Explore the IBM Granite integration
5. Start building your own features

---

**Need Help?** Check the [documentation](docs/) or open an issue on GitHub.

**Happy Racing!** 🏎️🏁