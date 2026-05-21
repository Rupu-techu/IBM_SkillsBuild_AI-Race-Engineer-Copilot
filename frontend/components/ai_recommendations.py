"""
AI Recommendations component using IBM Granite
"""

import streamlit as st
from src.core.race_analyzer import RaceConditions, RaceAnalyzer
from src.ai.granite_engine import GraniteEngine


def render_ai_recommendations(race_conditions: RaceConditions, 
                              race_analyzer: RaceAnalyzer,
                              granite_engine: GraniteEngine):
    """
    Render AI-powered strategy recommendations
    
    Args:
        race_conditions: Current race conditions
        race_analyzer: Race analyzer instance
        granite_engine: Granite AI engine instance
    """
    
    st.markdown("## 🤖 AI STRATEGY RECOMMENDATIONS")
    st.markdown("*Powered by IBM Granite*")
    st.markdown("---")
    
    # Get strategy recommendation
    try:
        recommendation = race_analyzer.analyze_strategy(race_conditions)
        
        # Get AI explanation
        explanation = granite_engine.explain_decision(
            recommendation.to_dict(),
            race_conditions.to_dict()
        )
        
        # Display primary recommendation
        action_emoji = {
            "pit_now": "🔴",
            "pit_next_lap": "🟡",
            "stay_out": "🟢",
            "push_hard": "⚡",
            "conserve_tires": "🛡️",
            "overtake_opportunity": "🎯"
        }
        
        action_color = {
            "pit_now": "#e63946",
            "pit_next_lap": "#ffd60a",
            "stay_out": "#06ffa5",
            "push_hard": "#f77f00",
            "conserve_tires": "#06ffa5",
            "overtake_opportunity": "#f77f00"
        }
        
        emoji = action_emoji.get(recommendation.action.value, "🏁")
        color = action_color.get(recommendation.action.value, "#06ffa5")
        
        st.markdown(f"""
        <div class="metric-card" style="border-color: {color}; background: linear-gradient(135deg, rgba(26, 26, 46, 0.9) 0%, rgba(26, 26, 46, 0.7) 100%);">
            <h2 style="color: {color}; margin: 0;">{emoji} {recommendation.action.value.replace('_', ' ').upper()}</h2>
            <p style="color: #888; margin: 5px 0;">Primary Recommendation</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Confidence and Risk
        col1, col2 = st.columns(2)
        
        with col1:
            confidence_pct = recommendation.confidence * 100
            confidence_color = "#06ffa5" if confidence_pct > 75 else "#ffd60a" if confidence_pct > 50 else "#e63946"
            
            st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <h3 style="color: {confidence_color}; margin: 0;">{confidence_pct:.0f}%</h3>
                <p style="margin: 5px 0 0 0; color: #888;">Confidence Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            risk_color = {
                "low": "#06ffa5",
                "medium": "#ffd60a",
                "high": "#e63946"
            }
            
            st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <h3 style="color: {risk_color.get(recommendation.risk_level, '#ffd60a')}; margin: 0;">{recommendation.risk_level.upper()}</h3>
                <p style="margin: 5px 0 0 0; color: #888;">Risk Level</p>
            </div>
            """, unsafe_allow_html=True)
        
        # AI Explanation
        st.markdown("### 💡 AI Reasoning")
        st.markdown(f"""
        <div class="metric-card">
            <p style="font-size: 14px; line-height: 1.6;">{explanation}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Expected Outcome
        st.markdown("### 🎯 Expected Outcome")
        st.markdown(f"""
        <div class="metric-card">
            <p style="font-size: 14px;">{recommendation.expected_outcome}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Timing Window (if applicable)
        if recommendation.timing_window:
            st.markdown("### ⏱️ Timing Window")
            st.markdown(f"""
            <div class="metric-card">
                <p style="font-size: 14px; color: #ffd60a;"><strong>{recommendation.timing_window}</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Tire Recommendation (if applicable)
        if recommendation.tire_recommendation:
            st.markdown("### 🛞 Recommended Tire")
            tire_colors = {
                "soft": "#e63946",
                "medium": "#ffd60a",
                "hard": "#f8f9fa",
                "intermediate": "#06ffa5",
                "wet": "#0077b6"
            }
            tire_color = tire_colors.get(recommendation.tire_recommendation.value, "#ffd60a")
            
            st.markdown(f"""
            <div class="metric-card" style="border-color: {tire_color};">
                <h3 style="color: {tire_color}; margin: 0;">{recommendation.tire_recommendation.value.upper()}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        # Alternative Actions
        if recommendation.alternative_actions:
            st.markdown("### 🔄 Alternative Strategies")
            for alt in recommendation.alternative_actions:
                risk_icon = "🔴" if alt.get('risk') == 'high' else "🟡" if alt.get('risk') == 'medium' else "🟢"
                st.markdown(f"""
                <div class="metric-card" style="background: rgba(26, 26, 46, 0.5);">
                    <p><strong>{risk_icon} {alt.get('action', '').replace('_', ' ').upper()}</strong></p>
                    <p style="font-size: 12px; color: #888;">{alt.get('reason', '')}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Additional AI Analysis
        with st.expander("📊 Detailed AI Analysis"):
            scenario_analysis = granite_engine.analyze_race_scenario(race_conditions.to_dict())
            st.markdown(scenario_analysis.get('analysis', 'Analysis not available'))
            st.caption(f"Source: {scenario_analysis.get('source', 'Unknown')}")
        
        # Pit Strategy Options
        with st.expander("🔧 Pit Strategy Options"):
            remaining_laps = race_conditions.total_laps - race_conditions.lap_number
            pit_strategies = granite_engine.generate_pit_strategy(
                race_conditions.to_dict(),
                remaining_laps
            )
            
            for strategy in pit_strategies:
                risk_color = {
                    "low": "#06ffa5",
                    "medium": "#ffd60a",
                    "high": "#e63946"
                }
                
                st.markdown(f"""
                <div class="metric-card" style="border-color: {risk_color.get(strategy.get('risk', 'medium'), '#ffd60a')};">
                    <h4 style="margin: 0;">{strategy.get('name', 'Strategy')}</h4>
                    <p style="font-size: 12px; color: #888;">{strategy.get('description', '')}</p>
                    <p style="font-size: 12px;"><strong>Stops:</strong> {strategy.get('stops', 0)}</p>
                    <p style="font-size: 12px;"><strong>Risk:</strong> <span style="color: {risk_color.get(strategy.get('risk', 'medium'), '#ffd60a')};">{strategy.get('risk', 'medium').upper()}</span></p>
                </div>
                """, unsafe_allow_html=True)
        
        # Overtaking Analysis (if gap is small)
        if race_conditions.gap_to_leader < 5.0:
            with st.expander("🎯 Overtaking Opportunity Analysis"):
                overtake_analysis = granite_engine.evaluate_overtaking_opportunity(
                    race_conditions.to_dict(),
                    race_conditions.gap_to_leader
                )
                
                probability = overtake_analysis.get('probability', 0) * 100
                prob_color = "#06ffa5" if probability > 60 else "#ffd60a" if probability > 40 else "#e63946"
                
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Overtaking Probability: <span style="color: {prob_color};">{probability:.0f}%</span></h4>
                    <p><strong>Recommendation:</strong> {overtake_analysis.get('recommendation', '')}</p>
                    <p><strong>Suggested Action:</strong> {overtake_analysis.get('suggested_action', '')}</p>
                </div>
                """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        st.info("Please check your IBM Granite configuration and try again.")

# Made with Bob
