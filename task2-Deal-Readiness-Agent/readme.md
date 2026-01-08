# 🎯 Competitive Deal Readiness

> **Agentic AI Lab** — Build a multi-agent system that helps sales teams win competitive deals

---

## 📋 Task Summary

In this task, you will build a **multi-agent AI solution** that helps a sales team prepare for a competitive deal by combining:

- 🌐 **External, real-time intelligence** from the web
- 🔒 **Internal, proprietary company knowledge**

The system will use two specialized agents and a simple orchestration step to assess deal risk and recommend sales positioning.

> 💡 This task demonstrates how agentic AI systems reason, coordinate, and act—going beyond simple chatbots to deliver real business value.

---

## 🏢 Business Context

Sales teams often rely on:

| Current State | Problem |
|---------------|---------|
| Static competitive battlecards | Quickly become outdated |
| Out-of-date market intelligence | Misses recent competitor moves |
| Tribal knowledge | Locked in documents or people's heads |

This task simulates a realistic scenario where an AI system assists sales engineers by answering:

> **"How ready are we to win this deal against [Competitor X]?"**

---

## 🎓 Learning Goals

By completing this task, you will learn how to:

### 1. Build Specialized AI Agents
- Create one agent focused on **external intelligence**
- Create another agent focused on **internal company data**
- Understand why splitting responsibilities improves clarity and reliability

### 2. Use Web Search as an Agent Tool
- Perform targeted, real-time searches for competitor signals
- Extract relevant information from search results
- Understand why live data improves trust and accuracy

### 3. Leverage Internal (Private) Data
- Query a provided internal dataset (e.g., win/loss data, product strengths)
- Apply internal context that cannot be found via public sources
- See how proprietary data becomes a competitive advantage

### 4. Orchestrate Agent Outputs
- Combine insights from multiple agents
- Resolve conflicting signals
- Make a clear, goal-driven decision

### 5. Produce Sales-Ready Outputs
- Generate a concise deal readiness summary
- Recommend competitive talking points
- Identify when escalation or caution is required

---

## 🏗️ What You Will Build

At the end of this task, you will have a working AI system that:

```
┌─────────────────────────────────────────────────────────────┐
│                     DEAL READINESS SYSTEM                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────────┐       ┌─────────────────┐            │
│   │    External     │       │    Internal     │            │
│   │  Intelligence   │       │  Intelligence   │            │
│   │     Agent       │       │     Agent       │            │
│   │                 │       │                 │            │
│   │  🌐 Web Search  │       │  📊 Win/Loss    │            │
│   │  📰 News        │       │  💪 Strengths   │            │
│   │  ⚠️  Incidents   │       │  📈 History     │            │
│   └────────┬────────┘       └────────┬────────┘            │
│            │                         │                      │
│            └───────────┬─────────────┘                      │
│                        ▼                                    │
│              ┌─────────────────┐                            │
│              │   Orchestrator  │                            │
│              │                 │                            │
│              │  🔄 Combine     │                            │
│              │  ⚖️  Resolve     │                            │
│              │  📝 Recommend   │                            │
│              └────────┬────────┘                            │
│                       ▼                                     │
│         ┌─────────────────────────┐                         │
│         │   Deal Readiness Report │                         │
│         └─────────────────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🤖 Agent Responsibilities

### External Intelligence Agent

| Attribute | Description |
|-----------|-------------|
| **Purpose** | Gather real-time competitor insights from public sources |
| **Data Sources** | Web search, news articles, press releases |

**Key Questions It Answers:**
- Has the competitor had recent outages, incidents, or news?
- Are there signals that increase deal risk or opportunity?

---

### Internal Intelligence Agent

| Attribute | Description |
|-----------|-------------|
| **Purpose** | Apply your organization's internal knowledge to the deal |
| **Data Sources** | Win/loss database, product comparisons, battlecards |

**Key Questions It Answers:**
- How have similar deals gone in the past?
- What are known strengths or weaknesses in this industry?
- Where do we typically win or lose?

---

## 📁 Internal Data (Provided)

The `data/` folder contains the proprietary datasets for the **Internal Intelligence Agent**:

| File | Description | Use For |
|------|-------------|---------|
| [`win_loss_records.json`](data/win_loss_records.json) | 15 historical competitive deals with outcomes | "How did similar deals go?" |
| [`product_strengths.json`](data/product_strengths.json) | Our capabilities, weaknesses, and talking points | "What are our advantages?" |
| [`competitor_battlecards.json`](data/competitor_battlecards.json) | Detailed analysis of 5 major competitors | "How do we beat [Competitor]?" |
| [`industry_insights.json`](data/industry_insights.json) | Win rates and strategies by industry | "What works in [Industry]?" |

### Example Queries the Agent Should Answer

```
"What's our win rate against Verizon in Healthcare?"
→ Query win_loss_records.json + industry_insights.json

"What are T-Mobile's weaknesses we can exploit?"
→ Query competitor_battlecards.json

"How should we position against AT&T's IoT platform?"
→ Query product_strengths.json + competitor_battlecards.json

"What objections should we expect in Financial Services?"
→ Query industry_insights.json
```

> 📖 See [`data/README.md`](data/README.md) for detailed schema documentation.

---

## ✅ Success Criteria

You have successfully completed this task when:

- [ ] Both agents perform their assigned roles
- [ ] Web Search is used intentionally (not generically)
- [ ] Internal data influences the final recommendation
- [ ] The system produces a clear deal readiness assessment
- [ ] The output is understandable and useful to a sales team

---

## 🤔 Reflection Questions

After completing the task, consider:

1. What happens when external and internal signals **conflict**?
2. Where would a **human review or approval** be required?
3. How could this task **scale** with more data sources or agents?
4. Why did you choose the approach you took?
5. What are the **tradeoffs** to your approach?

> 📸 **Include a screenshot of your working app in your submission.**
