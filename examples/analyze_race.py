"""
Example: Race Strategy Analysis
Demonstrates how to use the AI Race Engineer Copilot
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.race_analyzer import (
    RaceAnalyzer, 
    RaceConditions, 
    TireCompound, 
    WeatherCondition
)
from src.ai.granite_engine import GraniteEngine


def print_separator():
    """Print a visual separator"""
    print("\n" + "="*80 + "\n")


def analyze_scenario_1():
    """Scenario 1: Critical tire degradation during mid-race"""
    print("🏎️  SCENARIO 1: Critical Tire Degradation")
    print_separator()
    
    # Create race conditions
    conditions = RaceConditions(
        lap_number=28,
        total_laps=50,
        tire_wear=87.5,
        tire_compound=TireCompound.MEDIUM,
        tire_age=18,
        weather=WeatherCondition.DRY,
        track_temp=45.0,
        air_temp=28.0,
        position=3,
        fuel_level=62.0,
        gap_to_leader=12.3,
        gap_to_behind=4.8,
        track_conditions="green"
    )
    
    # Analyze strategy
    analyzer = RaceAnalyzer()
    recommendation = analyzer.analyze_strategy(conditions)
    
    # Print results
    print("📊 Race Conditions:")
    print(f"   Lap: {conditions.lap_number}/{conditions.total_laps}")
    print(f"   Position: P{conditions.position}")
    print(f"   Tire: {conditions.tire_compound.value} ({conditions.tire_age} laps, {conditions.tire_wear}% wear)")
    print(f"   Fuel: {conditions.fuel_level}%")
    print(f"   Weather: {conditions.weather.value}")
    print(f"   Track Temp: {conditions.track_temp}°C")
    
    print("\n🎯 AI Recommendation:")
    print(f"   Action: {recommendation.action.value.upper()}")
    print(f"   Confidence: {recommendation.confidence*100:.0f}%")
    print(f"   Risk Level: {recommendation.risk_level.upper()}")
    
    print(f"\n💡 Reasoning:")
    print(f"   {recommendation.reasoning}")
    
    print(f"\n🎲 Expected Outcome:")
    print(f"   {recommendation.expected_outcome}")
    
    if recommendation.tire_recommendation:
        print(f"\n🛞 Tire Recommendation: {recommendation.tire_recommendation.value.upper()}")
    
    # Get AI explanation
    ai_engine = GraniteEngine()
    explanation = ai_engine.explain_decision(
        recommendation.to_dict(),
        conditions.to_dict()
    )
    
    print(f"\n🤖 IBM Granite Explanation:")
    print(f"   {explanation}")
    
    print_separator()


def analyze_scenario_2():
    """Scenario 2: Weather changing to rain"""
    print("🏎️  SCENARIO 2: Weather Change - Rain Approaching")
    print_separator()
    
    conditions = RaceConditions(
        lap_number=15,
        total_laps=50,
        tire_wear=45.0,
        tire_compound=TireCompound.SOFT,
        tire_age=8,
        weather=WeatherCondition.LIGHT_RAIN,
        track_temp=32.0,
        air_temp=22.0,
        position=5,
        fuel_level=78.0,
        gap_to_leader=18.5,
        gap_to_behind=2.1,
        track_conditions="green"
    )
    
    analyzer = RaceAnalyzer()
    recommendation = analyzer.analyze_strategy(conditions)
    
    print("📊 Race Conditions:")
    print(f"   Lap: {conditions.lap_number}/{conditions.total_laps}")
    print(f"   Position: P{conditions.position}")
    print(f"   Tire: {conditions.tire_compound.value} ({conditions.tire_age} laps, {conditions.tire_wear}% wear)")
    print(f"   Weather: {conditions.weather.value} ⚠️")
    print(f"   Track Temp: {conditions.track_temp}°C (cooling)")
    
    print("\n🎯 AI Recommendation:")
    print(f"   Action: {recommendation.action.value.upper()}")
    print(f"   Confidence: {recommendation.confidence*100:.0f}%")
    print(f"   Risk Level: {recommendation.risk_level.upper()}")
    
    print(f"\n💡 Reasoning:")
    print(f"   {recommendation.reasoning}")
    
    if recommendation.tire_recommendation:
        print(f"\n🛞 Tire Recommendation: {recommendation.tire_recommendation.value.upper()}")
    
    print_separator()


def analyze_scenario_3():
    """Scenario 3: Under pressure from behind"""
    print("🏎️  SCENARIO 3: Defending Position - Car Behind Closing")
    print_separator()
    
    conditions = RaceConditions(
        lap_number=35,
        total_laps=50,
        tire_wear=68.0,
        tire_compound=TireCompound.HARD,
        tire_age=12,
        weather=WeatherCondition.DRY,
        track_temp=48.0,
        air_temp=30.0,
        position=2,
        fuel_level=45.0,
        gap_to_leader=5.2,
        gap_to_behind=0.8,  # Critical gap!
        track_conditions="green"
    )
    
    analyzer = RaceAnalyzer()
    recommendation = analyzer.analyze_strategy(conditions)
    
    print("📊 Race Conditions:")
    print(f"   Lap: {conditions.lap_number}/{conditions.total_laps}")
    print(f"   Position: P{conditions.position}")
    print(f"   Gap to Leader: +{conditions.gap_to_leader}s")
    print(f"   Gap to Behind: +{conditions.gap_to_behind}s ⚠️ CRITICAL")
    print(f"   Tire: {conditions.tire_compound.value} ({conditions.tire_wear}% wear)")
    
    print("\n🎯 AI Recommendation:")
    print(f"   Action: {recommendation.action.value.upper()}")
    print(f"   Confidence: {recommendation.confidence*100:.0f}%")
    print(f"   Risk Level: {recommendation.risk_level.upper()}")
    
    print(f"\n💡 Reasoning:")
    print(f"   {recommendation.reasoning}")
    
    print(f"\n⏱️  Timing Window:")
    print(f"   {recommendation.timing_window}")
    
    print_separator()


def analyze_undercut_opportunity():
    """Demonstrate undercut calculation"""
    print("🏎️  UNDERCUT OPPORTUNITY ANALYSIS")
    print_separator()
    
    conditions = RaceConditions(
        lap_number=22,
        total_laps=50,
        tire_wear=72.0,
        tire_compound=TireCompound.MEDIUM,
        tire_age=14,
        weather=WeatherCondition.DRY,
        track_temp=44.0,
        air_temp=27.0,
        position=4,
        fuel_level=68.0,
        gap_to_leader=15.8,
        gap_to_behind=6.2,
        track_conditions="green"
    )
    
    analyzer = RaceAnalyzer()
    
    # Competitor ahead has older tires
    competitor_tire_age = 20
    
    undercut_analysis = analyzer.calculate_undercut_opportunity(
        conditions, 
        competitor_tire_age
    )
    
    print("📊 Undercut Analysis:")
    print(f"   Your tire age: {conditions.tire_age} laps")
    print(f"   Competitor tire age: {competitor_tire_age} laps")
    print(f"   Tire delta: {competitor_tire_age - conditions.tire_age} laps")
    
    print(f"\n⚡ Undercut Viability:")
    print(f"   Is Viable: {'✅ YES' if undercut_analysis['is_viable'] else '❌ NO'}")
    print(f"   Time gain per lap: {undercut_analysis['time_gain_per_lap']:.2f}s")
    print(f"   Laps to recover: {undercut_analysis['laps_to_recover']}")
    print(f"   Laps remaining: {undercut_analysis['laps_remaining']}")
    print(f"   Confidence: {undercut_analysis['confidence']*100:.0f}%")
    
    print(f"\n🎯 Recommendation:")
    print(f"   {undercut_analysis['recommendation']}")
    
    print_separator()


def main():
    """Run all example scenarios"""
    print("\n" + "🏁"*40)
    print("AI RACE ENGINEER COPILOT - DEMO")
    print("IBM SkillsBuild AI Builders Challenge")
    print("🏁"*40 + "\n")
    
    try:
        # Run scenarios
        analyze_scenario_1()
        input("Press Enter to continue to next scenario...")
        
        analyze_scenario_2()
        input("Press Enter to continue to next scenario...")
        
        analyze_scenario_3()
        input("Press Enter to continue to undercut analysis...")
        
        analyze_undercut_opportunity()
        
        print("\n✅ Demo completed successfully!")
        print("\n💡 Next Steps:")
        print("   1. Set up IBM watsonx.ai credentials in .env file")
        print("   2. Install dependencies: pip install -r requirements.txt")
        print("   3. Run the API server: python src/api/main.py")
        print("   4. Explore Langflow workflows in src/workflows/")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

# Made with Bob
