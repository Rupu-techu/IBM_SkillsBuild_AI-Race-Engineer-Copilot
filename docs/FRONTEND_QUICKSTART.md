# Frontend Quick Start Guide

## Running the AI Race Engineer Copilot

### Prerequisites

Ensure you have Python 3.8+ installed and all dependencies from `requirements.txt`.

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables (optional for demo mode)
cp .env.example .env
# Edit .env with your IBM watsonx.ai credentials
```

### Running the Application

#### Option 1: Direct Streamlit Command
```bash
streamlit run frontend/app.py
```

#### Option 2: Using the Run Script
```bash
python examples/run_dashboard.py
```

### Accessing the Dashboard

Once running, open your browser to:
```
http://localhost:8501
```

---

## Features Overview

### 1. **Sidebar Controls** (Left)
- **Simulation Controls**: Start/Pause/Reset race simulation
- **Race Info**: Current lap, progress, status
- **Weather**: Track conditions and temperatures
- **Tire Strategy**: Compound selection and wear monitoring
- **Fuel Management**: Current fuel level
- **Analyze Button**: Trigger AI strategy analysis

### 2. **AI Strategy Recommendation** (Top Center)
- Large hero card with AI recommendation
- Confidence score with visual bar
- Risk level indicator
- Detailed reasoning bullets
- Expected outcome
- Alternative strategies (expandable)

### 3. **Live Telemetry** (Middle Left)
- Race progress bar
- Key metrics: Position, Tire Wear, Fuel, Temperature
- Tire status card with detailed info
- Weather & track conditions
- Competitive position (gaps to leader/behind)

### 4. **AI Commentary Feed** (Middle Right)
- Live race engineer radio messages
- Color-coded by message type:
  - 🚨 Critical (red)
  - 🎯 Overtake (orange)
  - 🔧 Pit (yellow)
  - 📊 Strategy (green)
  - 📻 Normal (green)
- Generate Commentary button

### 5. **Strategy Analytics** (Bottom)
Four interactive charts in tabs:
- **Tire Degradation**: Historical and projected wear
- **Fuel Analysis**: Consumption rate and projection
- **Lap Performance**: Lap time evolution
- **Pit Strategy**: Optimal pit windows

---

## Demo Mode

The application works in demo mode without IBM credentials:

1. **Fallback AI**: Uses rule-based strategy recommendations
2. **Sample Data**: Pre-configured race scenarios
3. **Full UI**: All visual features work perfectly

### Demo Scenarios

Use the sidebar controls to simulate different race situations:
- **Critical Tire Wear**: Set tire wear > 85%
- **Fuel Critical**: Set fuel level < 20%
- **Weather Change**: Select rain conditions
- **Safety Car**: Change track conditions
- **Optimal Strategy**: Balanced conditions

---

## Simulation Mode

### Starting Simulation
1. Click **▶️ START** in the sidebar
2. Watch telemetry update automatically
3. Observe AI commentary generation
4. Monitor strategy recommendations

### Simulation Features
- **Auto-advance**: Laps progress every 3 seconds
- **Dynamic Events**: Random race events (safety car, weather, etc.)
- **Tire Degradation**: Exponential wear model
- **Fuel Consumption**: Realistic fuel usage
- **Gap Changes**: Dynamic position changes
- **Commentary**: Automatic radio messages

### Controls
- **▶️ START**: Begin simulation
- **⏸️ PAUSE**: Pause simulation
- **🔄 RESET**: Reset to initial state

---

## Customization

### Adjusting Race Conditions

**In Sidebar**:
- Current Lap: 1-100
- Total Laps: 1-100
- Position: 1-20
- Tire Compound: Soft/Medium/Hard/Intermediate/Wet
- Tire Wear: 0-100%
- Tire Age: 0-50 laps
- Fuel Level: 0-100%
- Weather: Dry/Light Rain/Heavy Rain/Mixed
- Track Temperature: 20-60°C
- Air Temperature: 15-40°C
- Gap to Leader: 0-120s
- Gap Behind: 0-120s
- Track Conditions: Green/Yellow/Safety Car

### Triggering AI Analysis

1. Adjust race conditions in sidebar
2. Click **🤖 ANALYZE STRATEGY**
3. View AI recommendation in main panel
4. Check detailed analysis in expandable sections

---

## Keyboard Shortcuts

- **Ctrl/Cmd + R**: Refresh page
- **Ctrl/Cmd + Shift + R**: Hard refresh (clear cache)
- **F11**: Fullscreen mode

---

## Troubleshooting

### Application Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Clear Streamlit cache
streamlit cache clear
```

