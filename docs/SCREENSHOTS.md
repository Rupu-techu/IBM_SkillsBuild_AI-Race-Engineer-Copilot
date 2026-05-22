# 📸 Screenshots & Visual Assets

This document provides guidance for creating and organizing screenshots for the AI Race Engineer Copilot project.

---

## 📁 Directory Structure

```
docs/
└── images/
    ├── dashboard-hero.png          # Main hero image for README
    ├── dashboard-main.png          # Full dashboard overview
    ├── ai-strategy.png             # AI strategy panel
    ├── telemetry-charts.png        # Analytics and charts
    ├── simulation.png              # Live simulation view
    ├── architecture-diagram.png    # System architecture
    ├── workflow-diagram.png        # Langflow workflow
    └── demo/
        ├── scenario-1.png          # Critical tire wear
        ├── scenario-2.png          # Fuel emergency
        ├── scenario-3.png          # Weather change
        ├── scenario-4.png          # Undercut opportunity
        └── scenario-5.png          # Optimal strategy
```

---

## 🎯 Required Screenshots

### 1. Hero Image (`dashboard-hero.png`)

**Purpose:** Main banner for README  
**Dimensions:** 1920x1080 (16:9)  
**Content:** Full dashboard view with active telemetry  
**Requirements:**
- Show complete UI with all panels visible
- Include live telemetry data
- Display AI recommendation panel
- Show charts and visualizations
- Capture during an interesting scenario

**Recommended Settings:**
- Lap: 28/50
- Position: P3
- Tire Wear: 78%
- Active AI recommendation visible

---

### 2. Dashboard Main (`dashboard-main.png`)

**Purpose:** Overview of main interface  
**Dimensions:** 1920x1080  
**Content:** Complete dashboard layout  
**Requirements:**
- All major components visible
- Sidebar with race conditions
- Main telemetry cards
- Strategy panel
- Charts section
- Clean, professional appearance

---

### 3. AI Strategy Panel (`ai-strategy.png`)

**Purpose:** Showcase AI recommendations  
**Dimensions:** 1200x800  
**Content:** Close-up of strategy recommendation  
**Requirements:**
- Clear action display (PIT NOW, STAY OUT, etc.)
- Confidence score visible
- Risk level indicator
- Full AI reasoning text
- Alternative strategies section
- Professional formatting

**Example Content:**
```
🎯 Recommendation: PIT NOW
📊 Confidence: 92%
⚠️ Risk: HIGH

💡 Reasoning:
Pit now because tire degradation is critical at 87.5%...

🔄 Alternatives:
• PIT NEXT LAP (78% confidence)
• STAY OUT (45% confidence)
```

---

### 4. Telemetry Charts (`telemetry-charts.png`)

**Purpose:** Showcase analytics capabilities  
**Dimensions:** 1600x900  
**Content:** Interactive charts and graphs  
**Requirements:**
- Tire wear chart with historical data
- Fuel consumption graph
- Lap performance trends
- Pit strategy timeline
- Clear labels and legends
- Professional color scheme

---

### 5. Live Simulation (`simulation.png`)

**Purpose:** Show dynamic race events  
**Dimensions:** 1920x1080  
**Content:** Simulation in progress  
**Requirements:**
- Active race event visible
- Commentary panel showing
- Telemetry updating
- Event notification
- Animated elements captured

---

### 6. Architecture Diagram (`architecture-diagram.png`)

**Purpose:** System architecture visualization  
**Dimensions:** 1600x1200  
**Content:** Technical architecture  
**Requirements:**
- Clear layer separation
- Component relationships
- IBM technology callouts
- Data flow arrows
- Professional diagram style

**Suggested Tool:** draw.io, Lucidchart, or Figma

---

### 7. Workflow Diagram (`workflow-diagram.png`)

**Purpose:** Langflow workflow visualization  
**Dimensions:** 1400x1000  
**Content:** AI workflow pipeline  
**Requirements:**
- Langflow interface screenshot
- Complete workflow visible
- Component connections clear
- IBM Granite node highlighted
- Professional appearance

---

## 🎬 Demo Scenario Screenshots

### Scenario 1: Critical Tire Wear (`demo/scenario-1.png`)

**Setup:**
- Lap: 30/50
- Tire Wear: 88%
- Tire Age: 20 laps
- Compound: Soft

**Expected:** PIT NOW recommendation with HIGH risk

---

### Scenario 2: Fuel Emergency (`demo/scenario-2.png`)

**Setup:**
- Lap: 42/50
- Fuel Level: 12%
- Tire Wear: 65%

**Expected:** PIT NOW for fuel with CRITICAL risk

---

### Scenario 3: Weather Change (`demo/scenario-3.png`)

**Setup:**
- Lap: 25/50
- Weather: Light Rain
- Current Tires: Slicks
- Track Temp: Dropping

