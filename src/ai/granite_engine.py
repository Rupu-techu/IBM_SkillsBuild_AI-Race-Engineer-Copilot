"""
IBM Granite AI Engine
Integrates with IBM watsonx.ai and Granite models for explainable AI reasoning
"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass
import json

try:
    from ibm_watsonx_ai import APIClient
    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference
    WATSONX_AVAILABLE = True
except ImportError:
    WATSONX_AVAILABLE = False
    print("Warning: ibm-watsonx-ai not installed. Using mock mode.")


@dataclass
class GraniteConfig:
    """Configuration for IBM Granite model"""
    api_key: str
    project_id: str
    url: str
    model_id: str = "ibm/granite-13b-chat-v2"
    max_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 1.0
    top_k: int = 50


class GraniteEngine:
    """
    IBM Granite AI Engine for race strategy reasoning
    Provides explainable AI decision-making using IBM watsonx.ai
    """
    
    def __init__(self, config: Optional[GraniteConfig] = None):
        """
        Initialize Granite engine
        
        Args:
            config: GraniteConfig object, or None to load from environment
        """
        if config is None:
            config = self._load_config_from_env()
        
        self.config = config
        self.client = None
        self.model = None
        
        if WATSONX_AVAILABLE:
            self._initialize_watsonx()
        else:
            print("Running in mock mode - install ibm-watsonx-ai for full functionality")
    
    def _load_config_from_env(self) -> GraniteConfig:
        """Load configuration from environment variables"""
        return GraniteConfig(
            api_key=os.getenv("IBM_WATSONX_API_KEY", ""),
            project_id=os.getenv("IBM_WATSONX_PROJECT_ID", ""),
            url=os.getenv("IBM_WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
            model_id=os.getenv("GRANITE_MODEL_ID", "ibm/granite-13b-chat-v2"),
            max_tokens=int(os.getenv("GRANITE_MAX_TOKENS", "1024")),
            temperature=float(os.getenv("GRANITE_TEMPERATURE", "0.7"))
        )
    
    def _initialize_watsonx(self):
        """Initialize IBM watsonx.ai client"""
        try:
            credentials = Credentials(
                url=self.config.url,
                api_key=self.config.api_key
            )
            
            self.client = APIClient(credentials)
            
            self.model = ModelInference(
                model_id=self.config.model_id,
                credentials=credentials,
                project_id=self.config.project_id,
                params={
                    "max_new_tokens": self.config.max_tokens,
                    "temperature": self.config.temperature,
                    "top_p": self.config.top_p,
                    "top_k": self.config.top_k
                }
            )
            
            print(f"✓ IBM Granite engine initialized: {self.config.model_id}")
            
        except Exception as e:
            print(f"Warning: Could not initialize watsonx.ai: {e}")
            print("Running in mock mode")
            self.model = None
    
    def explain_decision(self, recommendation: Dict, 
                        race_conditions: Dict) -> str:
        """
        Generate explainable AI reasoning for a strategy decision
        
        Args:
            recommendation: Strategy recommendation dictionary
            race_conditions: Current race conditions dictionary
            
        Returns:
            Human-readable explanation string
        """
        prompt = self._build_explanation_prompt(recommendation, race_conditions)
        
        if self.model is not None:
            try:
                response = self.model.generate_text(prompt=prompt)
                return response
            except Exception as e:
                print(f"Error generating explanation: {e}")
                return self._generate_mock_explanation(recommendation, race_conditions)
        else:
            return self._generate_mock_explanation(recommendation, race_conditions)
    
    def _build_explanation_prompt(self, recommendation: Dict, 
                                  race_conditions: Dict) -> str:
        """Build prompt for Granite model"""
        prompt = f"""You are an expert AI Race Engineer analyzing a Formula 1 race situation.

