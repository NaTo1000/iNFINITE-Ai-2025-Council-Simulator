# Examples Guide

This file provides quick examples of how to use the council simulator for various scenarios.

## Running the Examples

```bash
# Run all examples
python examples.py

# Run specific simulation
python simulator.py

# Run tests
python test_simulator.py
```

## Quick Examples

### 1. Safe Business Hours Deployment

```python
from simulator import create_default_council, Proposal, DecisionType, RiskLevel
from datetime import datetime

simulator = create_default_council()

proposal = Proposal(
    id="DEPLOY-001",
    title="Deploy UI update",
    decision_type=DecisionType.DEPLOY,
    risk_level=RiskLevel.LOW,
    impact_scope=["web-service"],
    required_expertise=["engineering"],
    timestamp=datetime.now().replace(hour=14)  # 2pm
)

result = simulator.simulate_decision(proposal)
print(f"Approved: {result.approved}")
```

### 2. Preventing 3AM Disasters

```python
# This will be automatically rejected
dangerous_proposal = Proposal(
    id="DANGER-001",
    title="Critical database migration",
    decision_type=DecisionType.DEPLOY,
    risk_level=RiskLevel.CRITICAL,
    timestamp=datetime.now().replace(hour=3)  # 3am
)

result = simulator.simulate_decision(dangerous_proposal)
# result.approved will be False - blocked by safety guard!
```

### 3. Custom Council Members

```python
from simulator import CouncilSimulator, CouncilMember

simulator = CouncilSimulator()

simulator.add_member(CouncilMember(
    name="Security Expert",
    role="Security",
    risk_tolerance=0.2,  # Conservative
    expertise=["security", "compliance"],
    voting_weight=1.5
))
```

### 4. Historical Event Replay

```python
from simulator import Event

incident = Event(
    timestamp=datetime(2024, 12, 15, 3, 30),
    event_type="Production Outage",
    description="3am deployment caused outage",
    outcome="failure",
    lessons=["Never deploy at night"]
)

analysis = simulator.replay_historical_event(incident)
print(f"Would have prevented: {analysis['would_have_prevented_issue']}")
```

### 5. Stress Testing

```python
# Test with 100 random scenarios
results = simulator.stress_test_rules(100)

print(f"Passed: {results['passed']}")
print(f"Failed: {results['failed']}")
print(f"Night blocks: {results['night_blocks']}")
```

## Safety Mechanisms

The simulator has multiple safety layers:

1. **Time Restrictions**: Blocks night (9pm-6am) and weekend operations
2. **Circuit Breaker**: Prevents cascading failures
3. **Risk Assessment**: Multi-dimensional evaluation
4. **Weighted Voting**: Expert opinions carry more weight

## Understanding Results

When you run a simulation, you get:

```python
DecisionResult(
    proposal_id="...",
    approved=True/False,
    votes_for=X,
    votes_against=Y,
    total_weight=Z,
    unanimous=True/False,
    confidence_score=0.0-1.0,
    reasoning=[...list of reasons...]
)
```

## Common Patterns

### Check if safe to deploy

```python
# The simulator will automatically check time windows
result = simulator.simulate_decision(proposal)
if not result.approved:
    print("Deployment blocked:")
    for reason in result.reasoning:
        print(f"  - {reason}")
```

### Generate reports

```python
# After running simulations
report = simulator.generate_report()
simulator.save_report("my_report.json")
```

### Test multiple scenarios

```python
scenarios = [
    ("Low risk", RiskLevel.LOW),
    ("Medium risk", RiskLevel.MEDIUM),
    ("High risk", RiskLevel.HIGH),
]

for name, risk in scenarios:
    proposal = Proposal(
        id=f"TEST-{name}",
        title=name,
        decision_type=DecisionType.DEPLOY,
        risk_level=risk,
        timestamp=datetime.now().replace(hour=14)
    )
    result = simulator.simulate_decision(proposal)
    print(f"{name}: {'✓' if result.approved else '✗'}")
```

## See Also

- `DOCUMENTATION.md` - Complete technical documentation
- `simulator.py` - Source code with inline comments
- `test_simulator.py` - Test examples
- `config.json` - Configuration options
