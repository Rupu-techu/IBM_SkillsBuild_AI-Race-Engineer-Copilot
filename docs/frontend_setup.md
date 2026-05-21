# Frontend Setup Guide

## Overview

This guide explains how to set up and run the AI Race Engineer Copilot frontend dashboard built with Streamlit.

## Prerequisites

- Python 3.9 or higher
- IBM watsonx.ai credentials
- All backend components installed

## Installation

### 1. Install Dependencies

```bash
# Install all requirements including frontend dependencies
pip install -r requirements.txt
```

Key frontend dependencies:
- `streamlit==1.29.0` - Web application framework
- `plotly==5.18.0` - Interactive visualizations
- `kaleido==0.2.1` - Static image export for Plotly

### 2. Environment Configuration

Ensure your `.env` file contains the required credentials:

```env
# IBM watsonx.ai Configuration
IBM_WATSONX_API_KEY=your_api_key_here
IBM_WATSONX_PROJECT_ID=your_project_id_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
GRANITE_MODEL_ID=ibm/granite-13b-chat-v2

# Langflow Configuration (optional)
LANGFLOW_URL=http://localhost:7860
```

## Running the Dashboard

### Quick Start

```bash
# Navigate to project root
cd ai-race-engineer-copilot

# Run the Streamlit app
streamlit run frontend/app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

### Custom Configuration

```bash
# Run on a different port
streamlit run frontend/app.py --server.port 8080

# Run with custom theme
streamlit run frontend/app.py --theme.base dark

# Run without auto-opening browser
streamlit run frontend/app.py --server.headless true
```

## Dashboard Features

### 1. Sidebar Controls

The sidebar provides comprehensive race condition inputs:

**Race Progress**
- Current lap number
- Total laps in race
- Current position

**Tire Status**
- Tire compound selection (soft/medium/hard/intermediate/wet)
- Tire wear percentage (0-100%)
- Tire age in laps
- Visual status indicators

**Fuel Management**
- Fuel level percentage
- Visual fuel status indicators

**Weather Conditions**
- Weather selection (dry/light rain/heavy rain/mixed)
- Track temperature
- Air temperature

**Competitive Position**
- Gap to race leader
- Gap to car behind

**Track Status**
- Track conditions (green/yellow/safety car)
- Visual flag indicators

**Driver Mode**
- Aggression level (Conservative/Balanced/Aggressive)

### 2. Live Telemetry Panel

Real-time display of race data:

- **Race Progress Bar**: Visual representation of race completion
- **Key Metrics**: Position, tire wear, fuel level, track temperature
- **Tire Information Card**: Detailed tire status with color-coded indicators
- **Weather Data Card**: Current weather and track conditions
- **Competitive Position**: Visual gaps to leader and car behind
- **Race Situation Summary**: Phase analysis and remaining resources

### 3. AI Recommendations

IBM Granite-powered strategy recommendations:

- **Primary Recommendation**: Main strategy action with confidence score
- **Risk Assessment**: Risk level analysis (low/medium/high)
- **AI Reasoning**: Explainable AI explanation of the decision
- **Expected Outcome**: Predicted result of the strategy
- **Timing Window**: Optimal execution timing
- **Tire Recommendation**: Suggested tire compound
- **Alternative Strategies**: Other viable options
- **Detailed AI Analysis**: Comprehensive scenario analysis
- **Pit Strategy Options**: Multiple pit stop strategies
- **Overtaking Analysis**: Opportunity assessment (when applicable)

### 4. Race Analytics

Interactive Plotly visualizations:

**Tire Degradation Tab**
- Historical tire wear curve
- Projected future degradation
- Critical threshold indicators
- Optimal pit window visualization
- Tire status metrics

**Fuel Analysis Tab**
- Historical fuel consumption
- Projected fuel levels
- Critical fuel level warnings
- Finish line projection
- Consumption rate metrics

**Lap Performance Tab**
- Lap time evolution
- Average and best lap indicators
- Performance trend analysis
- Current pace metrics

**Pit Strategy Tab**
- Pit window timeline
- Early/optimal/late window visualization
- Current position marker
- Window status analysis
- Pit timing recommendations

## User Workflow

### Basic Usage

1. **Configure Race Conditions**
   - Adjust sidebar inputs to match current race situation
   - Set tire wear, fuel level, weather, etc.

2. **Analyze Strategy**
   - Click "🤖 ANALYZE STRATEGY" button
   - Wait for AI processing (typically 2-5 seconds)

3. **Review Recommendations**
   - Read primary recommendation
   - Check confidence score and risk level
   - Review AI reasoning and explanation

4. **Explore Analytics**
   - Switch between visualization tabs
   - Analyze tire degradation trends
   - Review fuel consumption projections
   - Check pit strategy windows

5. **Consider Alternatives**
   - Expand "Detailed AI Analysis" section
   - Review "Pit Strategy Options"
   - Check "Overtaking Opportunity Analysis" if applicable

### Advanced Usage

**Scenario Testing**
```python
# Test different scenarios by adjusting inputs
# Example: High tire wear scenario
- Set tire wear to 85%
- Set tire age to 18 laps
- Click analyze
- Compare with low wear scenario
```

**Strategy Comparison**
```python
# Compare different driver modes
1. Set conditions
2. Select "Conservative" mode → Analyze
3. Note recommendation
4. Select "Aggressive" mode → Analyze
5. Compare recommendations
```

## Customization

### Theme Customization

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
```

