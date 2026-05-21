# Langflow Workflow Setup Guide

## Overview

This guide explains how to set up Langflow workflows for the AI Race Engineer Copilot to orchestrate IBM Granite AI interactions.

## What is Langflow?

Langflow is a visual framework for building AI workflows. It allows you to:
- Design AI pipelines visually
- Connect multiple AI components
- Orchestrate complex reasoning chains
- Test and iterate quickly

## Installation

```bash
# Install Langflow
pip install langflow

# Start Langflow server
langflow run
```

The Langflow UI will open at `http://localhost:7860`

## Workflow Architecture

### 1. Race Strategy Analysis Workflow

**Purpose**: Analyze race conditions and generate strategy recommendations

**Components**:

```
┌─────────────────┐
│  Input Parser   │  ← Race conditions JSON
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Context Builder │  ← Format data for Granite
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  IBM Granite    │  ← Generate strategy
│   AI Model      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Output Parser   │  ← Structure response
└─────────────────┘
```

### 2. Explainability Workflow

**Purpose**: Generate human-readable explanations for AI decisions

**Components**:

```
┌─────────────────┐
│  Recommendation │  ← Strategy decision
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Explanation     │  ← Build explanation prompt
│ Prompt Builder  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  IBM Granite    │  ← Generate explanation
│   AI Model      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Clarity Filter  │  ← Ensure readability
└─────────────────┘
```

## Creating the Workflows

### Step 1: Create Race Strategy Workflow

1. **Open Langflow** at `http://localhost:7860`

2. **Create New Flow**: Click "New Flow"

3. **Add Input Node**:
   - Type: `Text Input`
   - Name: `race_conditions_input`
   - Description: "JSON input with race conditions"

4. **Add Prompt Template Node**:
   - Type: `Prompt Template`
   - Name: `strategy_prompt`
   - Template:
   ```
   You are an expert AI Race Engineer analyzing a Formula 1 race situation.

   Race Conditions:
   {race_conditions}

   Analyze the situation and provide:
   1. Primary strategy recommendation
   2. Confidence level (0-100%)
   3. Risk assessment (low/medium/high)
   4. Expected outcome
   5. Alternative strategies

   Format your response as JSON with these fields:
   - action: string
   - confidence: number
   - risk_level: string
   - reasoning: string
   - expected_outcome: string
   - alternatives: array

   Response:
   ```

5. **Add IBM Granite Model Node**:
   - Type: `LLM` (Language Model)
   - Model: `IBM Granite`
   - Configuration:
     - API Key: `{IBM_WATSONX_API_KEY}`
     - Project ID: `{IBM_WATSONX_PROJECT_ID}`
     - Model ID: `ibm/granite-13b-chat-v2`
     - Temperature: `0.7`
     - Max Tokens: `1024`

6. **Add Output Parser Node**:
   - Type: `JSON Output Parser`
   - Name: `strategy_output`

7. **Connect Nodes**:
   ```
   race_conditions_input → strategy_prompt → IBM Granite → strategy_output
   ```

8. **Save Flow**: Name it `race_strategy_analysis`

### Step 2: Create Explainability Workflow

1. **Create New Flow**: Click "New Flow"

2. **Add Input Nodes**:
   - `recommendation_input` (Text Input)
   - `race_conditions_input` (Text Input)

3. **Add Prompt Template**:
   - Name: `explanation_prompt`
   - Template:
   ```
   You are an expert AI Race Engineer. Explain this strategy decision in clear, professional language.

   Race Conditions:
   {race_conditions}

   Recommended Strategy:
   {recommendation}

   Provide a clear, concise explanation (2-3 sentences) of WHY this strategy is recommended.
   Consider:
   1. Current race situation
   2. Tire and fuel management
   3. Competitive positioning
   4. Risk vs reward

   Explanation:
   ```

4. **Add IBM Granite Model**:
   - Same configuration as Strategy Workflow

5. **Add Text Output Node**:
   - Name: `explanation_output`

6. **Connect Nodes**:
   ```
   recommendation_input ─┐
                         ├→ explanation_prompt → IBM Granite → explanation_output
   race_conditions_input ─┘
   ```

7. **Save Flow**: Name it `strategy_explainability`

### Step 3: Create Multi-Strategy Comparison Workflow

1. **Create New Flow**: Click "New Flow"

2. **Add Components**:
   - Input: `race_conditions_input`
   - Prompt: `comparison_prompt`
   - Model: IBM Granite
   - Output: `comparison_output`

3. **Prompt Template**:
   ```
   Analyze these race conditions and compare THREE different strategy options:

   Race Conditions:
   {race_conditions}

   For each strategy (Conservative, Balanced, Aggressive), provide:
   1. Strategy name
   2. Pit stop timing
   3. Tire selection
   4. Risk level
   5. Expected outcome
   6. Probability of success

   Format as JSON array with these strategies.

   Response:
   ```

