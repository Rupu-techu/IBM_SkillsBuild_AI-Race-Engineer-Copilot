"""
Real-time race simulation engine
Simulates live telemetry updates and race events
"""

import time
import random
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import streamlit as st


class RaceEvent(Enum):
    """Types of race events"""
    NORMAL = "normal"
    SAFETY_CAR = "safety_car"
    VIRTUAL_SAFETY_CAR = "vsc"
    YELLOW_FLAG = "yellow_flag"
    RED_FLAG = "red_flag"
    WEATHER_CHANGE = "weather_change"
    TIRE_DEGRADATION = "tire_degradation"
    OVERTAKE = "overtake"
    PIT_STOP = "pit_stop"


@dataclass
class SimulationEvent:
    """Simulation event data"""
    lap: int
    event_type: RaceEvent
    description: str
    impact: str
    severity: str  # "low", "medium", "high", "critical"


class RaceSimulator:
    """
    Real-time race simulation engine
    Generates dynamic telemetry and race events
    """
    
    def __init__(self):
        self.current_lap = 1
        self.is_running = False
        self.events_history: List[SimulationEvent] = []
        self.base_tire_degradation_rate = 2.5
        self.base_fuel_consumption_rate = 2.0
    
    def start_simulation(self, initial_conditions: Dict):
        """
        Start race simulation
        
        Args:
            initial_conditions: Starting race conditions
        """
        self.is_running = True
        self.current_lap = initial_conditions.get('lap_number', 1)
        
        # Initialize session state for simulation
        if 'simulation_data' not in st.session_state:
            st.session_state.simulation_data = {
                'lap': self.current_lap,
                'tire_wear': initial_conditions.get('tire_wear', 0),
                'fuel_level': initial_conditions.get('fuel_level', 100),
                'position': initial_conditions.get('position', 3),
                'tire_age': initial_conditions.get('tire_age', 0),
                'weather': initial_conditions.get('weather', 'dry'),
                'track_temp': initial_conditions.get('track_temp', 42),
                'gap_to_leader': initial_conditions.get('gap_to_leader', 8.5),
                'gap_to_behind': initial_conditions.get('gap_to_behind', 3.2),
                'events': []
            }
    
    def advance_lap(self) -> Dict:
        """
        Advance simulation by one lap
        
        Returns:
            Updated race conditions
        """
        if not st.session_state.get('simulation_data'):
            return {}
        
        data = st.session_state.simulation_data
        
        # Increment lap
        data['lap'] += 1
        data['tire_age'] += 1
        
        # Update tire wear (with randomness)
        degradation = self.base_tire_degradation_rate * (1 + random.uniform(-0.2, 0.3))
        # Exponential degradation as tires age
        degradation *= (1 + (data['tire_age'] * 0.05))
        data['tire_wear'] = min(100, data['tire_wear'] + degradation)
        
        # Update fuel consumption
        fuel_used = self.base_fuel_consumption_rate * random.uniform(0.9, 1.1)
        data['fuel_level'] = max(0, data['fuel_level'] - fuel_used)
        
        # Update gaps (with randomness)
        data['gap_to_leader'] += random.uniform(-0.3, 0.5)
        data['gap_to_behind'] += random.uniform(-0.4, 0.4)
        data['gap_to_behind'] = max(0.1, data['gap_to_behind'])
        
        # Track temperature variation
        data['track_temp'] += random.uniform(-1, 1)
        
        # Generate random events
        event = self._generate_random_event(data)
        if event:
            data['events'].append(event)
            self.events_history.append(event)
        
        st.session_state.simulation_data = data
        return data
    
    def _generate_random_event(self, current_data: Dict) -> Optional[SimulationEvent]:
        """
        Generate random race events
        
        Args:
            current_data: Current simulation data
            
        Returns:
            SimulationEvent or None
        """
        # Event probability (10% chance per lap)
        if random.random() > 0.1:
            return None
        
        lap = current_data['lap']
        
        # Weighted event selection
        events = [
            (RaceEvent.TIRE_DEGRADATION, 0.3),
            (RaceEvent.WEATHER_CHANGE, 0.15),
            (RaceEvent.SAFETY_CAR, 0.1),
            (RaceEvent.VIRTUAL_SAFETY_CAR, 0.15),
            (RaceEvent.YELLOW_FLAG, 0.15),
            (RaceEvent.OVERTAKE, 0.15)
        ]
        
        event_type = random.choices(
            [e[0] for e in events],
            weights=[e[1] for e in events]
        )[0]
        
        # Generate event details
        if event_type == RaceEvent.SAFETY_CAR:
            current_data['track_conditions'] = 'safety_car'
            return SimulationEvent(
                lap=lap,
                event_type=event_type,
                description="🚨 SAFETY CAR DEPLOYED - Incident on track",
                impact="Pit window opportunity. Consider strategy change.",
                severity="high"
            )
        
        elif event_type == RaceEvent.VIRTUAL_SAFETY_CAR:
            return SimulationEvent(
                lap=lap,
                event_type=event_type,
                description="⚠️ VIRTUAL SAFETY CAR - Debris on track",
                impact="Reduced pace. Potential pit stop advantage.",
                severity="medium"
            )
        
        elif event_type == RaceEvent.WEATHER_CHANGE:
            new_weather = random.choice(['light_rain', 'mixed'])
            current_data['weather'] = new_weather
            return SimulationEvent(
                lap=lap,
                event_type=event_type,
                description=f"🌧️ WEATHER CHANGE - Conditions now {new_weather.replace('_', ' ')}",
                impact="Consider tire change to intermediates.",
                severity="high"
            )
        
        elif event_type == RaceEvent.TIRE_DEGRADATION:
            # Accelerate tire wear
            current_data['tire_wear'] = min(100, current_data['tire_wear'] + 5)
            return SimulationEvent(
                lap=lap,
                event_type=event_type,
                description="🛞 INCREASED TIRE DEGRADATION - High wear detected",
                impact="Tire performance declining rapidly.",
                severity="medium"
            )
        
        elif event_type == RaceEvent.OVERTAKE:
            if current_data['gap_to_behind'] < 2.0:
                return SimulationEvent(
                    lap=lap,
                    event_type=event_type,
                    description="🎯 OVERTAKE THREAT - Car behind closing in",
                    impact="Defend position or increase pace.",
                    severity="medium"
                )
        
        elif event_type == RaceEvent.YELLOW_FLAG:
            return SimulationEvent(
                lap=lap,
                event_type=event_type,
                description="🟡 YELLOW FLAG - Sector 2",
                impact="Reduced pace in affected sector.",
                severity="low"
            )
        
        return None
    
    def trigger_pit_stop(self, tire_compound: str) -> Dict:
        """
        Simulate a pit stop
        
        Args:
            tire_compound: New tire compound
            
        Returns:
            Updated race conditions
        """
        if not st.session_state.get('simulation_data'):
            return {}
        
        data = st.session_state.simulation_data
        
        # Reset tire metrics
        data['tire_wear'] = 0
        data['tire_age'] = 0
        data['tire_compound'] = tire_compound
        
        # Refuel
        data['fuel_level'] = min(100, data['fuel_level'] + 30)
        
        # Pit stop time loss (positions)
        pit_time_loss = random.uniform(20, 25)  # seconds
        # Approximate position loss (rough calculation)
        if data['gap_to_behind'] < pit_time_loss:
            data['position'] = min(20, data['position'] + 1)
            data['gap_to_behind'] = random.uniform(0.5, 2.0)
        
        # Add pit stop event
        event = SimulationEvent(
            lap=data['lap'],
            event_type=RaceEvent.PIT_STOP,
            description=f"🔧 PIT STOP COMPLETE - {tire_compound.upper()} tires fitted",
            impact=f"Pit time: {pit_time_loss:.1f}s. Fresh tires advantage.",
            severity="low"
        )
        data['events'].append(event)
        self.events_history.append(event)
        
        st.session_state.simulation_data = data
        return data
    
    def get_current_state(self) -> Dict:
        """Get current simulation state"""
        return st.session_state.get('simulation_data', {})
    
    def get_recent_events(self, count: int = 5) -> List[SimulationEvent]:
        """
        Get recent race events
        
        Args:
            count: Number of recent events to return
            
        Returns:
            List of recent SimulationEvents
        """
        return self.events_history[-count:] if self.events_history else []
    
    def stop_simulation(self):
        """Stop the simulation"""
        self.is_running = False
    
    def reset_simulation(self):
        """Reset simulation to initial state"""
        self.is_running = False
        self.current_lap = 1
        self.events_history = []
        if 'simulation_data' in st.session_state:
            del st.session_state.simulation_data


