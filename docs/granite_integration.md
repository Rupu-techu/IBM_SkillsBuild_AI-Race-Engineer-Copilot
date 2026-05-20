# IBM Granite Integration Guide

## Overview

This guide explains how to integrate IBM Granite models with the AI Race Engineer Copilot using IBM watsonx.ai platform.

## Prerequisites

1. **IBM Cloud Account**
   - Sign up at [cloud.ibm.com](https://cloud.ibm.com)
   - Free tier available for development

2. **IBM watsonx.ai Access**
   - Create a watsonx.ai instance
   - Obtain API credentials

3. **Python Environment**
   - Python 3.9 or higher
   - Virtual environment recommended

## Setup Steps

### Step 1: Create IBM Cloud Account

1. Visit [cloud.ibm.com](https://cloud.ibm.com)
2. Click "Create an account"
3. Complete registration process
4. Verify your email

### Step 2: Set Up watsonx.ai

1. Log in to IBM Cloud Console
2. Navigate to **Catalog** → **AI / Machine Learning**
3. Select **watsonx.ai**
4. Click **Create** to provision an instance
5. Choose your region (e.g., Dallas, Frankfurt)
6. Select a pricing plan:
   - **Lite**: Free tier for development
   - **Standard**: Pay-as-you-go for production

### Step 3: Get API Credentials

1. Go to your watsonx.ai instance
2. Click **Manage** → **Access (IAM)**
3. Create an API key:
   ```
   Name: race-engineer-copilot
   Description: API key for AI Race Engineer Copilot
   ```
4. **Important**: Copy and save the API key immediately (it won't be shown again)

### Step 4: Get Project ID

1. In watsonx.ai, go to **Projects**
2. Create a new project or select existing one
3. Click on project name
4. Copy the **Project ID** from the URL or project settings

### Step 5: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# IBM watsonx.ai Configuration
IBM_WATSONX_API_KEY=your_api_key_here
IBM_WATSONX_PROJECT_ID=your_project_id_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com

# IBM Granite Model Configuration
GRANITE_MODEL_ID=ibm/granite-13b-chat-v2
GRANITE_MAX_TOKENS=1024
GRANITE_TEMPERATURE=0.7
```

**Regional URLs**:
- US South (Dallas): `https://us-south.ml.cloud.ibm.com`
- EU (Frankfurt): `https://eu-de.ml.cloud.ibm.com`
- UK (London): `https://eu-gb.ml.cloud.ibm.com`
- Japan (Tokyo): `https://jp-tok.ml.cloud.ibm.com`

### Step 6: Install Dependencies

```bash
pip install ibm-watsonx-ai
pip install python-dotenv
```

## Using IBM Granite in Code

### Basic Usage

```python
from src.ai.granite_engine import GraniteEngine

# Initialize engine (loads credentials from .env)
engine = GraniteEngine()

# Generate explanation
recommendation = {
    "action": "pit_now",
    "confidence": 0.9,
    "reasoning": "Tire degradation critical"
}

race_conditions = {
    "lap_number": 25,
    "total_laps": 50,
    "tire_wear": 87.5,
    "position": 3
}

explanation = engine.explain_decision(recommendation, race_conditions)
print(explanation)
```

### Advanced Usage

```python
from src.ai.granite_engine import GraniteEngine, GraniteConfig

# Custom configuration
config = GraniteConfig(
    api_key="your_api_key",
    project_id="your_project_id",
    url="https://us-south.ml.cloud.ibm.com",
    model_id="ibm/granite-13b-chat-v2",
    max_tokens=2048,
    temperature=0.5
)

engine = GraniteEngine(config)

# Analyze race scenario
analysis = engine.analyze_race_scenario(race_conditions)
print(analysis["analysis"])

# Generate pit strategy
strategies = engine.generate_pit_strategy(race_conditions, remaining_laps=25)
for strategy in strategies:
    print(f"{strategy['name']}: {strategy['description']}")
```

## IBM Granite Models

### Available Models

1. **granite-13b-chat-v2** (Recommended)
   - 13 billion parameters
   - Optimized for conversational AI
   - Best for explainable reasoning
   - Max tokens: 8192

2. **granite-13b-instruct-v2**
   - Instruction-following variant
   - Good for structured outputs
   - Max tokens: 8192

3. **granite-20b-multilingual**
   - Multilingual support
   - 20 billion parameters
   - Supports 100+ languages

### Model Parameters

```python
params = {
    "max_new_tokens": 1024,      # Maximum tokens to generate
    "temperature": 0.7,           # Randomness (0.0-1.0)
    "top_p": 1.0,                # Nucleus sampling
    "top_k": 50,                 # Top-k sampling
    "repetition_penalty": 1.0,   # Penalize repetition
    "stop_sequences": ["\n\n"]   # Stop generation at sequences
}
```

**Parameter Guidelines**:
- **Temperature**:
  - 0.0-0.3: Deterministic, factual responses
  - 0.4-0.7: Balanced creativity and accuracy (recommended)
  - 0.8-1.0: More creative, less predictable

- **Max Tokens**:
  - Short explanations: 256-512
  - Detailed analysis: 1024-2048
  - Comprehensive reports: 2048-4096

## Prompt Engineering for Racing Strategy

### Effective Prompt Structure

```python
prompt = f"""You are an expert AI Race Engineer analyzing a Formula 1 race.

Context:
- Current lap: {lap}/{total_laps}
- Position: P{position}
- Tire condition: {tire_wear}% wear, {tire_age} laps old
- Weather: {weather}

Task:
Explain why {action} is the optimal strategy.

Requirements:
1. Be concise (2-3 sentences)
2. Focus on data-driven reasoning
3. Consider risk vs reward
4. Mention specific metrics

Explanation:"""
```

### Best Practices

1. **Be Specific**: Provide exact numbers and conditions
2. **Set Context**: Explain the racing scenario clearly
3. **Define Output**: Specify desired format and length
4. **Use Examples**: Show expected response format
5. **Iterate**: Refine prompts based on results

### Example Prompts

**Pit Stop Decision**:
```python
prompt = """Analyze this pit stop decision:

Race: Lap 28/50 (56% complete)
Tire: Medium compound, 18 laps old, 85% wear
Position: P3, gap behind: 2.1s
Weather: Dry, track temp 45°C

Should we pit now or wait? Explain in 2 sentences."""
```

**Weather Strategy**:
```python
prompt = """Weather is changing from dry to light rain.

Current: Soft tires, 45% wear, 8 laps old
Forecast: Light rain in 3-5 laps
Position: P5, competitive situation

Recommend tire strategy and timing. Be specific."""
```

## Error Handling

### Common Issues and Solutions

**Issue 1: Authentication Error**
```
Error: Invalid API key
```
**Solution**: 
- Verify API key in `.env` file
- Check for extra spaces or quotes
- Regenerate API key if needed

**Issue 2: Project Not Found**
```
Error: Project ID not found
```
**Solution**:
- Verify project ID is correct
- Ensure project exists in watsonx.ai
- Check regional URL matches project location

**Issue 3: Rate Limiting**
```
Error: Rate limit exceeded
```
**Solution**:
- Implement exponential backoff
- Cache responses when possible
- Upgrade to higher tier plan

**Issue 4: Model Not Available**
```
Error: Model not found
```
**Solution**:
- Check model ID spelling
- Verify model is available in your region
- Use alternative model (e.g., granite-13b-instruct-v2)

### Implementing Retry Logic

```python
import time
from typing import Optional

def generate_with_retry(
    engine: GraniteEngine,
    prompt: str,
    max_retries: int = 3
) -> Optional[str]:
    """Generate text with exponential backoff retry"""
    
    for attempt in range(max_retries):
        try:
            return engine.model.generate_text(prompt=prompt)
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Failed after {max_retries} attempts: {e}")
                return None
            
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s")
            time.sleep(wait_time)
    
    return None
```

## Performance Optimization

### 1. Response Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_explanation(
    action: str,
    tire_wear: float,
    lap: int
) -> str:
    """Cache explanations for similar conditions"""
    # Generate explanation
    pass
```

### 2. Batch Processing

```python
def analyze_multiple_scenarios(scenarios: List[Dict]) -> List[Dict]:
    """Process multiple scenarios efficiently"""
    results = []
    
    # Batch similar requests
    for scenario in scenarios:
        result = engine.analyze_race_scenario(scenario)
        results.append(result)
    
    return results
```

### 3. Async Operations

```python
import asyncio

async def async_analyze(engine, conditions):
    """Async analysis for better performance"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        engine.analyze_race_scenario,
        conditions
    )
```

## Testing Granite Integration

### Unit Tests

```python
import pytest
from src.ai.granite_engine import GraniteEngine

def test_granite_initialization():
    """Test engine initialization"""
    engine = GraniteEngine()
    assert engine is not None
    assert engine.config is not None

def test_explanation_generation():
    """Test explanation generation"""
    engine = GraniteEngine()
    
    recommendation = {
        "action": "pit_now",
        "confidence": 0.9
    }
    
    conditions = {
        "lap_number": 25,
        "tire_wear": 85.0
    }
    
    explanation = engine.explain_decision(recommendation, conditions)
    assert explanation is not None
    assert len(explanation) > 0
```

### Integration Tests

```python
def test_end_to_end_analysis():
    """Test complete analysis workflow"""
    from src.core.race_analyzer import RaceAnalyzer, RaceConditions
    from src.ai.granite_engine import GraniteEngine
    
    # Create conditions
    conditions = RaceConditions(...)
    
    # Analyze
    analyzer = RaceAnalyzer()
    recommendation = analyzer.analyze_strategy(conditions)
    
    # Get AI explanation
    engine = GraniteEngine()
    explanation = engine.explain_decision(
        recommendation.to_dict(),
        conditions.to_dict()
    )
    
    assert explanation is not None
```

## Cost Management

### Pricing Considerations

**Lite Plan** (Free):
- Limited API calls per month
- Good for development and testing
- No credit card required

**Standard Plan** (Pay-as-you-go):
- Charged per 1000 tokens
- Input tokens: ~$0.0005/1K
- Output tokens: ~$0.0015/1K
- Typical analysis: $0.001-0.005

### Cost Optimization Tips

1. **Use Shorter Prompts**: Be concise but clear
2. **Limit Max Tokens**: Set appropriate limits
3. **Cache Results**: Avoid redundant API calls
4. **Batch Requests**: Process multiple items together
5. **Monitor Usage**: Track API calls and costs

## Security Best Practices

1. **Never Commit Credentials**
   - Use `.env` files
   - Add `.env` to `.gitignore`
   - Use environment variables in production

2. **Rotate API Keys Regularly**
   - Generate new keys periodically
   - Revoke old keys
   - Use separate keys for dev/prod

3. **Implement Access Controls**
   - Limit API key permissions
   - Use IAM roles appropriately
   - Monitor API usage

4. **Secure Data Transmission**
   - Always use HTTPS
   - Validate SSL certificates
   - Encrypt sensitive data

## Troubleshooting

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

engine = GraniteEngine()
# Detailed logs will show API calls and responses
```

### Testing Connection

```python
def test_watsonx_connection():
    """Test connection to watsonx.ai"""
    try:
        engine = GraniteEngine()
        
        # Simple test prompt
        response = engine.model.generate_text(
            prompt="Say 'Connection successful'"
        )
        
        print(f"✓ Connection successful: {response}")
        return True
        
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False
```

## Additional Resources

- [IBM watsonx.ai Documentation](https://www.ibm.com/docs/en/watsonx-as-a-service)
- [IBM Granite Models](https://www.ibm.com/granite)
- [Python SDK Documentation](https://ibm.github.io/watsonx-ai-python-sdk/)
- [API Reference](https://cloud.ibm.com/apidocs/watsonx-ai)

## Support

For issues with IBM Granite integration:
1. Check IBM Cloud status page
2. Review watsonx.ai documentation
3. Contact IBM Support
4. Post in IBM Developer Community

---

**Next Steps**: After setting up Granite integration, proceed to [Langflow Workflow Design](langflow_workflows.md) to orchestrate complex AI workflows.