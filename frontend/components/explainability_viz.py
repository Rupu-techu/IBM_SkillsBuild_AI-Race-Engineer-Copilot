"""
AI Explainability Visualizations
Advanced visual components for explaining AI decisions
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
import numpy as np


def render_confidence_gauge(confidence: float, title: str = "AI Confidence"):
    """
    Render a gauge chart for confidence visualization
    
    Args:
        confidence: Confidence score (0-1)
        title: Chart title
    """
    
    confidence_pct = confidence * 100
    
    # Determine color based on confidence
    if confidence_pct >= 80:
        color = "#06ffa5"
    elif confidence_pct >= 60:
        color = "#ffd60a"
    else:
        color = "#e63946"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = confidence_pct,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'color': 'white', 'size': 16}},
        number = {'suffix': "%", 'font': {'color': 'white', 'size': 32}},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "rgba(26, 26, 46, 0.8)",
            'borderwidth': 2,
            'bordercolor': color,
            'steps': [
                {'range': [0, 60], 'color': 'rgba(230, 57, 70, 0.3)'},
                {'range': [60, 80], 'color': 'rgba(255, 214, 10, 0.3)'},
                {'range': [80, 100], 'color': 'rgba(6, 255, 165, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': confidence_pct
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white"},
        height=250,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_decision_factors_chart(factors: Dict):
    """
    Render decision factors as a horizontal bar chart
    
    Args:
        factors: Dictionary of decision factors with weights
    """
    
    # Prepare data
    factor_names = []
    weights = []
    impacts = []
    colors = []
    
    for name, data in factors.items():
        factor_names.append(name.replace('_', ' ').title())
        weights.append(data['normalized_weight'] * 100)
        impacts.append(data['impact'])
        
        # Color based on impact
        if data['impact'] == 'critical':
            colors.append('#e63946')
        elif data['impact'] == 'high':
            colors.append('#f77f00')
        elif data['impact'] == 'medium':
            colors.append('#ffd60a')
        else:
            colors.append('#06ffa5')
    
    # Create figure
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=factor_names,
        x=weights,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='white', width=1)
        ),
        text=[f"{w:.1f}%" for w in weights],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Weight: %{x:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': "Decision Factor Weights",
            'font': {'color': 'white', 'size': 18}
        },
        xaxis_title="Influence on Decision (%)",
        yaxis_title="",
        paper_bgcolor='rgba(26, 26, 46, 0.8)',
        plot_bgcolor='rgba(26, 26, 46, 0.8)',
        font={'color': 'white'},
        height=300,
        margin=dict(l=150, r=20, t=50, b=50),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            range=[0, max(weights) * 1.1]
        ),
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_risk_reward_matrix(strategies: List[Dict]):
    """
    Render risk vs reward scatter plot for strategy comparison
    
    Args:
        strategies: List of strategy dictionaries with risk and reward
    """
    
    # Prepare data
    names = []
    risks = []
    rewards = []
    colors = []
    sizes = []
    
    for strategy in strategies:
        names.append(strategy.get('name', 'Unknown'))
        risks.append(strategy.get('risk', 0.5) * 100)
        rewards.append(strategy.get('reward', 0.5) * 100)
        
        # Color based on recommendation
        if strategy.get('recommended', False):
            colors.append('#06ffa5')
            sizes.append(20)
        else:
            colors.append('#ffd60a')
            sizes.append(15)
    
    # Create figure
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=risks,
        y=rewards,
        mode='markers+text',
        marker=dict(
            size=sizes,
            color=colors,
            line=dict(color='white', width=2)
        ),
        text=names,
        textposition="top center",
        textfont=dict(color='white', size=10),
        hovertemplate='<b>%{text}</b><br>Risk: %{x:.0f}%<br>Reward: %{y:.0f}%<extra></extra>'
    ))
    
    # Add quadrant lines
    fig.add_hline(y=50, line_dash="dash", line_color="rgba(255,255,255,0.3)")
    fig.add_vline(x=50, line_dash="dash", line_color="rgba(255,255,255,0.3)")
    
    # Add quadrant labels
    fig.add_annotation(x=25, y=75, text="Low Risk<br>High Reward", 
                      showarrow=False, font=dict(color='#06ffa5', size=10))
    fig.add_annotation(x=75, y=75, text="High Risk<br>High Reward",
                      showarrow=False, font=dict(color='#ffd60a', size=10))
    fig.add_annotation(x=25, y=25, text="Low Risk<br>Low Reward",
                      showarrow=False, font=dict(color='#888', size=10))
    fig.add_annotation(x=75, y=25, text="High Risk<br>Low Reward",
                      showarrow=False, font=dict(color='#e63946', size=10))
    
    fig.update_layout(
        title={
            'text': "Strategy Risk vs Reward Analysis",
            'font': {'color': 'white', 'size': 18}
        },
        xaxis_title="Risk Level (%)",
        yaxis_title="Expected Reward (%)",
        paper_bgcolor='rgba(26, 26, 46, 0.8)',
        plot_bgcolor='rgba(26, 26, 46, 0.8)',
        font={'color': 'white'},
        height=400,
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            range=[0, 100]
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            range=[0, 100]
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_strategy_comparison_radar(strategies: List[Dict]):
    """
    Render radar chart comparing multiple strategies
    
    Args:
        strategies: List of strategies with multiple metrics
    """
    
    categories = ['Speed', 'Tire Life', 'Fuel Efficiency', 'Risk', 'Confidence']
    
    fig = go.Figure()
    
    for strategy in strategies[:3]:  # Limit to 3 strategies for clarity
        values = [
            strategy.get('speed', 50),
            strategy.get('tire_life', 50),
            strategy.get('fuel_efficiency', 50),
            100 - strategy.get('risk', 50),  # Invert risk (lower is better)
            strategy.get('confidence', 50)
        ]
        
        # Close the radar chart
        values.append(values[0])
        categories_closed = categories + [categories[0]]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories_closed,
            fill='toself',
            name=strategy.get('name', 'Strategy'),
            line=dict(width=2)
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(255, 255, 255, 0.2)',
                tickfont=dict(color='white')
            ),
            angularaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.2)',
                tickfont=dict(color='white', size=12)
            ),
            bgcolor='rgba(26, 26, 46, 0.8)'
        ),
        showlegend=True,
        legend=dict(
            font=dict(color='white'),
            bgcolor='rgba(26, 26, 46, 0.8)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'},
        height=400,
        title={
            'text': "Multi-Dimensional Strategy Comparison",
            'font': {'color': 'white', 'size': 18}
        }
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_probability_distribution(outcomes: List[Dict]):
    """
    Render probability distribution of race outcomes
    
    Args:
        outcomes: List of possible outcomes with probabilities
    """
    
    positions = [o.get('position', 0) for o in outcomes]
    probabilities = [o.get('probability', 0) * 100 for o in outcomes]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=[f"P{p}" for p in positions],
        y=probabilities,
        marker=dict(
            color=probabilities,
            colorscale=[[0, '#e63946'], [0.5, '#ffd60a'], [1, '#06ffa5']],
            line=dict(color='white', width=1)
        ),
        text=[f"{p:.1f}%" for p in probabilities],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Probability: %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': "Race Outcome Probability Distribution",
            'font': {'color': 'white', 'size': 18}
        },
        xaxis_title="Final Position",
        yaxis_title="Probability (%)",
        paper_bgcolor='rgba(26, 26, 46, 0.8)',
        plot_bgcolor='rgba(26, 26, 46, 0.8)',
        font={'color': 'white'},
        height=300,
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            range=[0, 100]
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_decision_tree_flow(decision_path: List[Dict]):
    """
    Render decision tree showing AI reasoning flow
    
    Args:
        decision_path: List of decision nodes
    """
    
    st.markdown("### 🌳 AI Decision Flow")
    
    for idx, node in enumerate(decision_path):
        condition = node.get('condition', '')
        result = node.get('result', '')
        confidence = node.get('confidence', 0)
        
        # Determine color based on result
        if 'critical' in result.lower() or 'pit' in result.lower():
            color = "#e63946"
            icon = "🔴"
        elif 'warning' in result.lower() or 'monitor' in result.lower():
            color = "#ffd60a"
            icon = "🟡"
        else:
            color = "#06ffa5"
            icon = "🟢"
        
        # Render node
        st.markdown(f"""
        <div style="
            background: rgba(26, 26, 46, 0.8);
            border-left: 4px solid {color};
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 20px; margin-right: 10px;">{icon}</span>
                <span style="color: {color}; font-weight: bold;">Step {idx + 1}</span>
            </div>
            <div style="color: #ccc; font-size: 14px; margin-bottom: 5px;">
                <strong>Condition:</strong> {condition}
            </div>
            <div style="color: white; font-size: 14px; margin-bottom: 5px;">
                <strong>Result:</strong> {result}
            </div>
            <div style="color: #888; font-size: 12px;">
                Confidence: {confidence * 100:.0f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add arrow between nodes
        if idx < len(decision_path) - 1:
            st.markdown("""
            <div style="text-align: center; color: #888; font-size: 20px; margin: 5px 0;">
                ↓
            </div>
            """, unsafe_allow_html=True)


def render_explainability_dashboard(recommendation: Dict, race_conditions: Dict,
                                   advanced_analysis: Dict):
    """
    Render comprehensive explainability dashboard
    
    Args:
        recommendation: AI recommendation
        race_conditions: Current race conditions
        advanced_analysis: Advanced intelligence analysis
    """
    
    st.markdown("## 🔍 AI EXPLAINABILITY DASHBOARD")
    st.markdown("*Understanding the AI's decision-making process*")
    st.markdown("---")
    
    # Row 1: Confidence and Decision Factors
    col1, col2 = st.columns([1, 2])
    
    with col1:
        confidence = recommendation.get('confidence', 0.7)
        render_confidence_gauge(confidence, "Decision Confidence")
    
    with col2:
        if 'decision_factors' in advanced_analysis:
            render_decision_factors_chart(advanced_analysis['decision_factors'])
    
    st.markdown("---")
    
    # Row 2: Strategy Comparison
    if 'strategy_comparison' in advanced_analysis:
        render_risk_reward_matrix(advanced_analysis['strategy_comparison'])
    
    st.markdown("---")
    
    # Row 3: Decision Flow
    if 'decision_path' in advanced_analysis:
        render_decision_tree_flow(advanced_analysis['decision_path'])

# Made with Bob
