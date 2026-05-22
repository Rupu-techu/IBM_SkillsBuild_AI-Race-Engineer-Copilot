# Contributing to AI Race Engineer Copilot

Thank you for your interest in contributing to the **AI Race Engineer Copilot** project! 🏎️

This project was built for the IBM SkillsBuild AI Builders Challenge, and we welcome contributions that enhance its capabilities, improve documentation, or extend its applications.

---

## 🎯 Project Vision

Build an **intelligent, explainable AI racing strategy assistant** that demonstrates the power of IBM Granite and watsonx.ai in real-world, high-pressure decision-making scenarios.

### Core Principles

- **Explainability First** — Every AI decision must be transparent and understandable
- **Enterprise Quality** — Production-ready code with proper architecture
- **Racing Authenticity** — Accurate motorsport terminology and logic
- **IBM Technology** — Showcase IBM Granite, watsonx.ai, and Langflow capabilities

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+**
- **Node.js 18+** (for React frontend)
- **Git**
- **IBM watsonx.ai account** (optional for development)

### Setup Development Environment

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/ai-race-engineer-copilot.git
cd ai-race-engineer-copilot

# 2. Create a new branch for your feature
git checkout -b feature/your-feature-name

# 3. Backend setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Frontend setup
cd frontend
npm install
cd ..

# 5. Configure environment (optional)
cp .env.example .env
# Edit .env with your IBM credentials if needed
```

### Running the Development Environment

**Backend (Python):**
```bash
# Run example analysis
python examples/analyze_race.py

# Run tests
pytest tests/
```

**Frontend (React):**
```bash
cd frontend
npm run dev
# Open http://localhost:5173
```

---

## 📁 Project Structure

```
ai-race-engineer-copilot/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── data/            # Mock data and utilities
│   │   └── App.jsx          # Main app component
│   ├── package.json
│   └── vite.config.js
├── src/                     # Python backend
│   ├── ai/                  # IBM Granite integration
│   │   ├── granite_engine.py
│   │   └── watsonx_config.py
│   ├── core/                # Core race analysis
│   │   └── race_analyzer.py
│   └── utils/               # Utilities
├── workflows/               # Langflow workflows
│   ├── langflow_client.py
│   └── langflow_setup.md
├── docs/                    # Documentation
├── examples/                # Example scripts
├── tests/                   # Test suite
└── data/                    # Sample race data
```

---

## 🛠️ Development Guidelines

### Code Style

#### Python Code
- Follow **PEP 8** style guide
- Use **type hints** for all function parameters and returns
- Add **docstrings** for all classes and functions
- Keep functions **focused and modular** (single responsibility)
- Use **meaningful variable names**

**Example:**
```python
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class RaceConditions:
    """
    Represents current race conditions for strategy analysis.
    
    Attributes:
        lap_number: Current lap number
        tire_wear: Tire wear percentage (0-100)
        fuel_level: Remaining fuel percentage (0-100)
    """
    lap_number: int
    tire_wear: float
    fuel_level: float

def analyze_strategy(
    conditions: RaceConditions,
    use_ai: bool = True
) -> Dict[str, any]:
    """
    Analyze race conditions and generate strategy recommendation.
    
    Args:
        conditions: Current race conditions
        use_ai: Whether to use IBM Granite for explanation
        
    Returns:
        Dictionary containing action, confidence, and reasoning
        
    Raises:
        ValueError: If conditions are invalid
    """
    # Implementation
    pass
```

#### React/JavaScript Code
- Use **functional components** with hooks
- Follow **React best practices**
- Use **TailwindCSS** for styling
- Add **PropTypes** or TypeScript types
- Keep components **small and reusable**

**Example:**
```jsx
import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

/**
 * TelemetryCard - Displays real-time telemetry data
 * @param {Object} props - Component props
 * @param {Object} props.data - Telemetry data object
 * @param {Function} props.onUpdate - Callback for data updates
 */
export default function TelemetryCard({ data, onUpdate }) {
  const [isLoading, setIsLoading] = useState(false);
  
  useEffect(() => {
    // Effect logic
  }, [data]);
  
  return (
    <div className="bg-gray-900 rounded-lg p-6">
      {/* Component content */}
    </div>
  );
}

TelemetryCard.propTypes = {
  data: PropTypes.object.isRequired,
  onUpdate: PropTypes.func
};
```

### Testing

#### Python Tests
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_race_analyzer.py

# Run with verbose output
pytest -v tests/
```

