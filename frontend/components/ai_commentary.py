"""
AI Commentary System
Generates authentic F1-style race engineer communications using IBM Granite
"""

import streamlit as st
from typing import Dict, List
from src.ai.granite_engine import GraniteEngine


class AICommentaryEngine:
    """
    Generates F1-style race engineer commentary using IBM Granite
    """
    
    def __init__(self, granite_engine: GraniteEngine):
        self.granite_engine = granite_engine
        self.commentary_history: List[Dict] = []
    
    def generate_race_commentary(self, race_conditions: Dict, event_type: str = "normal") -> str:
        """
        Generate race engineer commentary
        
        Args:
            race_conditions: Current race conditions
            event_type: Type of event (normal, critical, emergency, overtake, pit)
            
        Returns:
            Commentary string in F1 engineer style
        """
        
        prompt = self._build_commentary_prompt(race_conditions, event_type)
        
        try:
            if self.granite_engine.model:
                commentary = self.granite_engine.model.generate_text(prompt=prompt)
            else:
                commentary = self._generate_fallback_commentary(race_conditions, event_type)
        except:
            commentary = self._generate_fallback_commentary(race_conditions, event_type)
        
        # Store in history
        self.commentary_history.append({
            "lap": race_conditions.get("lap_number"),
            "type": event_type,
            "commentary": commentary
        })
        
        return commentary
    
    def _build_commentary_prompt(self, race_conditions: Dict, event_type: str) -> str:
        """Build prompt for commentary generation"""
        
        base_prompt = f"""You are a Formula 1 race engineer communicating with your driver over team radio.

Current Race Situation:
- Lap {race_conditions.get('lap_number')} of {race_conditions.get('total_laps')}
- Position: P{race_conditions.get('position')}
- Tire: {race_conditions.get('tire_compound')} ({race_conditions.get('tire_age')} laps old, {race_conditions.get('tire_wear')}% wear)
- Fuel: {race_conditions.get('fuel_level')}%
- Gap to leader: +{race_conditions.get('gap_to_leader')}s
- Gap behind: +{race_conditions.get('gap_to_behind')}s
- Weather: {race_conditions.get('weather')}

"""
        
        if event_type == "critical":
            base_prompt += """Generate a CRITICAL radio message (1-2 sentences) about an urgent situation requiring immediate action.
Use professional F1 terminology. Be direct and clear. Example tone: "Box box box, critical tire wear detected."

Message:"""
        
        elif event_type == "emergency":
            base_prompt += """Generate an EMERGENCY radio message (1 sentence) about a critical safety situation.
Be extremely direct and urgent. Example: "Safety car deployed, hold position."

Message:"""
        
        elif event_type == "overtake":
            base_prompt += """Generate a radio message (1-2 sentences) about an overtaking opportunity or threat.
Use tactical language. Example: "DRS available, gap is 0.8 seconds, prepare to attack."

Message:"""
        
        elif event_type == "pit":
            base_prompt += """Generate a pit stop radio message (1-2 sentences) confirming strategy.
Be clear and professional. Example: "Box this lap, box this lap. Confirm."

Message:"""
        
        elif event_type == "strategy":
            base_prompt += """Generate a strategy update radio message (2-3 sentences) explaining the race plan.
Be informative and confident. Example: "Plan A is working well. We'll extend this stint 5 more laps, then box for hards."

Message:"""
        
        else:  # normal
            base_prompt += """Generate a standard radio message (1-2 sentences) with a race update or encouragement.
Be professional and supportive. Example: "Good pace, you're matching the leader. Keep it up."

Message:"""
        
        return base_prompt
    
    def _generate_fallback_commentary(self, race_conditions: Dict, event_type: str) -> str:
        """Generate fallback commentary when Granite is unavailable"""
        
        lap = race_conditions.get('lap_number')
        position = race_conditions.get('position')
        tire_wear = race_conditions.get('tire_wear', 0)
        fuel = race_conditions.get('fuel_level', 100)
        gap_behind = race_conditions.get('gap_to_behind', 0)
        
        if event_type == "critical":
            if tire_wear > 85:
                return f"Box box box! Tire wear critical at {tire_wear:.0f}%. Pit this lap."
            elif fuel < 20:
                return f"Fuel critical at {fuel:.0f}%. Box this lap for splash and dash."
            else:
                return "Critical situation detected. Prepare for immediate action."
        
        elif event_type == "emergency":
            return "Safety car deployed. Hold position, maintain delta."
        
        elif event_type == "overtake":
            if gap_behind < 1.0:
                return f"Car behind closing fast, gap {gap_behind:.1f}s. Defend into turn 1."
            else:
                return "DRS available next lap. Prepare to attack."
        
        elif event_type == "pit":
            return f"Box this lap, box this lap. {race_conditions.get('tire_compound', 'medium')} tires ready. Confirm."
        
        elif event_type == "strategy":
            return f"P{position}, lap {lap}. Strategy on track. Tire wear {tire_wear:.0f}%, fuel {fuel:.0f}%."
        
        else:  # normal
            if tire_wear < 50:
                return f"Good pace. P{position}, tire wear looking good at {tire_wear:.0f}%."
            elif tire_wear < 75:
                return f"P{position}, managing tires well. Wear at {tire_wear:.0f}%."
            else:
                return f"P{position}, tire wear increasing. Monitor closely."
    
    def generate_strategy_callout(self, recommendation: Dict) -> str:
        """
        Generate strategy callout based on AI recommendation
        
        Args:
            recommendation: Strategy recommendation dictionary
            
        Returns:
            Strategy callout string
        """
        action = recommendation.get('action', 'unknown')
        confidence = recommendation.get('confidence', 0) * 100
        
        callouts = {
            'pit_now': f"📻 BOX BOX BOX! Pit entry open. {confidence:.0f}% confidence in this call.",
            'pit_next_lap': f"📻 Box next lap. Prepare for pit stop. {confidence:.0f}% confidence.",
            'stay_out': f"📻 Stay out, stay out. Strategy on track. {confidence:.0f}% confidence.",
            'push_hard': f"📻 Push now! We need pace. {confidence:.0f}% confidence in this strategy.",
            'conserve_tires': f"📻 Manage tires, manage tires. Long stint ahead. {confidence:.0f}% confidence.",
            'overtake_opportunity': f"📻 Attack mode! DRS available. {confidence:.0f}% confidence."
        }
        
        return callouts.get(action, f"📻 Strategy update: {action.replace('_', ' ')}. {confidence:.0f}% confidence.")
    
    def generate_event_commentary(self, event: Dict) -> str:
        """
        Generate commentary for race events
        
        Args:
            event: Event dictionary with type and description
            
        Returns:
            Commentary string
        """
        event_type = event.get('event_type', 'normal')
        severity = event.get('severity', 'low')
        
        if severity == "critical":
            prefix = "🚨 CRITICAL:"
        elif severity == "high":
            prefix = "⚠️ ALERT:"
        elif severity == "medium":
            prefix = "📢 UPDATE:"
        else:
            prefix = "ℹ️ INFO:"
        
        return f"{prefix} {event.get('description', 'Race event occurred')}"
    
    def get_commentary_history(self, count: int = 5) -> List[Dict]:
        """
        Get recent commentary history
        
        Args:
            count: Number of recent messages to return
            
        Returns:
            List of commentary dictionaries
        """
        return self.commentary_history[-count:] if self.commentary_history else []