Race Conditions:
- Lap: {race_conditions.get('lap_number')}/{race_conditions.get('total_laps')}
- Position: {race_conditions.get('position')}
- Tire Wear: {race_conditions.get('tire_wear')}%
- Tire Compound: {race_conditions.get('tire_compound')}
- Tire Age: {race_conditions.get('tire_age')} laps
- Fuel Level: {race_conditions.get('fuel_level')}%
- Weather: {race_conditions.get('weather')}
- Track Temperature: {race_conditions.get('track_temp')}°C
- Gap to Leader: {race_conditions.get('gap_to_leader')}s
- Gap to Behind: {race_conditions.get('gap_to_behind')}s

Recommended Strategy:
- Action: {recommendation.get('action')}
- Confidence: {recommendation.get('confidence')*100:.0f}%
- Risk Level: {recommendation.get('risk_level')}

Provide a clear, concise explanation (2-3 sentences) of WHY this strategy is recommended, considering:
1. The current race situation
2. Tire and fuel management
3. Competitive positioning
4. Risk vs reward analysis

Explanation:"""
        
        return prompt
    
    def _generate_mock_explanation(self, recommendation: Dict, 
                                   race_conditions: Dict) -> str:
        """Generate mock explanation when Granite is not available"""
        action = recommendation.get('action', 'unknown')
        confidence = recommendation.get('confidence', 0) * 100
        
        explanations = {
            'pit_now': f"Immediate pit stop recommended with {confidence:.0f}% confidence. {recommendation.get('reasoning', '')}",
            'pit_next_lap': f"Pit stop next lap advised with {confidence:.0f}% confidence. {recommendation.get('reasoning', '')}",
            'stay_out': f"Continue current strategy with {confidence:.0f}% confidence. {recommendation.get('reasoning', '')}",
            'push_hard': f"Increase pace recommended with {confidence:.0f}% confidence. {recommendation.get('reasoning', '')}",
            'conserve_tires': f"Tire conservation strategy with {confidence:.0f}% confidence. {recommendation.get('reasoning', '')}"
        }
        
        return explanations.get(action, recommendation.get('reasoning', 'Strategy recommendation based on current conditions.'))
    
    def analyze_race_scenario(self, race_conditions: Dict) -> Dict:
        """
        Perform comprehensive race scenario analysis using Granite
        
        Args:
            race_conditions: Dictionary of current race conditions
            
        Returns:
            Dictionary with detailed analysis
        """
        prompt = self._build_scenario_analysis_prompt(race_conditions)
        
        if self.model is not None:
            try:
                response = self.model.generate_text(prompt=prompt)
                return self._parse_scenario_response(response)
            except Exception as e:
                print(f"Error analyzing scenario: {e}")
                return self._generate_mock_scenario_analysis(race_conditions)
        else:
            return self._generate_mock_scenario_analysis(race_conditions)
    
    def _build_scenario_analysis_prompt(self, race_conditions: Dict) -> str:
        """Build prompt for scenario analysis"""
        prompt = f"""Analyze this Formula 1 race scenario and provide strategic insights:

Current Situation:
- Lap {race_conditions.get('lap_number')} of {race_conditions.get('total_laps')}
- Position: P{race_conditions.get('position')}
- Tire: {race_conditions.get('tire_compound')} ({race_conditions.get('tire_age')} laps old, {race_conditions.get('tire_wear')}% wear)
- Fuel: {race_conditions.get('fuel_level')}%
- Weather: {race_conditions.get('weather')}
- Gaps: +{race_conditions.get('gap_to_leader')}s to leader, +{race_conditions.get('gap_to_behind')}s to car behind

Provide analysis on:
1. Key strategic opportunities
2. Main risks to consider
3. Optimal timing for next pit stop
4. Competitive threats

Analysis:"""
        
        return prompt
    
    def _parse_scenario_response(self, response: str) -> Dict:
        """Parse Granite response into structured format"""
        return {
            "analysis": response,
            "source": "IBM Granite",
            "model": self.config.model_id
        }
    
    def _generate_mock_scenario_analysis(self, race_conditions: Dict) -> Dict:
        """Generate mock scenario analysis"""
        lap_progress = (race_conditions.get('lap_number', 0) / 
                       race_conditions.get('total_laps', 50)) * 100
        
        analysis = f"""Race Scenario Analysis (Lap {race_conditions.get('lap_number')}/{race_conditions.get('total_laps')}):