#### Frontend Tests
```bash
cd frontend
npm test
```

### Commit Messages

Use clear, descriptive commit messages following this format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(ai): add multi-stop strategy analysis to Granite engine

Implemented new method for analyzing optimal multi-stop strategies
using IBM Granite AI. Includes confidence scoring and risk assessment.

Closes #42

---

fix(frontend): resolve tire wear chart rendering issue

Fixed bug where tire wear chart would not update after strategy
recommendation. Added proper state management.

---

docs(readme): update IBM technology integration section

Added detailed explanation of how Langflow orchestrates the AI
workflow pipeline.
```

---

## 🎨 UI/UX Guidelines

### Design System

**Color Palette:**
```css
/* Primary Colors */
--bg-primary: #0a0a0a;      /* Main background */
--bg-secondary: #1a1a1a;    /* Card background */
--bg-tertiary: #2a2a2a;     /* Elevated elements */

/* Accent Colors */
--accent-red: #e63946;      /* Critical/Danger */
--accent-orange: #f77f00;   /* Warning */
--accent-yellow: #ffd60a;   /* Caution */
--accent-green: #06ffa5;    /* Success/Optimal */
--accent-blue: #0096ff;     /* Info */

/* Text Colors */
--text-primary: #ffffff;
--text-secondary: #a0a0a0;
--text-muted: #666666;
```

**Typography:**
- **Headings:** Inter, system-ui
- **Body:** Inter, system-ui
- **Monospace:** 'Courier New', monospace (for telemetry data)

**Spacing Scale:**
- `xs`: 4px
- `sm`: 8px
- `md`: 16px
- `lg`: 24px
- `xl`: 32px
- `2xl`: 48px

### Component Guidelines

1. **Consistency** — Use existing components as templates
2. **Responsiveness** — Test on desktop and tablet
3. **Accessibility** — Include ARIA labels and keyboard navigation
4. **Loading States** — Show loading indicators for async operations
5. **Error Handling** — Display clear, helpful error messages
6. **Animations** — Use Framer Motion for smooth transitions

---

## 🤖 AI Integration Guidelines

### Working with IBM Granite

```python
from src.ai.granite_engine import GraniteEngine

# Initialize engine
engine = GraniteEngine()

# Generate explanation
explanation = engine.explain_decision(
    recommendation={
        "action": "pit_now",
        "confidence": 0.92,
        "risk_level": "high"
    },
    race_conditions={
        "lap": 28,
        "tire_wear": 87.5,
        "position": 3
    }
)

print(explanation)
# Output: "Pit now because tire degradation is critical..."
```

### Adding New AI Features

1. **Extend GraniteEngine** — Add new methods to [`src/ai/granite_engine.py`](src/ai/granite_engine.py)
2. **Create Prompts** — Design clear, structured prompts for Granite
3. **Handle Fallbacks** — Implement graceful degradation without API access
4. **Test Thoroughly** — Test with and without IBM credentials
5. **Document Usage** — Add examples and docstrings

### Prompt Engineering Best Practices

```python
def create_strategy_prompt(conditions: Dict) -> str:
    """
    Create a well-structured prompt for IBM Granite.
    
    Best practices:
    - Clear role definition
    - Structured input format
    - Specific output requirements
    - Context and constraints
    """
    return f"""You are an expert AI Race Engineer analyzing a Formula 1 race.

Race Conditions:
- Lap: {conditions['lap']}/{conditions['total_laps']}
- Tire Wear: {conditions['tire_wear']}%
- Position: P{conditions['position']}
- Fuel: {conditions['fuel']}%

Task: Recommend the optimal strategy considering:
1. Tire degradation and remaining life
2. Fuel consumption and finish viability
3. Competitive positioning
4. Risk vs. reward analysis

Provide:
- Primary recommendation (pit_now/pit_next_lap/stay_out)
- Confidence level (0-100%)
- Clear reasoning with data support
- Expected outcome

Recommendation:"""
```

---

## 📊 Adding Race Scenarios

Create JSON files in [`data/sample_races/`](data/sample_races/):

```json
{
  "race_name": "Monaco Grand Prix 2024",
  "circuit": "Circuit de Monaco",
  "total_laps": 78,
  "weather": "dry",
  "scenarios": [
    {
      "lap": 35,
      "description": "Critical tire wear situation",
      "conditions": {
        "lap_number": 35,
        "total_laps": 78,
        "tire_wear": 88.5,
        "tire_compound": "soft",
        "tire_age": 22,
        "weather": "dry",
        "track_temp": 48.0,
        "air_temp": 26.0,
        "position": 4,
        "fuel_level": 58.0,
        "gap_to_leader": 18.3,
        "gap_to_behind": 3.7,
        "track_conditions": "green"
      },
      "expected_recommendation": "pit_now",
      "reasoning": "Tire degradation critical, undercut opportunity"
    }
  ]
}
```

---

## 🐛 Bug Reports

### Before Reporting

1. **Search existing issues** — Check if already reported
2. **Try latest version** — Update to latest code
3. **Reproduce consistently** — Ensure bug is reproducible
4. **Gather information** — Collect logs and screenshots

### Bug Report Template

```markdown
## Bug Description
Clear and concise description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Enter data '...'
4. See error

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Screenshots
If applicable, add screenshots.

