"""
Langflow API Client for AI Race Engineer Copilot
Integrates Langflow workflows with the application
"""

import requests
import json
from typing import Dict, Optional
import os


class LangflowClient:
    """
    Client for interacting with Langflow API
    Orchestrates AI workflows for race strategy analysis
    """
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize Langflow client
        
        Args:
            base_url: Base URL for Langflow server (default: http://localhost:7860)
        """
        self.base_url = base_url or os.getenv("LANGFLOW_URL", "http://localhost:7860")
        self.api_version = "v1"
    
    def run_flow(self, flow_id: str, inputs: Dict, tweaks: Optional[Dict] = None) -> Dict:
        """
        Run a Langflow workflow
        
        Args:
            flow_id: ID or name of the flow to run
            inputs: Input data for the flow
            tweaks: Optional parameter tweaks for the flow
            
        Returns:
            Flow execution results
        """
        url = f"{self.base_url}/api/{self.api_version}/run/{flow_id}"
        
        payload = {
            "inputs": inputs
        }
        
        if tweaks:
            payload["tweaks"] = tweaks
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error running Langflow workflow: {e}")
            return {"error": str(e), "success": False}
    
    def analyze_strategy(self, race_conditions: Dict) -> Dict:
        """
        Run race strategy analysis workflow
        
        Args:
            race_conditions: Current race conditions dictionary
            
        Returns:
            Strategy recommendation dictionary
        """
        try:
            result = self.run_flow(
                flow_id="race_strategy_analysis",
                inputs={
                    "race_conditions": json.dumps(race_conditions, indent=2)
                }
            )
            
            if result.get("success", False):
                return result.get("output", {})
            else:
                return self._fallback_strategy(race_conditions)
        
        except Exception as e:
            print(f"Error in strategy analysis: {e}")
            return self._fallback_strategy(race_conditions)
    
    def explain_decision(self, recommendation: Dict, race_conditions: Dict) -> str:
        """
        Run explainability workflow to generate human-readable explanation
        
        Args:
            recommendation: Strategy recommendation dictionary
            race_conditions: Current race conditions dictionary
            
        Returns:
            Human-readable explanation string
        """
        try:
            result = self.run_flow(
                flow_id="strategy_explainability",
                inputs={
                    "recommendation": json.dumps(recommendation, indent=2),
                    "race_conditions": json.dumps(race_conditions, indent=2)
                }
            )
            
            if result.get("success", False):
                return result.get("output", "")
            else:
                return self._fallback_explanation(recommendation, race_conditions)
        
        except Exception as e:
            print(f"Error in explanation generation: {e}")
            return self._fallback_explanation(recommendation, race_conditions)
    
    def compare_strategies(self, race_conditions: Dict) -> list:
        """
        Run multi-strategy comparison workflow
        
        Args:
            race_conditions: Current race conditions dictionary
            
        Returns:
            List of strategy options with comparisons
        """
        try:
            result = self.run_flow(
                flow_id="multi_strategy_comparison",
                inputs={
                    "race_conditions": json.dumps(race_conditions, indent=2)
                }
            )
            
            if result.get("success", False):
                return result.get("output", [])
            else:
                return []
        
        except Exception as e:
            print(f"Error in strategy comparison: {e}")
            return []
    
    def _fallback_strategy(self, race_conditions: Dict) -> Dict:
        """
        Fallback strategy when Langflow is unavailable
        
        Args:
            race_conditions: Current race conditions
            
        Returns:
            Basic strategy recommendation
        """
        tire_wear = race_conditions.get("tire_wear", 0)
        fuel_level = race_conditions.get("fuel_level", 100)
        
        if tire_wear > 85 or fuel_level < 20:
            action = "pit_now"
            confidence = 0.9
            reasoning = "Critical tire wear or fuel level requires immediate pit stop"
        elif tire_wear > 70:
            action = "pit_next_lap"
            confidence = 0.8
            reasoning = "Tire wear approaching critical levels, pit stop recommended soon"
        else:
            action = "stay_out"
            confidence = 0.75
            reasoning = "Current conditions allow continuing on track"
        
        return {
            "action": action,
            "confidence": confidence,
            "reasoning": reasoning,
            "risk_level": "medium",
            "expected_outcome": "Maintain competitive position",
            "source": "fallback"
        }
    
    def _fallback_explanation(self, recommendation: Dict, race_conditions: Dict) -> str:
        """
        Fallback explanation when Langflow is unavailable
        
        Args:
            recommendation: Strategy recommendation
            race_conditions: Current race conditions
            
        Returns:
            Basic explanation string
        """
        action = recommendation.get("action", "unknown")
        confidence = recommendation.get("confidence", 0) * 100
        
        return f"{action.replace('_', ' ').title()} recommended with {confidence:.0f}% confidence. {recommendation.get('reasoning', '')}"
    
    def health_check(self) -> bool:
        """
        Check if Langflow server is available
        
        Returns:
            True if server is healthy, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = LangflowClient()
    
    # Check health
    if client.health_check():
        print("✓ Langflow server is running")
    else:
        print("✗ Langflow server is not available")
    
    # Test strategy analysis
    test_conditions = {
        "lap_number": 25,
        "total_laps": 50,
        "tire_wear": 78,
        "tire_compound": "medium",
        "tire_age": 16,
        "fuel_level": 65,
        "weather": "dry",
        "track_temp": 42,
        "position": 3
    }
    
    print("\nTesting strategy analysis...")
    strategy = client.analyze_strategy(test_conditions)
    print(f"Strategy: {strategy}")
    
    print("\nTesting explanation generation...")
    explanation = client.explain_decision(strategy, test_conditions)
    print(f"Explanation: {explanation}")

# Made with Bob
