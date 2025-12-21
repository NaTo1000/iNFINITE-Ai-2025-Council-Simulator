#!/usr/bin/env python3
"""
Example usage demonstrations for the iNFINITE AI 2025 Council Simulator
Shows various scenarios and how the council evaluates them
"""

from datetime import datetime, timedelta
from simulator import (
    create_default_council, 
    CouncilMember, 
    Proposal, 
    DecisionType, 
    RiskLevel, 
    Event
)


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_result(result, show_reasoning=True):
    """Print decision result in a formatted way"""
    status = "✓ APPROVED" if result.approved else "✗ REJECTED"
    print(f"\n{status}")
    print(f"  Votes: {result.votes_for} for, {result.votes_against} against")
    print(f"  Unanimous: {result.unanimous}")
    print(f"  Confidence: {result.confidence_score:.2f}")
    
    if show_reasoning:
        print("\n  Decision Reasoning:")
        for reason in result.reasoning:
            print(f"    • {reason}")


def example_1_safe_deployment():
    """Example 1: Safe deployment during business hours"""
    print_section("Example 1: Safe Low-Risk Deployment")
    
    simulator = create_default_council()
    
    # Create a Monday at 2pm
    monday = datetime.now()
    days_to_monday = (7 - monday.weekday()) % 7
    if days_to_monday != 0 or monday.weekday() != 0:
        monday = monday + timedelta(days=days_to_monday if days_to_monday != 0 else 7)
    monday = monday.replace(hour=14, minute=0)
    
    proposal = Proposal(
        id="SAFE-001",
        title="Deploy minor UI update to production",
        decision_type=DecisionType.DEPLOY,
        risk_level=RiskLevel.LOW,
        impact_scope=["web-frontend"],
        required_expertise=["engineering"],
        timestamp=monday,
        metadata={
            "change_type": "UI update",
            "rollback_plan": "Automatic via CDN",
            "testing": "Passed QA and staging"
        }
    )
    
    print(f"\nProposal: {proposal.title}")
    print(f"Time: {proposal.timestamp.strftime('%A, %I:%M %p')}")
    print(f"Risk Level: {proposal.risk_level.value}")
    print(f"Impact: {', '.join(proposal.impact_scope)}")
    
    result = simulator.simulate_decision(proposal)
    print_result(result)


def example_2_dangerous_night():
    """Example 2: Dangerous 3am deployment (should be blocked)"""
    print_section("Example 2: The Infamous 3AM Deployment")
    
    simulator = create_default_council()
    
    # Create a Monday at 3am
    monday = datetime.now()
    days_to_monday = (7 - monday.weekday()) % 7
    if days_to_monday != 0 or monday.weekday() != 0:
        monday = monday + timedelta(days=days_to_monday if days_to_monday != 0 else 7)
    monday = monday.replace(hour=3, minute=0)
    
    proposal = Proposal(
        id="DANGER-001",
        title="Critical database schema migration",
        decision_type=DecisionType.DEPLOY,
        risk_level=RiskLevel.CRITICAL,
        impact_scope=["database", "all-services"],
        required_expertise=["engineering", "operations", "security"],
        timestamp=monday,
        metadata={
            "change_type": "Database schema change",
            "downtime": "Expected 15 minutes",
            "testing": "Tested in staging"
        }
    )
    
    print(f"\nProposal: {proposal.title}")
    print(f"Time: {proposal.timestamp.strftime('%A, %I:%M %p')} ⚠️ NIGHT TIME")
    print(f"Risk Level: {proposal.risk_level.value}")
    print(f"Impact: {', '.join(proposal.impact_scope)}")
    
    result = simulator.simulate_decision(proposal)
    print_result(result)
    
    print("\n🛡️  SAFETY MECHANISM WORKED!")
    print("   The council prevented a potential 3am disaster.")


def example_3_custom_council():
    """Example 3: Custom council with specialized members"""
    print_section("Example 3: Custom Council Configuration")
    
    from simulator import CouncilSimulator
    
    simulator = CouncilSimulator()
    
    # Add custom members
    simulator.add_member(CouncilMember(
        name="Security Analyst",
        role="Security",
        risk_tolerance=0.1,  # Very conservative
        expertise=["security", "compliance"],
        voting_weight=2.0  # Double weight for security
    ))
    
    simulator.add_member(CouncilMember(
        name="DevOps Lead",
        role="DevOps",
        risk_tolerance=0.5,
        expertise=["operations", "automation"],
        voting_weight=1.5
    ))
    
    simulator.add_member(CouncilMember(
        name="Product Manager",
        role="Product",
        risk_tolerance=0.8,  # More aggressive
        expertise=["product", "business"],
        voting_weight=0.5  # Lower weight
    ))
    
    print("\nCustom Council Members:")
    for member in simulator.members:
        print(f"  • {member.name} ({member.role})")
        print(f"    Risk Tolerance: {member.risk_tolerance:.1f}, Weight: {member.voting_weight}")
    
    # Test with medium risk proposal
    monday = datetime.now()
    days_to_monday = (7 - monday.weekday()) % 7
    if days_to_monday != 0 or monday.weekday() != 0:
        monday = monday + timedelta(days=days_to_monday if days_to_monday != 0 else 7)
    monday = monday.replace(hour=15, minute=0)
    
    proposal = Proposal(
        id="CUSTOM-001",
        title="Deploy new API endpoint",
        decision_type=DecisionType.DEPLOY,
        risk_level=RiskLevel.MEDIUM,
        impact_scope=["api-service"],
        required_expertise=["engineering"],
        timestamp=monday
    )
    
    print(f"\nProposal: {proposal.title}")
    print(f"Risk Level: {proposal.risk_level.value}")
    
    result = simulator.simulate_decision(proposal)
    print_result(result, show_reasoning=False)