## Environment
- OS: [e.g., Windows 11, macOS 13, Ubuntu 22.04]
- Python Version: [e.g., 3.9.7]
- Node Version: [e.g., 18.17.0]
- Browser: [e.g., Chrome 120, Firefox 121]

## Additional Context
Any other relevant information.

## Possible Solution
(Optional) Suggest a fix if you have one.
```

---

## 🎯 Feature Requests

### Feature Request Template

```markdown
## Feature Description
Clear description of the proposed feature.

## Problem It Solves
What problem does this feature address?

## Proposed Solution
How should this feature work?

## Alternative Solutions
Other approaches you've considered.

## Use Cases
Real-world scenarios where this would be useful.

## Implementation Suggestions
(Optional) Technical approach or code examples.

## Additional Context
Mockups, diagrams, or related features.
```

---

## 🔄 Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

### PR Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Related Issues
Closes #(issue number)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
How was this tested?
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Screenshots
(If applicable)

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No new warnings
```

### Review Process

1. **Automated Checks** — CI/CD runs tests and linting
2. **Code Review** — Maintainer reviews code quality
3. **Testing** — Reviewer tests functionality
4. **Feedback** — Address review comments
5. **Approval** — Maintainer approves and merges

---

## 📝 Documentation

### Documentation Standards

- **Keep README.md updated** — Reflect new features
- **Update relevant docs** — Architecture, setup guides, etc.
- **Add inline comments** — Explain complex logic
- **Include examples** — Show how to use new features
- **Use clear language** — Avoid jargon when possible

### Documentation Structure

```
docs/
├── architecture.md          # System architecture
├── FRONTEND_README.md       # Frontend documentation
├── DEPLOYMENT.md            # Deployment guide
├── PRESENTATION_GUIDE.md    # Hackathon presentation
└── images/                  # Screenshots and diagrams
```

---

## 🏆 Recognition

Contributors will be recognized in:
- **README.md** — Contributors section
- **Release Notes** — Feature attribution
- **Project Credits** — Acknowledgments

---

## 📧 Communication

- **GitHub Issues** — Bug reports and feature requests
- **GitHub Discussions** — General questions and ideas
- **Pull Requests** — Code contributions and reviews

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the **MIT License**.

---

## 🎓 Learning Resources

### IBM Technologies
- [IBM Granite Documentation](https://www.ibm.com/granite)
- [watsonx.ai Platform Guide](https://www.ibm.com/watsonx)
- [Langflow Documentation](https://docs.langflow.org)

### Racing Strategy
- FIA Technical Regulations
- F1 Strategy Analysis Articles
- Motorsport Engineering Resources

### Development
- [React Documentation](https://react.dev)
- [TailwindCSS Docs](https://tailwindcss.com)
- [Python Best Practices](https://docs.python-guide.org)

---

## 🙏 Thank You

Thank you for contributing to **AI Race Engineer Copilot**! Your contributions help demonstrate the power of explainable AI in real-world applications.

Together, we're building an intelligent, transparent racing strategy assistant that showcases IBM's cutting-edge AI technologies.

---

<div align="center">

**Built with ❤️ for the IBM SkillsBuild AI Builders Challenge**

🏎️ **AI Race Engineer Copilot** — *Making Racing Strategy Intelligent and Transparent*

**[⭐ Star the Project](https://github.com/yourusername/ai-race-engineer-copilot)** • **[📖 Read Docs](docs/)** • **[🚀 Try Demo](#)**

</div>