Strategic Position: Currently P{race_conditions.get('position')} with {lap_progress:.1f}% race complete.

Tire Status: {race_conditions.get('tire_compound')} compound at {race_conditions.get('tire_wear')}% wear ({race_conditions.get('tire_age')} laps). 
{'Tires approaching critical degradation - pit window opening.' if race_conditions.get('tire_wear', 0) > 80 else 'Tire condition acceptable for current stint.'}

Competitive Situation: Gap to leader: {race_conditions.get('gap_to_leader')}s, Gap behind: {race_conditions.get('gap_to_behind')}s.
{'Under pressure from behind - maintain pace.' if race_conditions.get('gap_to_behind', 10) < 2 else 'Comfortable gap to car behind.'}

Weather Impact: {race_conditions.get('weather')} conditions. Track temp: {race_conditions.get('track_temp')}°C.
{'Monitor weather closely for strategy opportunities.' if race_conditions.get('weather') in ['mixed', 'light_rain'] else 'Stable conditions for current strategy.'}

Fuel Management: {race_conditions.get('fuel_level')}% remaining.
{'Fuel critical - immediate attention required.' if race_conditions.get('fuel_level', 100) < 20 else 'Fuel level adequate for race distance.'}
"""
        
        return {
            "analysis": analysis,
            "source": "Mock Analysis",
            "model": "mock"
        }
    
    def generate_pit_strategy(self, race_conditions: Dict, 
                            remaining_laps: int) -> List[Dict]:
        """
        Generate multi-stop pit strategy recommendations
        
        Args:
            race_conditions: Current race conditions
            remaining_laps: Laps remaining in race
            
        Returns:
            List of pit stop strategy options
        """
        strategies = []
        
        # One-stop strategy
        if remaining_laps > 15:
            strategies.append({
                "name": "One-Stop Strategy",
                "stops": 1,
                "pit_lap": race_conditions.get('lap_number', 0) + (remaining_laps // 2),
                "tire_sequence": [race_conditions.get('tire_compound'), "hard"],
                "risk": "medium",
                "description": "Single pit stop for hard tires to finish the race"
            })
        
        # Two-stop strategy
        if remaining_laps > 25:
            first_stop = race_conditions.get('lap_number', 0) + (remaining_laps // 3)
            second_stop = first_stop + (remaining_laps // 3)
            strategies.append({
                "name": "Two-Stop Strategy",
                "stops": 2,
                "pit_laps": [first_stop, second_stop],
                "tire_sequence": [race_conditions.get('tire_compound'), "medium", "soft"],
                "risk": "high",
                "description": "Aggressive two-stop strategy for maximum pace"
            })
        
        # Conservative strategy
        strategies.append({
            "name": "Conservative Strategy",
            "stops": 0,
            "pit_lap": None,
            "tire_sequence": [race_conditions.get('tire_compound')],
            "risk": "low",
            "description": "Stay out and manage current tires to the end"
        })
        
        return strategies
    
    def evaluate_overtaking_opportunity(self, race_conditions: Dict,
                                       target_gap: float) -> Dict:
        """
        Evaluate overtaking opportunity using AI analysis
        
        Args:
            race_conditions: Current race conditions
            target_gap: Gap to car ahead in seconds
            
        Returns:
            Dictionary with overtaking analysis
        """
        tire_advantage = race_conditions.get('tire_age', 10) < 10
        drs_available = target_gap < 1.0
        
        if tire_advantage and drs_available:
            probability = 0.75
            recommendation = "High probability overtaking opportunity"
        elif tire_advantage or drs_available:
            probability = 0.50
            recommendation = "Moderate overtaking opportunity"
        else:
            probability = 0.25
            recommendation = "Low probability - wait for better opportunity"
        
        return {
            "probability": probability,
            "recommendation": recommendation,
            "factors": {
                "tire_advantage": tire_advantage,
                "drs_available": drs_available,
                "gap": target_gap
            },
            "suggested_action": "Attack" if probability > 0.6 else "Wait"
        }

# Made with Bob
