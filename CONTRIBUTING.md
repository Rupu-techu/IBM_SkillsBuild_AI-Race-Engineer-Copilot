# Contributing to AI Race Engineer Copilot

Thank you for your interest in contributing to the AI Race Engineer Copilot project!

## 🎯 Project Vision

Build an intelligent, explainable AI racing strategy assistant that demonstrates the power of IBM Granite and watsonx.ai in real-world decision-making scenarios.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Git
- IBM watsonx.ai account (optional for development)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-race-engineer-copilot.git
cd ai-race-engineer-copilot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your credentials (optional for demo mode)

# Run the dashboard
streamlit run frontend/app.py
```

## 📁 Project Structure

```
ai-race-engineer-copilot/
├── frontend/              # Streamlit dashboard
│   ├── app.py            # Main application
│   ├── components/       # UI components
│   ├── styles/           # CSS and animations
│   └── utils/            # Helper functions
├── src/                  # Core logic
│   ├── ai/              # IBM Granite integration
│   ├── core/            # Race analysis engine
│   └── utils/           # Utilities
├── workflows/           # Langflow workflows
├── docs/                # Documentation
├── examples/            # Example scripts
└── tests/               # Test suite
```

## 🛠️ Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use type hints for function parameters and returns
- Add docstrings for all functions and classes
- Keep functions focused and modular

Example:
```python
def analyze_strategy(race_conditions: Dict) -> StrategyRecommendation:
    """
    Analyze race conditions and generate strategy recommendation
    
    Args:
        race_conditions: Current race conditions dictionary
        
    Returns:
        StrategyRecommendation with action and reasoning
    """
    # Implementation
    pass
```

### Component Development

When creating new frontend components:

1. Place in `frontend/components/`
2. Import required dependencies
3. Use Streamlit best practices
4. Add inline documentation
5. Test with different scenarios

Example component structure:
```python
"""
Component Name
Brief description of what this component does
"""

import streamlit as st
from typing import Dict

def render_component(data: Dict):
    """
    Render the component
    
    Args:
        data: Component data
    """
    st.markdown("## Component Title")
    # Implementation
```

### Adding New Features

1. **Create a branch**: `git checkout -b feature/your-feature-name`
2. **Implement the feature**: Follow coding standards
3. **Test thoroughly**: Ensure it works in different scenarios
4. **Document**: Update relevant documentation
5. **Submit PR**: Create a pull request with clear description

### Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Test specific module
pytest tests/test_race_analyzer.py
```

## 🎨 UI/UX Guidelines

### Design Principles
- **F1-Inspired**: Racing aesthetics with professional feel
- **Dark Theme**: Primary background #0a0a0a
- **Accent Colors**: Red (#e63946), Orange (#f77f00), Yellow (#ffd60a), Green (#06ffa5)
- **Typography**: Monospace fonts for technical data
- **Animations**: Smooth, purposeful, not distracting

### Component Guidelines
- Use consistent spacing (10px, 15px, 20px)
- Add loading states for async operations
- Provide clear error messages
- Include helpful tooltips
- Ensure responsive design

## 🤖 AI Integration

### Working with IBM Granite

```python
from src.ai.granite_engine import GraniteEngine

# Initialize engine
engine = GraniteEngine()

# Generate explanation
explanation = engine.explain_decision(
    recommendation=recommendation_dict,
    race_conditions=conditions_dict
)
```

### Adding New AI Features

1. Extend `GraniteEngine` class
2. Add appropriate prompts
3. Handle fallback cases
4. Test with and without API access
5. Document the feature

## 📊 Data and Scenarios

### Adding Race Scenarios

Create JSON files in `data/sample_races/`:

```json
{
  "race_name": "Your Race Name",
  "circuit": "Circuit Name",
  "total_laps": 50,
  "scenarios": [
    {
      "lap": 25,
      "description": "Scenario description",
      "conditions": {
        "lap_number": 25,
        "tire_wear": 78,
        // ... other conditions
      }
    }
  ]
}
```

## 📝 Documentation

### Documentation Standards

- Keep README.md updated
- Document new features in relevant docs
- Add inline comments for complex logic
- Update API documentation
- Include usage examples

### Documentation Structure

- `README.md`: Project overview
- `QUICKSTART.md`: Quick start guide
- `docs/`: Detailed documentation
  - `architecture.md`: System architecture
  - `frontend_setup.md`: Frontend guide
  - `DEPLOYMENT.md`: Deployment instructions
  - `PRESENTATION_GUIDE.md`: Hackathon presentation

## 🐛 Bug Reports

### Reporting Bugs

1. Check existing issues first
2. Use issue template
3. Provide clear reproduction steps
4. Include system information
5. Add screenshots if applicable

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. ...

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 11]
- Python: [e.g., 3.9.7]
- Browser: [e.g., Chrome 120]

**Screenshots**
If applicable
```

## 🎯 Feature Requests

### Requesting Features

1. Check if feature already exists
2. Describe the use case
3. Explain the benefit
4. Suggest implementation approach

## 🔄 Pull Request Process

### PR Guidelines

1. **Branch naming**: `feature/name`, `fix/name`, `docs/name`
2. **Commit messages**: Clear, descriptive, present tense
3. **PR description**: Explain what and why
4. **Tests**: Include tests for new features
5. **Documentation**: Update relevant docs

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
How was this tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
```

## 🏆 Recognition

Contributors will be recognized in:
- Project README
- Release notes
- Contributor list

## 📧 Contact

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: [your-email@example.com]

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to AI Race Engineer Copilot! 🏎️💨**