**Expected:** PIT NOW for intermediate tires

---

### Scenario 4: Undercut Opportunity (`demo/scenario-4.png`)

**Setup:**
- Lap: 22/50
- Position: P3
- Gap to P2: 2.8s
- Tire Wear: 72%

**Expected:** PIT NEXT LAP for undercut

---

### Scenario 5: Optimal Strategy (`demo/scenario-5.png`)

**Setup:**
- Lap: 25/50
- Tire Wear: 58%
- Fuel: 70%
- Position: P2

**Expected:** STAY OUT with medium confidence

---

## 🎨 Screenshot Guidelines

### Quality Standards

- **Resolution:** Minimum 1920x1080 for main screenshots
- **Format:** PNG for UI screenshots, SVG for diagrams
- **File Size:** Optimize to <500KB per image
- **Clarity:** Ensure text is readable at 100% zoom
- **Consistency:** Use same UI state/theme across screenshots

### Capture Settings

**Browser:**
- Use Chrome or Firefox
- Full screen mode (F11)
- Zoom: 100%
- DevTools closed

**Display:**
- 1920x1080 or higher resolution
- Dark mode enabled
- No browser UI visible
- Clean desktop background

### Editing

**Tools:**
- Screenshot: Windows Snipping Tool, macOS Screenshot, or Flameshot
- Editing: GIMP, Photoshop, or Figma
- Optimization: TinyPNG, ImageOptim

**Edits:**
- Crop to relevant content
- Add subtle drop shadows if needed
- Highlight important elements with arrows/boxes
- Blur sensitive information (API keys, etc.)
- Optimize file size

---

## 📐 Diagram Creation

### Architecture Diagram

**Tool:** draw.io (diagrams.net)

**Style:**
- Dark background (#0a0a0a)
- White text (#ffffff)
- Accent colors: Red (#e63946), Green (#06ffa5), Blue (#0096ff)
- Rounded rectangles for components
- Arrows for data flow
- Clear labels

**Layers:**
1. Frontend Layer (React)
2. AI Orchestration (Langflow)
3. Core Analysis (Python)
4. IBM AI Layer (Granite + watsonx.ai)
5. Data Layer

---

### Workflow Diagram

**Source:** Langflow interface screenshot

**Requirements:**
- Export from Langflow at high resolution
- Ensure all nodes are visible
- Show connections clearly
- Highlight IBM Granite components
- Add annotations if needed

---

## 🖼️ Image Placeholders

Until actual screenshots are captured, use these placeholders:

```markdown
![Dashboard Overview](docs/images/dashboard-main.png)
*Real-time telemetry monitoring with AI-powered insights*
```

**Placeholder Services:**
- [Placeholder.com](https://placeholder.com)
- [Lorem Picsum](https://picsum.photos)
- Create simple mockups in Figma

---

## ✅ Screenshot Checklist

Before publishing screenshots:

- [ ] All required screenshots captured
- [ ] Images optimized for web (<500KB each)
- [ ] Consistent UI theme across all images
- [ ] No sensitive information visible
- [ ] Text is readable at 100% zoom
- [ ] Professional appearance
- [ ] Proper file naming convention
- [ ] Organized in correct directories
- [ ] Referenced in documentation
- [ ] Alt text added for accessibility

---

## 📝 Image Attribution

All screenshots should include:

```markdown
![Description](path/to/image.png)
*Caption describing the image*
```

**Example:**
```markdown
![AI Strategy Panel](docs/images/ai-strategy.png)
*Explainable AI recommendations with confidence scoring and risk assessment*
```

---

## 🎥 Video Demo

### Recording Settings

**Tool:** OBS Studio, Loom, or Screen Studio

**Settings:**
- Resolution: 1920x1080
- Frame Rate: 30 FPS
- Format: MP4 (H.264)
- Audio: Clear narration
- Length: 3-5 minutes

**Content:**
1. Introduction (15s)
2. Dashboard overview (30s)
3. Scenario 1 demo (45s)
4. Scenario 2 demo (45s)
5. Technology highlight (45s)
6. Conclusion (30s)

---

## 🔗 Asset Links

Once created, update these links in documentation:

- **README.md** — Hero image, main screenshots
- **PROJECT_HIGHLIGHTS.md** — Feature screenshots
- **QUICKSTART.md** — Setup screenshots
- **docs/architecture.md** — Architecture diagram
- **workflows/langflow_setup.md** — Workflow diagram

---

## 📧 Questions?

For questions about screenshots or visual assets:
- Open an issue on GitHub
- Check existing documentation
- Review similar projects for inspiration

---

<div align="center">

**AI Race Engineer Copilot** — *Professional Documentation*

**[📖 Back to Docs](../README.md)** • **[🎯 Quick Start](../QUICKSTART.md)** • **[🏆 Highlights](PROJECT_HIGHLIGHTS.md)**

</div>