4. **Save Flow**: Name it `multi_strategy_comparison`

## Integration with Python

### Using Langflow API

```python
import requests
import json

class LangflowClient:
    """Client for Langflow API integration"""
    
    def __init__(self, base_url="http://localhost:7860"):
        self.base_url = base_url
    
    def run_flow(self, flow_id: str, inputs: dict) -> dict:
        """
        Run a Langflow workflow
        
        Args:
            flow_id: ID of the flow to run
            inputs: Input data for the flow
            
        Returns:
            Flow execution results
        """
        url = f"{self.base_url}/api/v1/run/{flow_id}"
        
        response = requests.post(
            url,
            json={"inputs": inputs},
            headers={"Content-Type": "application/json"}
        )
        
        return response.json()
    
    def analyze_strategy(self, race_conditions: dict) -> dict:
        """
        Run race strategy analysis workflow
        
        Args:
            race_conditions: Current race conditions
            
        Returns:
            Strategy recommendation
        """
        return self.run_flow(
            flow_id="race_strategy_analysis",
            inputs={"race_conditions": json.dumps(race_conditions)}
        )
    
    def explain_decision(self, recommendation: dict, race_conditions: dict) -> str:
        """
        Run explainability workflow
        
        Args:
            recommendation: Strategy recommendation
            race_conditions: Current race conditions
            
        Returns:
            Human-readable explanation
        """
        result = self.run_flow(
            flow_id="strategy_explainability",
            inputs={
                "recommendation": json.dumps(recommendation),
                "race_conditions": json.dumps(race_conditions)
            }
        )
        
        return result.get("output", "")
```

### Integration Example

```python
from workflows.langflow_client import LangflowClient

# Initialize client
langflow = LangflowClient()

# Prepare race conditions
race_conditions = {
    "lap_number": 25,
    "total_laps": 50,
    "tire_wear": 78,
    "tire_compound": "medium",
    "fuel_level": 65,
    "position": 3
}

# Get strategy recommendation
strategy = langflow.analyze_strategy(race_conditions)

# Get explanation
explanation = langflow.explain_decision(strategy, race_conditions)

print(f"Strategy: {strategy['action']}")
print(f"Explanation: {explanation}")
```

## Advanced Features

### 1. Chain Multiple Workflows

Connect workflows in sequence:
```
Strategy Analysis → Explainability → Risk Assessment → Final Output
```

### 2. Add Conditional Logic

Use Langflow's conditional nodes to:
- Route based on tire wear levels
- Switch strategies based on weather
- Adjust confidence thresholds

### 3. Add Memory

Use Langflow's memory components to:
- Track recommendation history
- Learn from past decisions
- Maintain conversation context

### 4. Add Validation

Add validation nodes to:
- Check input data quality
- Validate AI outputs
- Ensure safety constraints

## Testing Workflows

### Test in Langflow UI

1. Open your workflow
2. Click "Run" button
3. Provide test inputs
4. Review outputs
5. Iterate and improve

### Test via API

```python
# Test script
def test_workflow():
    client = LangflowClient()
    
    test_cases = [
        {
            "name": "High tire wear",
            "conditions": {"tire_wear": 85, "lap_number": 30}
        },
        {
            "name": "Low fuel",
            "conditions": {"fuel_level": 15, "lap_number": 40}
        }
    ]
    
    for test in test_cases:
        print(f"\nTesting: {test['name']}")
        result = client.analyze_strategy(test['conditions'])
        print(f"Result: {result}")

test_workflow()
```

## Best Practices

1. **Modular Design**: Create separate flows for different tasks
2. **Error Handling**: Add error handling nodes
3. **Logging**: Enable logging for debugging
4. **Version Control**: Export and version your flows
5. **Documentation**: Document each node's purpose
6. **Testing**: Test with various race scenarios

## Troubleshooting

### Common Issues

**Issue**: Langflow won't start
```bash
# Solution: Check port availability
netstat -an | grep 7860

# Use different port
langflow run --port 8080
```

**Issue**: IBM Granite connection fails
```bash
# Solution: Verify credentials
export IBM_WATSONX_API_KEY="your_key"
export IBM_WATSONX_PROJECT_ID="your_project_id"
```

**Issue**: Workflow timeout
```bash
# Solution: Increase timeout in Langflow settings
# Or optimize prompt length
```

## Next Steps

1. Create the three core workflows
2. Test with sample race data
3. Integrate with Streamlit frontend
4. Add monitoring and logging
5. Optimize for performance

## Resources

- [Langflow Documentation](https://docs.langflow.org/)
- [IBM Granite Documentation](https://www.ibm.com/granite)
- [Langflow GitHub](https://github.com/logspace-ai/langflow)

---

**Built for AI Race Engineer Copilot**