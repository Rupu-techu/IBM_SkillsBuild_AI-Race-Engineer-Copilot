"""
Guided Demo Mode Component
Provides interactive demo experience with prebuilt scenarios
"""

import streamlit as st
from typing import Dict, Optional
from frontend.utils.simulation import RaceSimulator, create_demo_scenario
from frontend.components.ai_commentary import AICommentaryEngine, render_live_commentary_ticker
import time


class DemoController:
    """
    Controls guided demo experience
    """
    
    def __init__(self):
        self.scenarios = {
            "critical_tire_wear": {
                "title": "🛞 Critical Tire Wear",
                "description": "Experience high tire degradation requiring immediate pit stop decision",
                "duration": "2 minutes",
                "difficulty": "Medium"
            },
            "fuel_critical": {
                "title": "⛽ Fuel Emergency",
                "description": "Low fuel situation requiring strategic fuel management",
                "duration": "2 minutes",
                "difficulty": "High"
            },
            "weather_change": {
                "title": "🌧️ Weather Strategy",
                "description": "Rain approaching - make the right tire choice",
                "duration": "3 minutes",
                "difficulty": "High"
            },
            "safety_car": {
                "title": "🚨 Safety Car Opportunity",
                "description": "Strategic pit window opens during safety car period",
                "duration": "2 minutes",
                "difficulty": "Medium"
            },
            "optimal_strategy": {
                "title": "🎯 Perfect Strategy",
                "description": "Execute the optimal pit stop in ideal conditions",
                "duration": "2 minutes",
                "difficulty": "Easy"
            }
        }
    
    def render_scenario_selector(self) -> Optional[str]:
        """
        Render scenario selection interface
        
        Returns:
            Selected scenario key or None
        """
        
        st.markdown("## 🎬 DEMO MODE")
        st.markdown("Experience AI-powered race strategy in action with guided scenarios")
        st.markdown("---")
        
        # Scenario cards
        cols = st.columns(2)
        
        selected_scenario = None
        
        for idx, (key, scenario) in enumerate(self.scenarios.items()):
            col = cols[idx % 2]
            
            with col:
                with st.container():
                    st.markdown(f"""
                    <div style="
                        background: rgba(26, 26, 46, 0.8);
                        border: 2px solid #e63946;
                        border-radius: 10px;
                        padding: 20px;
                        margin: 10px 0;
                        cursor: pointer;
                        transition: all 0.3s;
                    ">
                        <h3 style="color: #e63946; margin: 0 0 10px 0;">{scenario['title']}</h3>
                        <p style="color: #ccc; font-size: 14px; margin: 10px 0;">
                            {scenario['description']}
                        </p>
                        <div style="display: flex; justify-content: space-between; margin-top: 15px;">
                            <span style="color: #888; font-size: 12px;">⏱️ {scenario['duration']}</span>
                            <span style="color: #888; font-size: 12px;">📊 {scenario['difficulty']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Start {scenario['title']}", key=f"start_{key}", use_container_width=True):
                        selected_scenario = key
        
        return selected_scenario
    
    def start_demo(self, scenario_key: str):
        """
        Start a demo scenario
        
        Args:
            scenario_key: Key of the scenario to start
        """
        
        # Initialize demo state
        st.session_state.demo_active = True
        st.session_state.demo_scenario = scenario_key
        st.session_state.demo_step = 0
        
        # Load scenario
        scenario_data = create_demo_scenario(scenario_key)
        st.session_state.demo_conditions = scenario_data['conditions']
        
        # Show intro
        st.success(f"🎬 Demo Started: {scenario_data['name']}")
        st.info(scenario_data['description'])


def render_demo_controls():
    """Render demo playback controls"""
    
    if not st.session_state.get('demo_active'):
        return
    
    st.markdown("### 🎮 Demo Controls")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("▶️ Play", use_container_width=True):
            st.session_state.demo_playing = True
    
    with col2:
        if st.button("⏸️ Pause", use_container_width=True):
            st.session_state.demo_playing = False
    
    with col3:
        if st.button("⏭️ Next Lap", use_container_width=True):
            if 'simulator' in st.session_state:
                st.session_state.simulator.advance_lap()
                st.rerun()
    
    with col4:
        if st.button("⏹️ Stop Demo", use_container_width=True):
            st.session_state.demo_active = False
            st.session_state.demo_playing = False
            st.rerun()


def render_demo_timeline():
    """Render demo progress timeline"""
    
    if not st.session_state.get('demo_active'):
        return
    
    st.markdown("### 📊 Demo Timeline")
    
    # Get current demo state
    scenario_key = st.session_state.get('demo_scenario', '')
    current_lap = st.session_state.get('simulation_data', {}).get('lap', 1)
    total_laps = st.session_state.get('simulation_data', {}).get('total_laps', 50)
    
    # Progress bar
    progress = (current_lap / total_laps) * 100
    
    st.markdown(f"""
    <div style="
        background: rgba(26, 26, 46, 0.8);
        border: 2px solid #e63946;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    ">
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span style="color: #06ffa5; font-weight: bold;">Lap {current_lap} / {total_laps}</span>
            <span style="color: #ffd60a;">{progress:.0f}% Complete</span>
        </div>
        <div style="
            background: rgba(100, 100, 100, 0.3);
            height: 20px;
            border-radius: 10px;
            overflow: hidden;
        ">
            <div style="
                background: linear-gradient(90deg, #e63946 0%, #f77f00 100%);
                height: 100%;
                width: {progress}%;
                transition: width 0.5s ease;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_demo_instructions(scenario_key: str):
    """
    Render step-by-step demo instructions
    
    Args:
        scenario_key: Current scenario key
    """
    
    instructions = {
        "critical_tire_wear": [
            "🔍 Observe the high tire wear (87%) in the telemetry panel",
            "🤖 Click 'ANALYZE STRATEGY' to get AI recommendation",
            "📊 Review the tire degradation chart showing critical levels",
            "✅ AI should recommend immediate pit stop",
            "🎯 Note the confidence score and risk assessment"
        ],
        "fuel_critical": [
            "⛽ Check the low fuel level (18%) in the sidebar",
            "🤖 Request AI strategy analysis",
            "📈 View fuel consumption projection",
            "🚨 AI will flag critical fuel situation",
            "🔧 Understand the pit stop urgency"
        ],
        "weather_change": [
            "🌧️ Notice the 'mixed' weather conditions",
            "🤖 Analyze strategy with AI",
            "📊 Check weather impact on tire choice",
            "🛞 AI recommends intermediate tires",
            "⏱️ Timing is critical for weather changes"
        ],
        "safety_car": [
            "🚨 Safety car is deployed (check track status)",
            "🤖 Get AI recommendation for this opportunity",
            "📊 Review pit strategy timing windows",
            "✅ Safety car creates strategic advantage",
            "🎯 Understand the risk vs reward"
        ],
        "optimal_strategy": [
            "📊 Review all telemetry indicators",
            "🤖 Request comprehensive AI analysis",
            "📈 Explore all visualization tabs",
            "🔄 Compare alternative strategies",
            "✅ Execute optimal pit stop timing"
        ]
    }
    
    st.markdown("### 📋 Demo Guide")
    
    steps = instructions.get(scenario_key, [])
    
    for idx, step in enumerate(steps, 1):
        completed = st.session_state.get('demo_step', 0) >= idx
        
        if completed:
            icon = "✅"
            color = "#06ffa5"
        else:
            icon = "⭕"
            color = "#888"
        
        st.markdown(f"""
        <div style="
            color: {color};
            padding: 10px;
            margin: 5px 0;
            border-left: 3px solid {color};
            background: rgba(26, 26, 46, 0.5);
        ">
            {icon} <strong>Step {idx}:</strong> {step}
        </div>
        """, unsafe_allow_html=True)


def render_demo_highlights():
    """Render key demo highlights and learning points"""
    
    st.markdown("### 💡 Key Takeaways")
    
    highlights = [
        {
            "title": "AI-Powered Decision Making",
            "description": "IBM Granite analyzes complex race data in real-time",
            "icon": "🤖"
        },
        {
            "title": "Explainable AI",
            "description": "Every recommendation includes clear reasoning",
            "icon": "💡"
        },
        {
            "title": "Risk Assessment",
            "description": "Confidence scores and risk levels for informed decisions",
            "icon": "📊"
        },
        {
            "title": "Multiple Strategies",
            "description": "Compare alternatives and understand trade-offs",
            "icon": "🔄"
        }
    ]
    
    cols = st.columns(2)
    
    for idx, highlight in enumerate(highlights):
        col = cols[idx % 2]
        
        with col:
            st.markdown(f"""
            <div style="
                background: rgba(26, 26, 46, 0.8);
                border: 2px solid #06ffa5;
                border-radius: 10px;
                padding: 15px;
                margin: 10px 0;
            ">
                <div style="font-size: 32px; margin-bottom: 10px;">{highlight['icon']}</div>
                <h4 style="color: #06ffa5; margin: 0 0 10px 0;">{highlight['title']}</h4>
                <p style="color: #ccc; font-size: 13px; margin: 0;">
                    {highlight['description']}
                </p>
            </div>
            """, unsafe_allow_html=True)


def auto_advance_demo():
    """Automatically advance demo if playing"""
    
    if not st.session_state.get('demo_playing'):
        return
    
    if not st.session_state.get('demo_active'):
        return
    
    # Advance simulation
    if 'simulator' in st.session_state:
        time.sleep(2)  # 2 second delay between laps
        st.session_state.simulator.advance_lap()
        st.rerun()

# Made with Bob
