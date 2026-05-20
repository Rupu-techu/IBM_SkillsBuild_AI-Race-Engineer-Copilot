"""
Race Analyzer Module
Analyzes race conditions and generates strategy recommendations
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class TireCompound(Enum):
    """Tire compound types"""
    SOFT = "soft"
    MEDIUM = "medium"
    HARD = "hard"
    INTERMEDIATE = "intermediate"
    WET = "wet"


class WeatherCondition(Enum):
    """Weather conditions"""
    DRY = "dry"
    LIGHT_RAIN = "light_rain"
    HEAVY_RAIN = "heavy_rain"
    MIXED = "mixed"


class StrategyAction(Enum):
    """Possible strategy actions"""
    PIT_NOW = "pit_now"
    PIT_NEXT_LAP = "pit_next_lap"
    STAY_OUT = "stay_out"
    PUSH_HARD = "push_hard"
    CONSERVE_TIRES = "conserve_tires"
    OVERTAKE_OPPORTUNITY = "overtake_opportunity"


@dataclass
class RaceConditions:
    """Data class for race conditions"""
    lap_number: int
    total_laps: int
    tire_wear: float  # Percentage (0-100)
    tire_compound: TireCompound
    tire_age: int  # Laps on current tires
    weather: WeatherCondition
    track_temp: float  # Celsius
    air_temp: float  # Celsius
    position: int
    fuel_level: float  # Percentage (0-100)
    gap_to_leader: float  # Seconds
    gap_to_behind: float  # Seconds
    track_conditions: str  # "green", "yellow", "safety_car"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for AI processing"""
        return {
            "lap_number": self.lap_number,
            "total_laps": self.total_laps,
            "race_progress": f"{(self.lap_number / self.total_laps) * 100:.1f}%",
            "tire_wear": self.tire_wear,
            "tire_compound": self.tire_compound.value,
            "tire_age": self.tire_age,
            "weather": self.weather.value,
            "track_temp": self.track_temp,
            "air_temp": self.air_temp,
            "position": self.position,
            "fuel_level": self.fuel_level,
            "gap_to_leader": self.gap_to_leader,
            "gap_to_behind": self.gap_to_behind,
            "track_conditions": self.track_conditions
        }


@dataclass
class StrategyRecommendation:
    """Data class for strategy recommendations"""
    action: StrategyAction
    confidence: float  # 0-1
    reasoning: str
    risk_level: str  # "low", "medium", "high"
    expected_outcome: str
    alternative_actions: List[Dict]
    timing_window: Optional[str] = None
    tire_recommendation: Optional[TireCompound] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "action": self.action.value,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "risk_level": self.risk_level,
            "expected_outcome": self.expected_outcome,
            "alternative_actions": self.alternative_actions,
            "timing_window": self.timing_window,
            "tire_recommendation": self.tire_recommendation.value if self.tire_recommendation else None
        }


