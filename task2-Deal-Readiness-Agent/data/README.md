# 📊 Internal Data for Deal Readiness Agent

This folder contains the internal/proprietary data used by the **Internal Intelligence Agent**.

## Data Files

| File | Description | Records |
|------|-------------|---------|
| [win_loss_records.json](win_loss_records.json) | Historical competitive deal outcomes | 15 deals |
| [product_strengths.json](product_strengths.json) | Product capabilities and weaknesses | 8 strengths, 5 weaknesses |
| [competitor_battlecards.json](competitor_battlecards.json) | Detailed competitor analysis | 5 competitors |
| [industry_insights.json](industry_insights.json) | Industry-specific win patterns | 6 industries |

## Data Schema

### Win/Loss Records
```json
{
  "deal_id": "DEAL-2025-001",
  "customer": "Company Name",
  "industry": "Healthcare",
  "deal_size": 2400000,
  "competitor": "Verizon Business",
  "outcome": "WIN|LOSS",
  "decision_factors": ["factor1", "factor2"],
  "winning_themes": ["theme1", "theme2"],  // if WIN
  "loss_reasons": ["reason1", "reason2"],   // if LOSS
  "notes": "Additional context"
}
```

### Product Strengths/Weaknesses
```json
{
  "category": "Network Coverage",
  "strength": "Rural and Highway Coverage",
  "description": "...",
  "evidence": ["data point 1", "data point 2"],
  "best_for_industries": ["Healthcare", "Government"],
  "talking_points": ["point 1", "point 2"]
}
```

### Competitor Battlecards
```json
{
  "name": "Verizon Business",
  "key_strengths": ["..."],
  "key_weaknesses": ["..."],
  "recent_vulnerabilities": ["..."],
  "how_we_win": ["..."],
  "how_we_lose": ["..."],
  "ideal_opportunities": ["..."],
  "avoid_opportunities": ["..."]
}
```

### Industry Insights
```json
{
  "name": "Healthcare",
  "our_win_rate": "72%",
  "buying_triggers": ["..."],
  "critical_requirements": ["..."],
  "our_advantages": ["..."],
  "winning_strategies": ["..."],
  "common_objections": [
    {"objection": "...", "response": "..."}
  ]
}
```

## Usage in Agent

The Internal Intelligence Agent should query this data to answer:

1. **Historical Performance**: "How have we done against [Competitor] in [Industry]?"
2. **Win Patterns**: "What helped us win similar deals?"
3. **Loss Patterns**: "Where do we typically lose and why?"
4. **Talking Points**: "What are our strengths against [Competitor]?"
5. **Objection Handling**: "How do we respond to [common objection]?"

## Example Queries

```python
# Find deals against Verizon in Healthcare
deals = [d for d in records if d["competitor"] == "Verizon Business" 
         and d["industry"] == "Healthcare"]

# Get our win rate in Financial Services
industry = next(i for i in industries if i["name"] == "Financial Services")
print(f"Win rate: {industry['our_win_rate']}")

# Get battlecard for T-Mobile
battlecard = next(c for c in competitors if c["name"] == "T-Mobile Business")
print(f"How we win: {battlecard['how_we_win']}")
```

## Data Freshness

- **Win/Loss Records**: Updated weekly by Sales Ops
- **Product Strengths**: Updated quarterly by Product Marketing
- **Battlecards**: Updated monthly by Competitive Intelligence
- **Industry Insights**: Updated quarterly by Industry Marketing

---

> ⚠️ **Note**: This is simulated data for the lab exercise. In a real implementation, this would connect to your CRM, competitive intelligence platform, and internal knowledge bases.
