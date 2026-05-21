"""
Advanced Racing Intelligence Module
Sophisticated AI-powered racing strategy analysis
"""

import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class StrategyOutcome:
    """Predicted outcome of a strategy"""
    strategy_name: str
    expected_position: float
    probability: float
    time_delta: float  # seconds gained/lost
    risk_score: float  # 0-1
    confidence: float  # 0-1


class AdvancedRacingIntelligence:
    """
    Advanced AI racing intelligence for sophisticated strategy analysis
    """
    
    def __init__(self):
        self.tire_compound_performance = {
            'soft': {'speed': 1.0, 'degradation': 3.0, 'optimal_temp': 90},
            'medium': {'speed': 0.95, 'degradation': 2.0, 'optimal_temp': 85},
            'hard': {'speed': 0.90, 'degradation': 1.2, 'optimal_temp': 80},
            'intermediate': {'speed': 0.85, 'degradation': 2.5, 'optimal_temp': 70},
            'wet': {'speed': 0.75, 'degradation': 2.0, 'optimal_temp': 60}
        }
    
    def compare_tire_strategies(self, race_conditions: Dict, 
                                remaining_laps: int) -> List[Dict]:
        """
        Compare different tire compound strategies
        
        Args:
            race_conditions: Current race conditions
            remaining_laps: Laps remaining in race
            
        Returns:
            List of tire strategy comparisons
        """
        current_compound = race_conditions.get('tire_compound', 'medium')
        track_temp = race_conditions.get('track_temp', 42)
        weather = race_conditions.get('weather', 'dry')
        
        strategies = []
        
        # Determine available compounds based on weather
        if weather in ['dry']:
            compounds = ['soft', 'medium', 'hard']
        elif weather in ['light_rain', 'mixed']:
            compounds = ['intermediate', 'medium']
        else:
            compounds = ['wet', 'intermediate']
        
        for compound in compounds:
            perf = self.tire_compound_performance[compound]
            
            # Calculate temperature delta
            temp_delta = abs(track_temp - perf['optimal_temp'])
            temp_factor = max(0.7, 1.0 - (temp_delta / 100))
            
            # Estimate lap time advantage
            base_lap_time = 90.0  # seconds
            compound_speed = perf['speed'] * temp_factor
            lap_time = base_lap_time / compound_speed
            
            # Estimate stint length
            max_stint = int(30 / perf['degradation'])
            viable_stint = min(max_stint, remaining_laps)
            
            # Calculate total time
            total_time = lap_time * viable_stint
            
            # Determine if pit stop needed
            needs_pit = viable_stint < remaining_laps
            if needs_pit:
                total_time += 22.0  # pit stop time
            
            # Calculate advantage vs current
            current_perf = self.tire_compound_performance[current_compound]
            current_lap_time = base_lap_time / (current_perf['speed'] * temp_factor)
            time_advantage = (current_lap_time - lap_time) * viable_stint
            
            strategies.append({
                'compound': compound,
                'lap_time': lap_time,
                'stint_length': viable_stint,
                'total_time': total_time,
                'time_advantage': time_advantage,
                'needs_pit': needs_pit,
                'degradation_rate': perf['degradation'],
                'speed_factor': compound_speed,
                'recommendation': self._get_compound_recommendation(
                    compound, time_advantage, viable_stint, remaining_laps
                )
            })
        
        # Sort by time advantage
        strategies.sort(key=lambda x: x['time_advantage'], reverse=True)
        
        return strategies
    
    def _get_compound_recommendation(self, compound: str, time_advantage: float,
                                    stint_length: int, remaining_laps: int) -> str:
        """Generate recommendation for tire compound"""
        if time_advantage > 5.0:
            return f"Highly recommended - {time_advantage:.1f}s advantage"
        elif time_advantage > 0:
            return f"Viable option - {time_advantage:.1f}s advantage"
        elif stint_length >= remaining_laps:
            return "Can finish race without additional stop"
        else:
            return f"Not optimal - {abs(time_advantage):.1f}s slower"
    
    def predict_undercut_overcut(self, race_conditions: Dict,
                                 opponent_tire_age: int) -> Dict:
        """
        Predict undercut/overcut opportunities
        
        Args:
            race_conditions: Current race conditions
            opponent_tire_age: Age of opponent's tires
            
        Returns:
            Undercut/overcut analysis
        """
        our_tire_age = race_conditions.get('tire_age', 0)
        gap_to_ahead = race_conditions.get('gap_to_leader', 10.0)
        
        # Tire delta advantage
        tire_delta = opponent_tire_age - our_tire_age
        
        # Estimate lap time gain with fresh tires
        lap_time_gain = 0.3 + (tire_delta * 0.05)  # seconds per lap
        
        # Pit stop time loss
        pit_time = 22.0  # seconds
        
        # Undercut calculation
        laps_to_recover_undercut = int(pit_time / lap_time_gain) + 1
        undercut_viable = (gap_to_ahead > pit_time - (lap_time_gain * 2))
        undercut_probability = min(0.95, max(0.1, 
            1.0 - (pit_time - gap_to_ahead) / 20.0))
        
        # Overcut calculation (staying out longer)
        overcut_advantage = tire_delta * 0.1  # seconds per lap
        overcut_laps = min(5, int(10 / (overcut_advantage + 0.1)))
        overcut_viable = tire_delta > 3 and our_tire_age < 15
        overcut_probability = min(0.85, max(0.1,
            tire_delta / 10.0))
        
        return {
            'undercut': {
                'viable': undercut_viable,
                'probability': undercut_probability,
                'laps_to_recover': laps_to_recover_undercut,
                'lap_time_gain': lap_time_gain,
                'recommendation': (
                    f"Undercut opportunity! Pit now to gain {lap_time_gain:.2f}s/lap"
                    if undercut_viable else
                    "Undercut not viable - gap too small"
                )
            },
            'overcut': {
                'viable': overcut_viable,
                'probability': overcut_probability,
                'optimal_laps': overcut_laps,
                'advantage_per_lap': overcut_advantage,
                'recommendation': (
                    f"Overcut possible - stay out {overcut_laps} more laps"
                    if overcut_viable else
                    "Overcut not recommended - tire age too high"
                )
            },
            'tire_delta': tire_delta,
            'gap_to_ahead': gap_to_ahead
        }
    
    def forecast_weather_probability(self, current_weather: str,
                                     track_temp: float,
                                     lap_number: int) -> Dict:
        """
        Forecast weather change probability
        
        Args:
            current_weather: Current weather condition
            track_temp: Track temperature
            lap_number: Current lap number
            
        Returns:
            Weather forecast analysis
        """
        # Simplified weather model
        weather_transitions = {
            'dry': {
                'dry': 0.85,
                'mixed': 0.10,
                'light_rain': 0.05,
                'heavy_rain': 0.00
            },
            'mixed': {
                'dry': 0.30,
                'mixed': 0.40,
                'light_rain': 0.25,
                'heavy_rain': 0.05
            },
            'light_rain': {
                'dry': 0.10,
                'mixed': 0.30,
                'light_rain': 0.45,
                'heavy_rain': 0.15
            },
            'heavy_rain': {
                'dry': 0.00,
                'mixed': 0.05,
                'light_rain': 0.35,
                'heavy_rain': 0.60
            }
        }
        
        current_probs = weather_transitions.get(current_weather, 
                                               weather_transitions['dry'])
        
        # Temperature influence
        if track_temp > 45:
            # Hot track - less likely to rain
            current_probs['dry'] = min(0.95, current_probs['dry'] * 1.2)
            current_probs['light_rain'] *= 0.5
        elif track_temp < 30:
            # Cool track - more likely to rain
            current_probs['light_rain'] = min(0.50, current_probs['light_rain'] * 1.5)
        
        # Normalize probabilities
        total = sum(current_probs.values())
        normalized = {k: v/total for k, v in current_probs.items()}
        
        # Determine most likely change
        sorted_weather = sorted(normalized.items(), key=lambda x: x[1], reverse=True)
        most_likely = sorted_weather[0][0]
        probability = sorted_weather[0][1]
        
        # Generate recommendation
        if most_likely != current_weather and probability > 0.3:
            recommendation = f"Weather likely to change to {most_likely} ({probability*100:.0f}% probability)"
            action = self._get_weather_action(current_weather, most_likely)
        else:
            recommendation = f"Weather stable - {current_weather} conditions continuing"
            action = "Maintain current tire strategy"
        
        return {
            'current': current_weather,
            'probabilities': normalized,
            'most_likely': most_likely,
            'change_probability': probability if most_likely != current_weather else 0,
            'recommendation': recommendation,
            'suggested_action': action,
            'confidence': probability
        }
    
    def _get_weather_action(self, current: str, predicted: str) -> str:
        """Get recommended action for weather change"""
        if predicted in ['light_rain', 'mixed'] and current == 'dry':
            return "Prepare for intermediate tires - pit window opening"
        elif predicted == 'heavy_rain':
            return "Wet tires required - plan pit stop immediately"
        elif predicted == 'dry' and current in ['light_rain', 'mixed']:
            return "Track drying - consider slick tires soon"
        else:
            return "Monitor weather closely"
    
    def estimate_race_outcome(self, race_conditions: Dict,
                             strategy: str) -> StrategyOutcome:
        """
        Estimate race outcome for a given strategy
        
        Args:
            race_conditions: Current race conditions
            strategy: Strategy to evaluate
            
        Returns:
            StrategyOutcome prediction
        """
        current_position = race_conditions.get('position', 5)
        tire_wear = race_conditions.get('tire_wear', 50)
        fuel_level = race_conditions.get('fuel_level', 70)
        lap_number = race_conditions.get('lap_number', 25)
        total_laps = race_conditions.get('total_laps', 50)
        
        remaining_laps = total_laps - lap_number
        
        # Base probability
        base_probability = 0.7
        
        # Strategy-specific adjustments
        if strategy == 'pit_now':
            if tire_wear > 80:
                position_change = 0  # Maintain position
                time_delta = -2.0  # Gain time with fresh tires
                risk = 0.2
                probability = 0.9
            else:
                position_change = -1  # Lose position
                time_delta = 5.0  # Lose time unnecessarily
                risk = 0.5
                probability = 0.6
        
        elif strategy == 'stay_out':
            if tire_wear < 70:
                position_change = 0.5  # Potential gain
                time_delta = -1.0
                risk = 0.3
                probability = 0.8
            else:
                position_change = -1.5  # Likely lose positions
                time_delta = 10.0
                risk = 0.8
                probability = 0.4
        
        elif strategy == 'push_hard':
            position_change = 0.3
            time_delta = -3.0
            risk = 0.6
            probability = 0.7
        
        else:  # conservative
            position_change = 0
            time_delta = 0
            risk = 0.2
            probability = 0.75
        
        expected_position = max(1, current_position + position_change)
        
        return StrategyOutcome(
            strategy_name=strategy,
            expected_position=expected_position,
            probability=probability,
            time_delta=time_delta,
            risk_score=risk,
            confidence=base_probability
        )
    
    def calculate_decision_factors(self, race_conditions: Dict,
                                   recommendation: Dict) -> Dict:
        """
        Calculate and weight decision factors for explainability
        
        Args:
            race_conditions: Current race conditions
            recommendation: AI recommendation
            
        Returns:
            Weighted decision factors
        """
        factors = {}
        
        # Tire wear factor
        tire_wear = race_conditions.get('tire_wear', 0)
        if tire_wear > 85:
            factors['tire_wear'] = {'weight': 0.40, 'impact': 'critical', 
                                   'value': tire_wear}
        elif tire_wear > 70:
            factors['tire_wear'] = {'weight': 0.25, 'impact': 'high',
                                   'value': tire_wear}
        else:
            factors['tire_wear'] = {'weight': 0.10, 'impact': 'low',
                                   'value': tire_wear}
        
        # Fuel level factor
        fuel_level = race_conditions.get('fuel_level', 100)
        if fuel_level < 20:
            factors['fuel_level'] = {'weight': 0.35, 'impact': 'critical',
                                    'value': fuel_level}
        elif fuel_level < 40:
            factors['fuel_level'] = {'weight': 0.15, 'impact': 'medium',
                                    'value': fuel_level}
        else:
            factors['fuel_level'] = {'weight': 0.05, 'impact': 'low',
                                    'value': fuel_level}
        
        # Race progress factor
        lap_number = race_conditions.get('lap_number', 0)
        total_laps = race_conditions.get('total_laps', 50)
        progress = lap_number / total_laps
        
        if 0.4 <= progress <= 0.7:
            factors['race_progress'] = {'weight': 0.20, 'impact': 'high',
                                       'value': progress * 100}
        else:
            factors['race_progress'] = {'weight': 0.10, 'impact': 'medium',
                                       'value': progress * 100}
        
        # Competitive position factor
        gap_behind = race_conditions.get('gap_to_behind', 10)
        if gap_behind < 2.0:
            factors['competitive_pressure'] = {'weight': 0.15, 'impact': 'high',
                                              'value': gap_behind}
        else:
            factors['competitive_pressure'] = {'weight': 0.05, 'impact': 'low',
                                              'value': gap_behind}
        
        # Weather factor
        weather = race_conditions.get('weather', 'dry')
        if weather in ['mixed', 'light_rain']:
            factors['weather'] = {'weight': 0.25, 'impact': 'high',
                                 'value': weather}
        else:
            factors['weather'] = {'weight': 0.05, 'impact': 'low',
                                 'value': weather}
        
        # Normalize weights
        total_weight = sum(f['weight'] for f in factors.values())
        for factor in factors.values():
            factor['normalized_weight'] = factor['weight'] / total_weight
        
        return factors

# Made with Bob