class RaceAnalyzer:
    """
    Main race analysis engine
    Processes race conditions and generates strategy recommendations
    """
    
    def __init__(self):
        self.tire_degradation_threshold = 85.0  # Percentage
        self.fuel_critical_level = 15.0  # Percentage
        self.optimal_pit_window_start = 0.4  # 40% race distance
        self.optimal_pit_window_end = 0.7  # 70% race distance
    
    def analyze_strategy(self, conditions: RaceConditions) -> StrategyRecommendation:
        """
        Analyze race conditions and generate strategy recommendation
        
        Args:
            conditions: Current race conditions
            
        Returns:
            StrategyRecommendation with action and reasoning
        """
        # Calculate race progress
        race_progress = conditions.lap_number / conditions.total_laps
        
        # Analyze tire condition
        tire_critical = conditions.tire_wear > self.tire_degradation_threshold
        tire_age_high = conditions.tire_age > 15
        
        # Analyze fuel situation
        fuel_critical = conditions.fuel_level < self.fuel_critical_level
        
        # Check pit window
        in_pit_window = (self.optimal_pit_window_start <= race_progress <= 
                        self.optimal_pit_window_end)
        
        # Analyze weather
        weather_changing = conditions.weather in [WeatherCondition.MIXED, 
                                                  WeatherCondition.LIGHT_RAIN]
        
        # Generate recommendation based on conditions
        if tire_critical and in_pit_window:
            return self._recommend_pit_now(conditions, "tire_degradation")
        
        elif fuel_critical:
            return self._recommend_pit_now(conditions, "fuel_critical")
        
        elif weather_changing:
            return self._recommend_weather_strategy(conditions)
        
        elif conditions.gap_to_behind < 1.0 and not tire_critical:
            return self._recommend_push_strategy(conditions)
        
        elif tire_age_high and in_pit_window:
            return self._recommend_pit_next_lap(conditions)
        
        else:
            return self._recommend_stay_out(conditions)
    
    def _recommend_pit_now(self, conditions: RaceConditions, 
                          reason: str) -> StrategyRecommendation:
        """Generate pit now recommendation"""
        if reason == "tire_degradation":
            reasoning = (
                f"Pit now because tire degradation is critical at {conditions.tire_wear:.1f}%. "
                f"Current tire age: {conditions.tire_age} laps. "
                f"Staying out risks performance loss and potential undercut from competitors."
            )
            tire_rec = self._recommend_tire_compound(conditions)
            
        elif reason == "fuel_critical":
            reasoning = (
                f"Pit now due to critical fuel level at {conditions.fuel_level:.1f}%. "
                f"Insufficient fuel to complete the race distance. "
                f"Immediate pit stop required to avoid retirement."
            )
            tire_rec = conditions.tire_compound
        
        else:
            reasoning = "Pit stop recommended based on current race conditions."
            tire_rec = self._recommend_tire_compound(conditions)
        
        return StrategyRecommendation(
            action=StrategyAction.PIT_NOW,
            confidence=0.9,
            reasoning=reasoning,
            risk_level="low",
            expected_outcome=f"Maintain position {conditions.position} with fresh tires",
            alternative_actions=[
                {"action": "stay_out", "risk": "high", "reason": "Risk tire failure or fuel shortage"}
            ],
            timing_window="Current lap",
            tire_recommendation=tire_rec
        )
    
    def _recommend_pit_next_lap(self, conditions: RaceConditions) -> StrategyRecommendation:
        """Generate pit next lap recommendation"""
        reasoning = (
            f"Pit next lap for optimal strategy. Current tire wear: {conditions.tire_wear:.1f}%, "
            f"tire age: {conditions.tire_age} laps. "
            f"One more lap allows better track position while maintaining tire performance."
        )
        
        return StrategyRecommendation(
            action=StrategyAction.PIT_NEXT_LAP,
            confidence=0.85,
            reasoning=reasoning,
            risk_level="low",
            expected_outcome=f"Optimal pit timing for position {conditions.position}",
            alternative_actions=[
                {"action": "pit_now", "risk": "low", "reason": "Slightly earlier but safer"},
                {"action": "stay_out", "risk": "medium", "reason": "Risk missing optimal window"}
            ],
            timing_window="Next lap",
            tire_recommendation=self._recommend_tire_compound(conditions)
        )
    
    def _recommend_stay_out(self, conditions: RaceConditions) -> StrategyRecommendation:
        """Generate stay out recommendation"""
        reasoning = (
            f"Stay out and maintain current pace. Tire wear at {conditions.tire_wear:.1f}% "
            f"is acceptable, fuel level at {conditions.fuel_level:.1f}% is sufficient. "
            f"Current position {conditions.position} is stable with {conditions.gap_to_behind:.1f}s gap behind."
        )
        
        return StrategyRecommendation(
            action=StrategyAction.STAY_OUT,
            confidence=0.8,
            reasoning=reasoning,
            risk_level="low",
            expected_outcome="Maintain current position and tire advantage",
            alternative_actions=[
                {"action": "conserve_tires", "risk": "low", "reason": "Extend stint if needed"}
            ],
            timing_window=None
        )
    
    def _recommend_weather_strategy(self, conditions: RaceConditions) -> StrategyRecommendation:
        """Generate weather-based strategy recommendation"""
        if conditions.weather == WeatherCondition.LIGHT_RAIN:
            tire_rec = TireCompound.INTERMEDIATE
            reasoning = (
                f"Weather changing to light rain. Consider pit stop for intermediate tires. "
                f"Current conditions: track temp {conditions.track_temp}°C, "
                f"air temp {conditions.air_temp}°C. "
                f"Early switch could provide competitive advantage."
            )
        else:
            tire_rec = TireCompound.INTERMEDIATE
            reasoning = (
                f"Mixed weather conditions detected. Monitor closely for tire change opportunity. "
                f"Current tire: {conditions.tire_compound.value}, wear: {conditions.tire_wear:.1f}%."
            )
        
        return StrategyRecommendation(
            action=StrategyAction.PIT_NOW,
            confidence=0.75,
            reasoning=reasoning,
            risk_level="medium",
            expected_outcome="Gain advantage with weather-appropriate tires",
            alternative_actions=[
                {"action": "stay_out", "risk": "high", "reason": "Risk losing grip in changing conditions"}
            ],
            timing_window="Within 2 laps",
            tire_recommendation=tire_rec
        )
    
    def _recommend_push_strategy(self, conditions: RaceConditions) -> StrategyRecommendation:
        """Generate push hard recommendation"""
        reasoning = (
            f"Push hard to defend position {conditions.position}. "
            f"Gap to car behind: {conditions.gap_to_behind:.1f}s (critical). "
            f"Tire wear at {conditions.tire_wear:.1f}% allows for increased pace. "
            f"Maintain pressure to prevent undercut attempt."
        )
        
        return StrategyRecommendation(
            action=StrategyAction.PUSH_HARD,
            confidence=0.85,
            reasoning=reasoning,
            risk_level="medium",
            expected_outcome="Maintain or extend gap to car behind",
            alternative_actions=[
                {"action": "conserve_tires", "risk": "high", "reason": "Risk losing position"}
            ],
            timing_window="Next 3-5 laps"
        )
    
    def _recommend_tire_compound(self, conditions: RaceConditions) -> TireCompound:
        """Recommend tire compound based on conditions"""
        race_progress = conditions.lap_number / conditions.total_laps
        
        # Weather-based selection
        if conditions.weather == WeatherCondition.HEAVY_RAIN:
            return TireCompound.WET
        elif conditions.weather == WeatherCondition.LIGHT_RAIN:
            return TireCompound.INTERMEDIATE
        
        # Dry conditions - strategy based on race progress
        if race_progress < 0.3:
            # Early race - medium or hard
            return TireCompound.MEDIUM if conditions.track_temp > 35 else TireCompound.HARD
        elif race_progress < 0.7:
            # Mid race - hard for longevity
            return TireCompound.HARD
        else:
            # Late race - soft for pace
            return TireCompound.SOFT
    
    def calculate_undercut_opportunity(self, conditions: RaceConditions, 
                                      competitor_tire_age: int) -> Dict:
        """
        Calculate undercut opportunity against competitor
        
        Args:
            conditions: Current race conditions
            competitor_tire_age: Age of competitor's tires
            
        Returns:
            Dictionary with undercut analysis
        """
        tire_delta = competitor_tire_age - conditions.tire_age
        
        # Estimate time gain per lap with fresh tires
        time_gain_per_lap = 0.3 + (tire_delta * 0.05)  # Seconds
        
        # Pit stop time loss (typical)
        pit_time_loss = 20.0  # Seconds
        
        # Calculate laps needed to recover
        laps_to_recover = int(pit_time_loss / time_gain_per_lap) + 1
        
        # Check if undercut is viable
        laps_remaining = conditions.total_laps - conditions.lap_number
        is_viable = laps_to_recover < laps_remaining
        
        return {
            "is_viable": is_viable,
            "time_gain_per_lap": time_gain_per_lap,
            "laps_to_recover": laps_to_recover,
            "laps_remaining": laps_remaining,
            "confidence": 0.8 if is_viable else 0.3,
            "recommendation": "Execute undercut" if is_viable else "Undercut not viable"
        }

# Made with Bob