def example_4_historical_replay():
    """Example 4: Replay historical incident"""
    print_section("Example 4: Historical Event Replay")
    
    simulator = create_default_council()
    
    # Define a historical incident
    incident = Event(
        timestamp=datetime(2024, 12, 15, 3, 30),
        event_type="Production Outage",
        description="Database migration executed at 3:30am caused 2-hour outage",
        outcome="failure",
        lessons=[
            "Never deploy database changes at night",
            "Require multiple approvals for critical changes",
            "Maintain on-call support for all deployments"
        ],
        metadata={
            'impact_scope': ['database', 'all-services'],
            'required_expertise': ['engineering', 'operations'],
            'downtime_minutes': 120,
            'customer_impact': 'high'
        }
    )
    
    print(f"\nHistorical Incident:")
    print(f"  Date: {incident.timestamp.strftime('%Y-%m-%d at %I:%M %p')}")
    print(f"  Type: {incident.event_type}")
    print(f"  Description: {incident.description}")
    print(f"  Actual Outcome: {incident.outcome.upper()}")
    
    analysis = simulator.replay_historical_event(incident)
    
    print(f"\nSimulator Analysis:")
    simulated = analysis['simulated_decision']
    print(f"  Would Council Have Approved: {simulated['approved']}")
    print(f"  Would Have Prevented Issue: {analysis['would_have_prevented_issue']}")
    
    if analysis['would_have_prevented_issue']:
        print("\n✓ The council would have PREVENTED this disaster!")
    else:
        print("\n⚠️  The council would not have prevented this issue.")
    
    print(f"\nLessons Learned:")
    for lesson in incident.lessons:
        print(f"  • {lesson}")


def example_5_stress_test():
    """Example 5: Stress testing"""
    print_section("Example 5: Stress Testing Council Rules")
    
    simulator = create_default_council()
    
    print("\nRunning stress test with 50 random scenarios...")
    print("This tests the council against various times, risk levels, and conditions.\n")
    
    results = simulator.stress_test_rules(num_scenarios=50)
    
    print(f"Results:")
    print(f"  Total Scenarios: {results['total_scenarios']}")
    print(f"  Approved: {results['passed']} ({results['passed']/results['total_scenarios']*100:.1f}%)")
    print(f"  Rejected: {results['failed']} ({results['failed']/results['total_scenarios']*100:.1f}%)")
    print(f"\nSafety Blocks:")
    print(f"  Night Operations Blocked: {results['night_blocks']}")
    print(f"  Weekend Operations Blocked: {results['weekend_blocks']}")
    print(f"  Circuit Breaker Activations: {results['circuit_breaker_trips']}")
    
    print(f"\nSample Scenarios:")
    for scenario in results['scenarios'][:5]:
        print(f"  • {scenario['time']}")
        print(f"    Risk: {scenario['risk_level']}, Result: {'APPROVED' if scenario['approved'] else 'REJECTED'}")


def example_6_emergency_stop():
    """Example 6: Emergency stop (bypasses checks)"""
    print_section("Example 6: Emergency Stop Procedure")
    
    simulator = create_default_council()
    
    # Even at 3am, emergency stops should be allowed
    monday = datetime.now()
    days_to_monday = (7 - monday.weekday()) % 7
    if days_to_monday != 0 or monday.weekday() != 0:
        monday = monday + timedelta(days=days_to_monday if days_to_monday != 0 else 7)
    monday = monday.replace(hour=3, minute=0)
    
    proposal = Proposal(
        id="EMERGENCY-001",
        title="Emergency stop: Kill runaway process causing outage",
        decision_type=DecisionType.EMERGENCY_STOP,
        risk_level=RiskLevel.CRITICAL,
        impact_scope=["affected-service"],
        required_expertise=["operations"],
        timestamp=monday,
        metadata={
            "reason": "Runaway process consuming all database connections",
            "immediate_action_required": True
        }
    )
    
    print(f"\nEmergency Proposal: {proposal.title}")
    print(f"Time: {proposal.timestamp.strftime('%A, %I:%M %p')} (Night time)")
    print(f"Type: {proposal.decision_type.value.upper()}")
    
    result = simulator.simulate_decision(proposal)
    print_result(result, show_reasoning=False)
    
    print("\n⚡ Emergency procedures bypass normal time restrictions")
    print("   to allow critical incident response.")


def main():
    """Run all examples"""
    print("=" * 80)
    print("  iNFINITE AI 2025 Council Simulator - Usage Examples")
    print("  Demonstrating Highly Complex & Technically Accurate Decision Engine")
    print("=" * 80)
    
    example_1_safe_deployment()
    example_2_dangerous_night()
    example_3_custom_council()
    example_4_historical_replay()
    example_5_stress_test()
    example_6_emergency_stop()
    
    print("\n" + "=" * 80)
    print("  Examples Complete!")
    print("=" * 80)
    print("\n📚 For more information, see DOCUMENTATION.md")
    print("🧪 Run tests with: python test_simulator.py")
    print("🚀 Run full simulation with: python simulator.py\n")


if __name__ == "__main__":
    main()
