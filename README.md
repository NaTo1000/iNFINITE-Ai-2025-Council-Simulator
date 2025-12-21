# iNFINITE AI 2025 Council Simulator

**Highly Complex & Technically Accurate Decision Engine**

Offline simulation engine that:
- ✅ Replays historical events
- ✅ Stress-tests decision rules  
- ✅ Proves the council won't nuke prod at 3am

## 🚀 Quick Start

```bash
# Run the simulation
python simulator.py

# Run comprehensive tests
python test_simulator.py
```

## 🎯 Features

- **Advanced Safety Guards**: Prevents night/weekend deployments
- **Multi-Member Council**: 5 diverse decision-makers with weighted voting
- **Risk Assessment**: Multi-dimensional evaluation (Critical → Negligible)
- **Circuit Breaker**: Prevents cascading failures
- **Historical Replay**: Learn from past incidents
- **Stress Testing**: Validates rules against 100+ scenarios
- **Comprehensive Reports**: JSON output with full audit trail

## 📋 Components

- `simulator.py` - Core simulation engine (600+ lines)
- `test_simulator.py` - Comprehensive test suite (400+ lines)
- `config.json` - Configuration for safety rules
- `DOCUMENTATION.md` - Full technical documentation

## 🛡️ Safety Mechanisms

| Time | Status | Risk |
|------|--------|------|
| 9am-5pm | ✅ SAFE | Business hours |
| 9pm-6am | 🚫 BLOCKED | Night operations prohibited |
| Weekend | 🚫 BLOCKED | No deployments |

**The simulator mathematically proves it won't approve dangerous 3am deployments.**

## 📖 Documentation

See [DOCUMENTATION.md](DOCUMENTATION.md) for complete technical details, examples, and API reference.

---

*Can't take your eyes off it* - Every decision is logged, evaluated, and protected by multiple safety layers.
