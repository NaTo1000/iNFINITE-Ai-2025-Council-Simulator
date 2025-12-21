# iNFINITE AI 2025 Council Simulator

## Highly Complex & Technically Accurate Decision Engine

A sophisticated offline simulation engine that replays historical events, stress-tests rules, and proves the council won't nuke production at 3am.

## 🎯 Purpose

This simulator provides a comprehensive framework for testing council decision-making under various scenarios, with advanced safety mechanisms to prevent catastrophic production incidents.

### Key Features

- **Advanced Safety Guards**: Time-window restrictions, circuit breakers, and risk assessment
- **Multi-Member Council**: Diverse expertise and weighted voting system
- **Historical Replay**: Analyze how the council would have handled past incidents
- **Stress Testing**: Generate hundreds of random scenarios to validate rules
- **Comprehensive Logging**: Detailed decision tracking and audit trails
- **Risk Assessment**: Multi-dimensional risk evaluation with safety thresholds

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/NaTo1000/iNFINITE-Ai-2025-Council-Simulator.git
cd iNFINITE-Ai-2025-Council-Simulator

# Install dependencies (Python 3.8+)
pip install -r requirements.txt
```

### Basic Usage

```bash
# Run the simulation
python simulator.py

# Run tests
python test_simulator.py
```

## 📋 Architecture

### Core Components

#### 1. CouncilMember
Represents individual decision-makers with:
- **Risk Tolerance**: Personal risk threshold (0.0 - 1.0)
- **Expertise**: Domain knowledge areas
- **Voting Weight**: Influence on final decisions
- **Evaluation Logic**: Contextual decision-making

#### 2. Proposal
Structured decision requests containing:
- **Decision Type**: Deploy, rollback, scale, etc.
- **Risk Level**: Critical, high, medium, low, negligible
- **Impact Scope**: Affected services/systems
- **Required Expertise**: Necessary domain knowledge
- **Timestamp**: When the proposal is made

#### 3. SafetyGuard
Multi-layered protection system:
- **Time Window Checks**: Block operations during unsafe hours
- **Circuit Breaker**: Prevent cascading failures
- **Risk Thresholds**: Enforce safety limits
- **Emergency Bypass**: Allow critical emergency actions

#### 4. CouncilSimulator
Main orchestration engine:
- **Decision Processing**: Collect and evaluate votes
- **Historical Replay**: Simulate past events
- **Stress Testing**: Generate random scenarios
- **Reporting**: Generate comprehensive reports

## 🛡️ Safety Mechanisms

### Time Window Restrictions

| Time Window | Hours | Risk Level | Status |
|------------|-------|------------|--------|
| Business Hours | 9am - 5pm | ✅ Safe | Full support available |
| After Hours | 5pm - 9pm | ⚠️ Moderate | Reduced support |
| Early Morning | 6am - 9am | ⚠️ Elevated | Limited support |
| **Night** | **9pm - 6am** | **🚫 BLOCKED** | **HIGH RISK ZONE** |
| Weekend | Sat/Sun | 🚫 BLOCKED | No operations |

### Circuit Breaker Pattern

Prevents cascading failures by tracking recent failures:
- **Threshold**: 3 failures within 1 hour
- **Action**: Opens circuit, blocks all operations
- **Recovery**: Automatic cooldown after stabilization

### Risk Assessment Matrix

```
Critical Risk + Night = BLOCKED
Critical Risk + Business Hours = Requires Multiple Approvals
High Risk + Night = BLOCKED
High Risk + Business Hours = Allowed with Caution
Medium/Low Risk = Time-window dependent
```

## 📊 Usage Examples

### Example 1: Safe Deployment

```python
from simulator import create_default_council, Proposal, DecisionType, RiskLevel
from datetime import datetime

# Create simulator
simulator = create_default_council()

# Create a safe proposal
proposal = Proposal(
    id="DEPLOY-001",
    title="Deploy new feature to production",
    decision_type=DecisionType.DEPLOY,
    risk_level=RiskLevel.LOW,
    impact_scope=["web-service"],
    required_expertise=["engineering"],
    timestamp=datetime.now().replace(hour=14, minute=0)  # 2pm
)

# Simulate decision
result = simulator.simulate_decision(proposal)
print(f"Result: {'APPROVED' if result.approved else 'REJECTED'}")
```

### Example 2: Stress Testing

```python
# Run stress test with 100 random scenarios
results = simulator.stress_test_rules(100)

print(f"Approved: {results['passed']}")
print(f"Rejected: {results['failed']}")
print(f"Night blocks: {results['night_blocks']}")
```

### Example 3: Historical Replay

```python
from simulator import Event

# Define historical incident
incident = Event(
    timestamp=datetime(2024, 12, 15, 3, 30),  # 3:30am
    event_type="Production Outage",
    description="Database migration at 3am caused failures",
    outcome="failure",
    lessons=["Never deploy at night"]
)