### Component Customization

Edit component files in `frontend/components/`:

- `sidebar.py` - Modify input controls
- `telemetry.py` - Customize telemetry display
- `ai_recommendations.py` - Adjust AI output format
- `visualizations.py` - Modify charts and graphs

## Troubleshooting

### Common Issues

**Issue: Streamlit won't start**
```bash
# Solution: Check if port is in use
netstat -an | grep 8501

# Use different port
streamlit run frontend/app.py --server.port 8080
```

**Issue: IBM Granite connection fails**
```bash
# Solution: Verify credentials
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('IBM_WATSONX_API_KEY'))"

# Check if credentials are loaded
```

**Issue: Visualizations not displaying**
```bash
# Solution: Reinstall Plotly and Kaleido
pip uninstall plotly kaleido
pip install plotly==5.18.0 kaleido==0.2.1
```

**Issue: Import errors**
```bash
# Solution: Ensure you're in the project root
cd ai-race-engineer-copilot

# Verify Python path
python -c "import sys; print(sys.path)"
```

**Issue: Session state errors**
```bash
# Solution: Clear Streamlit cache
streamlit cache clear

# Or restart the app
```

### Performance Optimization

**Slow AI Response**
- Check IBM watsonx.ai API status
- Reduce max_tokens in Granite configuration
- Enable caching for repeated queries

**Slow Visualizations**
- Reduce data points in charts
- Use sampling for large datasets
- Enable Plotly WebGL rendering

**Memory Issues**
- Clear session state periodically
- Limit recommendation history
- Use pagination for large datasets

## Development Mode

### Hot Reload

Streamlit automatically reloads when files change:

```bash
# Run in development mode (default)
streamlit run frontend/app.py

# Disable auto-reload
streamlit run frontend/app.py --server.runOnSave false
```

### Debug Mode

Enable debug logging:

```python
# Add to app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Testing Components

Test individual components:

```bash
# Test sidebar
python -c "from frontend.components.sidebar import render_sidebar; print('Sidebar OK')"

# Test visualizations
python -c "from frontend.components.visualizations import render_visualizations; print('Viz OK')"
```

## Deployment

### Local Network Access

```bash
# Allow network access
streamlit run frontend/app.py --server.address 0.0.0.0
```

### Production Deployment

**Using Streamlit Cloud**
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Configure secrets in Streamlit Cloud dashboard
4. Deploy

**Using Docker**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "frontend/app.py", "--server.address", "0.0.0.0"]
```

**Using Heroku**
```bash
# Create Procfile
echo "web: streamlit run frontend/app.py --server.port $PORT" > Procfile

# Deploy
heroku create ai-race-engineer
git push heroku main
```

## Best Practices

1. **Input Validation**: Always validate user inputs before processing
2. **Error Handling**: Implement graceful error handling for API failures
3. **Caching**: Use `@st.cache_data` for expensive computations
4. **Session State**: Properly manage session state to avoid memory leaks
5. **Responsive Design**: Test on different screen sizes
6. **Performance**: Monitor and optimize slow operations
7. **Security**: Never expose API keys in the frontend code

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [IBM Granite Documentation](https://www.ibm.com/granite)
- [Project GitHub Repository](https://github.com/yourusername/ai-race-engineer-copilot)

## Support

For issues or questions:
1. Check this documentation
2. Review troubleshooting section
3. Check project GitHub issues
4. Contact project maintainers

---

**Built with ❤️ for IBM SkillsBuild AI Builders Challenge**