### Styling Issues
```bash
# Hard refresh browser (Ctrl+Shift+R)
# Clear browser cache
# Check CSS files exist in frontend/styles/
```

### IBM Granite Not Working
- Application works in demo mode without credentials
- Check `.env` file for correct API keys
- Verify IBM watsonx.ai access
- Review error messages in terminal

### Slow Performance
- Close other browser tabs
- Reduce simulation speed (modify `update_simulation()`)
- Disable browser extensions
- Check system resources

---

## Best Practices

### For Presentations
1. **Start in Demo Mode**: No credentials needed
2. **Use Simulation**: Shows live updates
3. **Highlight AI Features**: Expandable sections
4. **Show Different Scenarios**: Adjust conditions
5. **Fullscreen Mode**: F11 for immersive view

### For Development
1. **Hot Reload**: Streamlit auto-reloads on file changes
2. **Debug Mode**: Check terminal for errors
3. **Session State**: Use `st.session_state` for data
4. **Component Testing**: Test individual components
5. **CSS Changes**: Hard refresh to see updates

### For Production
1. **Set Environment Variables**: Use `.env` file
2. **Enable Caching**: Optimize performance
3. **Monitor Logs**: Check for errors
4. **Test Thoroughly**: All features and scenarios
5. **Secure Credentials**: Never commit `.env`

---

## Advanced Features

### Custom Scenarios
Edit `frontend/utils/simulation.py` to add custom race scenarios:
```python
scenarios = {
    "my_scenario": {
        "name": "My Custom Scenario",
        "description": "Description here",
        "conditions": {
            "lap_number": 25,
            "total_laps": 50,
            # ... other conditions
        }
    }
}
```

### Custom Commentary
Modify `frontend/components/ai_commentary.py` to customize AI messages:
```python
def _generate_fallback_commentary(self, race_conditions, event_type):
    # Add custom logic here
    return "Your custom message"
```

### Custom Styling
Edit `frontend/styles/f1_professional.css` to adjust colors and styles:
```css
:root {
    --accent-red: #your-color;
    --accent-orange: #your-color;
    /* ... other variables */
}
```

---

## Performance Tips

1. **Limit Chart Data**: Reduce data points for faster rendering
2. **Optimize Images**: Compress any custom images
3. **Minimize Reruns**: Use `st.cache_data` where appropriate
4. **Lazy Loading**: Load heavy components on demand
5. **Browser Choice**: Chrome/Edge recommended for best performance

---

## Support

### Documentation
- `docs/FRONTEND_IMPROVEMENTS.md` - Detailed improvements
- `docs/architecture.md` - System architecture
- `README.md` - Project overview

### Common Issues
- **Import Errors**: Check Python path and dependencies
- **CSS Not Loading**: Verify file paths in `app.py`
- **Simulation Not Running**: Check `simulation_running` in session state
- **Charts Not Rendering**: Verify Plotly installation

---

## Next Steps

1. **Explore Features**: Try all controls and buttons
2. **Test Scenarios**: Simulate different race conditions
3. **Customize**: Adjust colors, messages, scenarios
4. **Integrate**: Connect to real F1 data APIs
5. **Deploy**: Host on Streamlit Cloud or other platforms

---

**Enjoy your professional F1 race strategy command center!** 🏎️

For questions or issues, refer to the documentation or check the project repository.