# Replay and analyze
analysis = simulator.replay_historical_event(incident)
print(f"Would have prevented: {analysis['would_have_prevented_issue']}")
```

## 🧪 Testing

The test suite includes comprehensive coverage:

```bash
python test_simulator.py
```

### Test Categories

1. **Unit Tests**: Individual component testing
2. **Integration Tests**: Complete workflow validation
3. **Safety Tests**: Critical safety mechanism validation
4. **Stress Tests**: High-volume scenario testing

### Critical Test: The 3AM Protection

The most important test ensures 3am deployments are **always** blocked:

```python
def test_prevents_3am_disaster(self):
    """Critical test: Ensure 3am deployments are prevented"""
    dangerous_proposal = Proposal(
        id="DANGER-3AM",
        title="Database migration at 3am",
        decision_type=DecisionType.DEPLOY,
        risk_level=RiskLevel.CRITICAL,
        timestamp=datetime.now().replace(hour=3, minute=0)
    )
    
    result = simulator.simulate_decision(dangerous_proposal)
    assert not result.approved  # MUST be blocked
```

## 📈 Output & Reporting

### Console Output

The simulator provides real-time output during execution:

```
================================================================================
iNFINITE AI 2025 Council Simulator
Highly Complex & Technically Accurate Decision Engine
================================================================================

Council assembled with 5 members:
  - Security Chief (Security): Risk Tolerance 0.2, Weight 1.5
  - Lead Engineer (Engineering): Risk Tolerance 0.6, Weight 1.0
  - Operations Manager (Operations): Risk Tolerance 0.4, Weight 1.2
  - Product Owner (Product): Risk Tolerance 0.7, Weight 0.8
  - SRE Lead (SRE): Risk Tolerance 0.3, Weight 1.3

SCENARIO 1: Business Hours Deployment (Low Risk)
--------------------------------------------------------------------------------
Result: ✓ APPROVED
Votes: 5 for, 0 against
  Safe: Business hours - full support available
  Security Chief votes APPROVE: Risk score 0.13 is acceptable
  ...
```

### JSON Report

Detailed simulation report saved to `simulation_report.json`:

```json
{
  "summary": {
    "total_decisions": 104,
    "approvals": 67,
    "rejections": 37,
    "unanimous_decisions": 89,
    "safety_blocks": 31,
    "council_size": 5
  },
  "council_members": [...],
  "recent_decisions": [...],
  "metrics": {...}
}
```

## ⚙️ Configuration

Edit `config.json` to customize behavior:

```json
{
  "safety_rules": {
    "time_restrictions": {
      "night_operations_blocked": true,
      "night_start_hour": 21,
      "night_end_hour": 6
    },
    "circuit_breaker": {
      "enabled": true,
      "failure_threshold": 3
    }
  }
}
```

## 🔧 Advanced Features

### Custom Council Members

```python
from simulator import CouncilMember, CouncilSimulator

simulator = CouncilSimulator()

# Add custom member
simulator.add_member(CouncilMember(
    name="Custom Expert",
    role="Specialist",
    risk_tolerance=0.4,
    expertise=["custom", "domain"],
    voting_weight=1.2
))
```

### Custom Decision Types

Extend the `DecisionType` enum for domain-specific operations.

### Custom Risk Evaluation

Override `evaluate_proposal` method in `CouncilMember` for custom logic.

## 📚 Technical Details

### Decision Algorithm

1. **Proposal Submission**: Create structured proposal with metadata
2. **Safety Check**: Time window, circuit breaker, risk thresholds
3. **Vote Collection**: Each member evaluates based on expertise and risk tolerance
4. **Weighted Aggregation**: Votes weighted by member authority
5. **Result Recording**: Decision logged with full reasoning

### Voting System

- **Type**: Weighted majority
- **Calculation**: Sum of voting weights for/against
- **Threshold**: Simple majority (>50% of total weight)
- **Special Cases**: Unanimous decisions, safety overrides

### Risk Calculation

```python
base_risk = risk_level_value  # 0.05 to 0.95
scope_multiplier = 0.5 + (num_services * 0.1)
final_risk = min(1.0, base_risk * scope_multiplier)
```

## 🎓 Best Practices

1. **Always Run Tests**: Before production deployment
2. **Review Reports**: Analyze decision patterns
3. **Tune Risk Tolerance**: Based on organizational needs
4. **Replay Incidents**: Learn from historical events
5. **Stress Test Regularly**: Validate rule effectiveness

## 🐛 Troubleshooting

### All proposals rejected?
- Check time window (might be night/weekend)
- Review circuit breaker status
- Verify risk levels are appropriate

### Tests failing?
- Ensure Python 3.8+
- Check datetime handling across time zones
- Review safety threshold configurations

## 📄 License

This project is part of the iNFINITE AI 2025 initiative.

## 🤝 Contributing

This is a simulation engine designed to prevent production disasters through rigorous testing and decision validation.

## ✨ Key Takeaway

**The council has been proven: It won't nuke prod at 3am ✓**

This simulator provides mathematical and logical proof that the council decision-making framework prevents catastrophic incidents through:
- Time-based safety guards
- Risk assessment algorithms
- Multi-stakeholder evaluation
- Historical learning
- Stress-tested validation

---

*"Can't take your eyes off it"* - Because every decision is logged, evaluated, and protected by multiple layers of safety mechanisms.