def create_demo_scenario(scenario_name: str) -> Dict:
    """
    Create predefined demo scenarios
    
    Args:
        scenario_name: Name of the scenario
        
    Returns:
        Race conditions dictionary
    """
    scenarios = {
        "critical_tire_wear": {
            "name": "Critical Tire Wear",
            "description": "High tire degradation requiring immediate pit stop",
            "conditions": {
                "lap_number": 28,
                "total_laps": 50,
                "tire_wear": 87,
                "tire_compound": "medium",
                "tire_age": 19,
                "fuel_level": 62,
                "weather": "dry",
                "track_temp": 45,
                "air_temp": 28,
                "position": 3,
                "gap_to_leader": 9.2,
                "gap_to_behind": 4.1,
                "track_conditions": "green"
            }
        },
        "fuel_critical": {
            "name": "Fuel Critical",
            "description": "Low fuel requiring immediate attention",
            "conditions": {
                "lap_number": 42,
                "total_laps": 50,
                "tire_wear": 65,
                "tire_compound": "hard",
                "tire_age": 12,
                "fuel_level": 18,
                "weather": "dry",
                "track_temp": 43,
                "air_temp": 27,
                "position": 4,
                "gap_to_leader": 15.8,
                "gap_to_behind": 2.3,
                "track_conditions": "green"
            }
        },
        "weather_change": {
            "name": "Weather Change",
            "description": "Rain approaching, tire strategy decision needed",
            "conditions": {
                "lap_number": 20,
                "total_laps": 50,
                "tire_wear": 55,
                "tire_compound": "soft",
                "tire_age": 10,
                "fuel_level": 75,
                "weather": "mixed",
                "track_temp": 38,
                "air_temp": 24,
                "position": 2,
                "gap_to_leader": 3.5,
                "gap_to_behind": 5.8,
                "track_conditions": "green"
            }
        },
        "safety_car": {
            "name": "Safety Car Opportunity",
            "description": "Safety car deployed, strategic pit window open",
            "conditions": {
                "lap_number": 32,
                "total_laps": 50,
                "tire_wear": 72,
                "tire_compound": "medium",
                "tire_age": 15,
                "fuel_level": 58,
                "weather": "dry",
                "track_temp": 44,
                "air_temp": 27,
                "position": 5,
                "gap_to_leader": 18.5,
                "gap_to_behind": 1.2,
                "track_conditions": "safety_car"
            }
        },
        "optimal_strategy": {
            "name": "Optimal Strategy Window",
            "description": "Perfect conditions for planned pit stop",
            "conditions": {
                "lap_number": 25,
                "total_laps": 50,
                "tire_wear": 68,
                "tire_compound": "medium",
                "tire_age": 14,
                "fuel_level": 70,
                "weather": "dry",
                "track_temp": 42,
                "air_temp": 26,
                "position": 3,
                "gap_to_leader": 8.5,
                "gap_to_behind": 3.2,
                "track_conditions": "green"
            }
        }
    }
    
    return scenarios.get(scenario_name, scenarios["optimal_strategy"])

# Made with Bob