def render_commentary_feed(commentary_engine: AICommentaryEngine):
    """
    Render live commentary feed component
    
    Args:
        commentary_engine: AICommentaryEngine instance
    """
    
    st.markdown("### 📻 RACE ENGINEER RADIO")
    
    # Get recent commentary
    recent_commentary = commentary_engine.get_commentary_history(5)
    
    if not recent_commentary:
        st.info("🎙️ Awaiting race engineer communications...")
        return
    
    # Display commentary feed (newest first)
    for comm in reversed(recent_commentary):
        lap = comm.get('lap', 0)
        comm_type = comm.get('type', 'normal')
        message = comm.get('commentary', '')
        
        # Color coding based on type
        if comm_type == "critical" or comm_type == "emergency":
            border_color = "#e63946"
            bg_color = "rgba(230, 57, 70, 0.1)"
        elif comm_type == "overtake":
            border_color = "#f77f00"
            bg_color = "rgba(247, 127, 0, 0.1)"
        elif comm_type == "pit":
            border_color = "#ffd60a"
            bg_color = "rgba(255, 214, 10, 0.1)"
        else:
            border_color = "#06ffa5"
            bg_color = "rgba(6, 255, 165, 0.1)"
        
        st.markdown(f"""
        <div style="
            border-left: 4px solid {border_color};
            background: {bg_color};
            padding: 12px;
            margin: 8px 0;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
        ">
            <div style="color: #888; font-size: 11px; margin-bottom: 5px;">
                LAP {lap} | {comm_type.upper()}
            </div>
            <div style="color: white; font-size: 14px; line-height: 1.4;">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_live_commentary_ticker(message: str):
    """
    Render a live commentary ticker at the top of the screen
    
    Args:
        message: Commentary message to display
    """
    
    st.markdown(f"""
    <div class="animate-slide-in-up" style="
        background: linear-gradient(90deg, #e63946 0%, #f77f00 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        margin: 10px 0;
        font-family: 'Courier New', monospace;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 4px 6px rgba(230, 57, 70, 0.3);
        animation: glow-pulse 2s ease-in-out infinite;
    ">
        📻 RACE ENGINEER: {message}
    </div>
    """, unsafe_allow_html=True)

# Made with Bob
