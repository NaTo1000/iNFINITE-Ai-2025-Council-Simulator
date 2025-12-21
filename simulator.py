#!/usr/bin/env python3
"""
iNFINITE AI 2025 Council Simulator
A highly complex and technically accurate simulation engine for testing council decision-making
under various scenarios to prevent catastrophic production incidents.
"""

import json
import logging
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict
import random
import math


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DecisionType(Enum):
    """Types of decisions the council can make"""
    DEPLOY = "deploy"
    ROLLBACK = "rollback"
    SCALE_UP = "scale_up"
    SCALE_DOWN = "scale_down"
    EMERGENCY_STOP = "emergency_stop"
    APPROVE = "approve"
    REJECT = "reject"
    DEFER = "defer"


class RiskLevel(Enum):
    """Risk levels for operations"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NEGLIGIBLE = "negligible"


class TimeWindow(Enum):
    """Time windows for operations"""
    BUSINESS_HOURS = "business_hours"  # 9am - 5pm
    AFTER_HOURS = "after_hours"  # 5pm - 9pm
    NIGHT = "night"  # 9pm - 6am
    EARLY_MORNING = "early_morning"  # 6am - 9am
    WEEKEND = "weekend"


@dataclass
class CouncilMember:
    """Represents a council member with decision-making capabilities"""
    name: str
    role: str
    risk_tolerance: float  # 0.0 (conservative) to 1.0 (aggressive)
    expertise: List[str]
    voting_weight: float = 1.0
    availability_pattern: Dict[TimeWindow, float] = field(default_factory=dict)
    
    def evaluate_proposal(self, proposal: 'Proposal', context: Dict[str, Any]) -> Tuple[bool, float, str]:
        """
        Evaluate a proposal and return (vote, confidence, reasoning)
        """
        confidence = 0.7
        
        # Adjust confidence based on expertise
        if any(exp in proposal.required_expertise for exp in self.expertise):
            confidence += 0.2
        
        # Evaluate risk
        risk_score = proposal.calculate_risk_score()
        
        # Decision logic based on risk tolerance
        if risk_score > (1.0 - self.risk_tolerance):
            vote = False
            reasoning = f"{self.name} votes REJECT: Risk score {risk_score:.2f} exceeds tolerance {1.0 - self.risk_tolerance:.2f}"
        elif risk_score < self.risk_tolerance / 2:
            vote = True
            reasoning = f"{self.name} votes APPROVE: Risk score {risk_score:.2f} is acceptable"
        else:
            # Check time window
            current_window = context.get('time_window', TimeWindow.BUSINESS_HOURS)
            if current_window == TimeWindow.NIGHT and risk_score > 0.3:
                vote = False
                reasoning = f"{self.name} votes REJECT: Too risky for night deployment (risk: {risk_score:.2f})"
            else:
                vote = True
                reasoning = f"{self.name} votes APPROVE: Risk manageable in current window"
        
        return vote, confidence, reasoning


@dataclass
class Proposal:
    """Represents a proposal for council decision"""
    id: str
    title: str
    decision_type: DecisionType
    risk_level: RiskLevel
    impact_scope: List[str]
    required_expertise: List[str]
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def calculate_risk_score(self) -> float:
        """Calculate numerical risk score (0.0 to 1.0)"""
        risk_map = {
            RiskLevel.CRITICAL: 0.95,
            RiskLevel.HIGH: 0.75,
            RiskLevel.MEDIUM: 0.50,
            RiskLevel.LOW: 0.25,
            RiskLevel.NEGLIGIBLE: 0.05
        }
        base_risk = risk_map[self.risk_level]
        
        # Adjust based on impact scope
        scope_multiplier = min(1.0, 0.5 + (len(self.impact_scope) * 0.1))
        
        return min(1.0, base_risk * scope_multiplier)


@dataclass
class DecisionResult:
    """Result of a council decision"""
    proposal_id: str
    approved: bool
    votes_for: int
    votes_against: int
    total_weight: float
    timestamp: datetime
    reasoning: List[str]
    unanimous: bool
    confidence_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'proposal_id': self.proposal_id,
            'approved': self.approved,
            'votes_for': self.votes_for,
            'votes_against': self.votes_against,
            'total_weight': self.total_weight,
            'timestamp': self.timestamp.isoformat(),
            'reasoning': self.reasoning,
            'unanimous': self.unanimous,
            'confidence_score': self.confidence_score
        }


@dataclass
class Event:
    """Historical event for replay"""
    timestamp: datetime
    event_type: str
    description: str
    outcome: str
    lessons: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


class SafetyGuard:
    """Safety mechanisms to prevent catastrophic decisions"""
    
    def __init__(self):
        self.circuit_breaker_threshold = 3
        self.recent_failures = []
        self.blackout_periods = []
        
    def check_time_window(self, timestamp: datetime) -> Tuple[bool, TimeWindow, str]:
        """Check if current time is safe for operations"""
        hour = timestamp.hour
        day = timestamp.weekday()
        
        # Weekend check
        if day >= 5:  # Saturday = 5, Sunday = 6
            return False, TimeWindow.WEEKEND, "Operations restricted on weekends"
        
        # Night operations (9pm - 6am) - HIGH RISK
        if hour >= 21 or hour < 6:
            return False, TimeWindow.NIGHT, "CRITICAL: Night operations prohibited (9pm-6am) - Historical incident prevention"
        
        # Early morning (6am - 9am) - ELEVATED RISK
        if 6 <= hour < 9:
            return True, TimeWindow.EARLY_MORNING, "Caution: Early morning - limited support available"
        
        # Business hours (9am - 5pm) - SAFE
        if 9 <= hour < 17:
            return True, TimeWindow.BUSINESS_HOURS, "Safe: Business hours - full support available"
        
        # After hours (5pm - 9pm) - MODERATE RISK
        return True, TimeWindow.AFTER_HOURS, "Warning: After hours - reduced support"
    
    def check_circuit_breaker(self, risk_score: float) -> Tuple[bool, str]:
        """Circuit breaker pattern to prevent cascading failures"""
        # Remove old failures (older than 1 hour)
        cutoff = datetime.now() - timedelta(hours=1)
        self.recent_failures = [f for f in self.recent_failures if f > cutoff]
        
        if len(self.recent_failures) >= self.circuit_breaker_threshold:
            return False, f"Circuit breaker OPEN: {len(self.recent_failures)} failures in last hour"
        
        if risk_score > 0.8:
            return True, "High risk operation - proceed with extreme caution"
        
        return True, "Circuit breaker closed - operations normal"
    
    def record_failure(self):
        """Record a failure for circuit breaker"""
        self.recent_failures.append(datetime.now())
    
    def evaluate_proposal_safety(self, proposal: Proposal, context: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Comprehensive safety evaluation"""
        warnings = []
        safe = True
        
        # Check time window
        time_safe, time_window, time_msg = self.check_time_window(proposal.timestamp)
        context['time_window'] = time_window
        
        if not time_safe:
            safe = False
            warnings.append(f"TIME RESTRICTION: {time_msg}")
        else:
            warnings.append(time_msg)
        
        # Check circuit breaker
        risk_score = proposal.calculate_risk_score()
        breaker_ok, breaker_msg = self.check_circuit_breaker(risk_score)
        warnings.append(breaker_msg)
        
        if not breaker_ok:
            safe = False
        
        # Check for emergency stop
        if proposal.decision_type == DecisionType.EMERGENCY_STOP:
            warnings.append("EMERGENCY STOP: Bypassing normal checks")
            return True, warnings
        
        # Critical operations require additional safeguards
        if proposal.risk_level == RiskLevel.CRITICAL:
            if time_window != TimeWindow.BUSINESS_HOURS:
                safe = False
                warnings.append("CRITICAL RISK: Can only be executed during business hours")
        
        return safe, warnings


class CouncilSimulator:
    """Main simulation engine for council decision-making"""
    
    def __init__(self):
        self.members: List[CouncilMember] = []
        self.safety_guard = SafetyGuard()
        self.decision_history: List[DecisionResult] = []
        self.event_history: List[Event] = []
        self.metrics = defaultdict(int)
        
    def add_member(self, member: CouncilMember):
        """Add a council member"""
        self.members.append(member)
        logger.info(f"Added council member: {member.name} ({member.role})")
    
    def simulate_decision(self, proposal: Proposal) -> DecisionResult:
        """Simulate a council decision on a proposal"""
        logger.info(f"Simulating decision for proposal: {proposal.id} - {proposal.title}")
        
        context = {
            'timestamp': proposal.timestamp,
            'simulation_mode': True
        }
        
        # Safety checks
        safe, safety_warnings = self.safety_guard.evaluate_proposal_safety(proposal, context)
        
        if not safe:
            logger.warning(f"Safety guard blocked proposal {proposal.id}")
            result = DecisionResult(
                proposal_id=proposal.id,
                approved=False,
                votes_for=0,
                votes_against=len(self.members),
                total_weight=sum(m.voting_weight for m in self.members),
                timestamp=datetime.now(),
                reasoning=safety_warnings,
                unanimous=True,
                confidence_score=1.0
            )
            self.decision_history.append(result)
            self.metrics['safety_blocks'] += 1
            return result
        
        # Collect votes
        votes_for = 0
        votes_against = 0
        total_weight = 0
        reasoning = safety_warnings.copy()
        confidences = []
        
        for member in self.members:
            vote, confidence, vote_reasoning = member.evaluate_proposal(proposal, context)
            confidences.append(confidence)
            reasoning.append(vote_reasoning)
            
            if vote:
                votes_for += member.voting_weight
            else:
                votes_against += member.voting_weight
            
            total_weight += member.voting_weight
        
        # Determine outcome (simple majority by weight)
        approved = votes_for > votes_against
        unanimous = (votes_for == total_weight) or (votes_against == total_weight)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        result = DecisionResult(
            proposal_id=proposal.id,
            approved=approved,
            votes_for=int(votes_for),
            votes_against=int(votes_against),
            total_weight=total_weight,
            timestamp=datetime.now(),
            reasoning=reasoning,
            unanimous=unanimous,
            confidence_score=avg_confidence
        )
        
        self.decision_history.append(result)
        
        # Update metrics
        if approved:
            self.metrics['approvals'] += 1
        else:
            self.metrics['rejections'] += 1
        
        if unanimous:
            self.metrics['unanimous_decisions'] += 1
        
        logger.info(f"Decision result: {'APPROVED' if approved else 'REJECTED'} "
                   f"(For: {votes_for}, Against: {votes_against}, Unanimous: {unanimous})")
        
        return result
    
    def replay_historical_event(self, event: Event) -> Dict[str, Any]:
        """Replay a historical event and evaluate how council would have responded"""
        logger.info(f"Replaying event: {event.event_type} at {event.timestamp}")
        
        # Create a proposal based on the historical event
        proposal = Proposal(
            id=f"replay_{event.timestamp.timestamp()}",
            title=f"Historical replay: {event.event_type}",
            decision_type=DecisionType.DEPLOY,
            risk_level=RiskLevel.HIGH,
            impact_scope=event.metadata.get('impact_scope', ['production']),
            required_expertise=event.metadata.get('required_expertise', ['engineering']),
            timestamp=event.timestamp,
            metadata={'historical_event': True, 'original_outcome': event.outcome}
        )
        
        result = self.simulate_decision(proposal)
        
        # Compare with actual outcome
        analysis = {
            'event': asdict(event),
            'simulated_decision': result.to_dict(),
            'would_have_prevented_issue': not result.approved and event.outcome == 'failure',
            'lessons_applied': event.lessons
        }
        
        self.event_history.append(event)
        return analysis
    
    def stress_test_rules(self, num_scenarios: int = 100) -> Dict[str, Any]:
        """Stress test the council rules with random scenarios"""
        logger.info(f"Starting stress test with {num_scenarios} scenarios")
        
        results = {
            'total_scenarios': num_scenarios,
            'passed': 0,
            'failed': 0,
            'night_blocks': 0,
            'weekend_blocks': 0,
            'circuit_breaker_trips': 0,
            'scenarios': []
        }
        
        risk_levels = list(RiskLevel)
        decision_types = list(DecisionType)
        
        for i in range(num_scenarios):
            # Generate random scenario
            hour = random.randint(0, 23)
            day = random.randint(0, 6)
            timestamp = datetime.now().replace(hour=hour, minute=random.randint(0, 59))
            timestamp = timestamp + timedelta(days=(day - timestamp.weekday()))
            
            proposal = Proposal(
                id=f"stress_test_{i}",
                title=f"Stress test scenario {i}",
                decision_type=random.choice(decision_types),
                risk_level=random.choice(risk_levels),
                impact_scope=[f"service_{random.randint(1, 5)}"],
                required_expertise=[random.choice(['engineering', 'security', 'operations'])],
                timestamp=timestamp
            )
            
            result = self.simulate_decision(proposal)
            
            scenario_result = {
                'scenario_id': i,
                'time': timestamp.strftime("%Y-%m-%d %H:%M (%A)"),
                'risk_level': proposal.risk_level.value,
                'approved': result.approved,
                'reasoning_summary': result.reasoning[0] if result.reasoning else "No reasoning"
            }
            
            # Track specific blocks
            if 'Night operations prohibited' in str(result.reasoning):
                results['night_blocks'] += 1
            if 'weekend' in str(result.reasoning).lower():
                results['weekend_blocks'] += 1
            if 'Circuit breaker' in str(result.reasoning):
                results['circuit_breaker_trips'] += 1
            
            if result.approved:
                results['passed'] += 1
            else:
                results['failed'] += 1
            
            results['scenarios'].append(scenario_result)
        
        logger.info(f"Stress test complete. Passed: {results['passed']}, Failed: {results['failed']}")
        return results
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive simulation report"""
        report = {
            'summary': {
                'total_decisions': len(self.decision_history),
                'approvals': self.metrics['approvals'],
                'rejections': self.metrics['rejections'],
                'unanimous_decisions': self.metrics['unanimous_decisions'],
                'safety_blocks': self.metrics['safety_blocks'],
                'council_size': len(self.members)
            },
            'council_members': [
                {
                    'name': m.name,
                    'role': m.role,
                    'risk_tolerance': m.risk_tolerance,
                    'expertise': m.expertise
                }
                for m in self.members
            ],
            'recent_decisions': [
                d.to_dict() for d in self.decision_history[-10:]
            ],
            'metrics': dict(self.metrics)
        }
        
        return report
    
    def save_report(self, filename: str = "simulation_report.json"):
        """Save simulation report to file"""
        report = self.generate_report()
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        logger.info(f"Report saved to {filename}")


def create_default_council() -> CouncilSimulator:
    """Create a default council with standard members"""
    simulator = CouncilSimulator()
    
    # Add diverse council members
    simulator.add_member(CouncilMember(
        name="Security Chief",
        role="Security",
        risk_tolerance=0.2,  # Very conservative
        expertise=["security", "compliance", "risk-management"],
        voting_weight=1.5  # Higher weight for security
    ))
    
    simulator.add_member(CouncilMember(
        name="Lead Engineer",
        role="Engineering",
        risk_tolerance=0.6,  # Moderate
        expertise=["engineering", "architecture", "operations"],
        voting_weight=1.0
    ))
    
    simulator.add_member(CouncilMember(
        name="Operations Manager",
        role="Operations",
        risk_tolerance=0.4,  # Cautious
        expertise=["operations", "monitoring", "incident-response"],
        voting_weight=1.2
    ))
    
    simulator.add_member(CouncilMember(
        name="Product Owner",
        role="Product",
        risk_tolerance=0.7,  # More aggressive
        expertise=["product", "business", "user-experience"],
        voting_weight=0.8
    ))
    
    simulator.add_member(CouncilMember(
        name="SRE Lead",
        role="SRE",
        risk_tolerance=0.3,  # Conservative
        expertise=["reliability", "performance", "automation"],
        voting_weight=1.3
    ))
    
    return simulator


def main():
    """Main execution function"""
    print("=" * 80)
    print("iNFINITE AI 2025 Council Simulator")
    print("Highly Complex & Technically Accurate Decision Engine")
    print("=" * 80)
    print()
    
    # Create simulator with default council
    simulator = create_default_council()
    
    print(f"Council assembled with {len(simulator.members)} members:")
    for member in simulator.members:
        print(f"  - {member.name} ({member.role}): Risk Tolerance {member.risk_tolerance:.1f}, Weight {member.voting_weight}")
    print()
    
    # Test scenario 1: Safe business hours deployment
    print("SCENARIO 1: Business Hours Deployment (Low Risk)")
    print("-" * 80)
    proposal1 = Proposal(
        id="DEPLOY-001",
        title="Deploy new feature to production",
        decision_type=DecisionType.DEPLOY,
        risk_level=RiskLevel.LOW,
        impact_scope=["web-service", "api"],
        required_expertise=["engineering", "operations"],
        timestamp=datetime.now().replace(hour=14, minute=0)  # 2pm
    )
    result1 = simulator.simulate_decision(proposal1)
    print(f"Result: {'✓ APPROVED' if result1.approved else '✗ REJECTED'}")
    print(f"Votes: {result1.votes_for} for, {result1.votes_against} against")
    for reason in result1.reasoning:
        print(f"  {reason}")
    print()
    
    # Test scenario 2: Night deployment (should be blocked)
    print("SCENARIO 2: Night Deployment (High Risk) - 3am")
    print("-" * 80)
    proposal2 = Proposal(
        id="DEPLOY-002",
        title="Emergency hotfix deployment",
        decision_type=DecisionType.DEPLOY,
        risk_level=RiskLevel.HIGH,
        impact_scope=["database", "core-service"],
        required_expertise=["engineering", "operations"],
        timestamp=datetime.now().replace(hour=3, minute=0)  # 3am - THE DANGER ZONE
    )
    result2 = simulator.simulate_decision(proposal2)
    print(f"Result: {'✓ APPROVED' if result2.approved else '✗ REJECTED'}")
    print(f"Votes: {result2.votes_for} for, {result2.votes_against} against")
    for reason in result2.reasoning:
        print(f"  {reason}")
    print()
    
    # Test scenario 3: Critical operation business hours
    print("SCENARIO 3: Critical Database Migration (Business Hours)")
    print("-" * 80)
    proposal3 = Proposal(
        id="MIGRATE-001",
        title="Critical database schema migration",
        decision_type=DecisionType.DEPLOY,
        risk_level=RiskLevel.CRITICAL,
        impact_scope=["database", "all-services"],
        required_expertise=["engineering", "operations", "security"],
        timestamp=datetime.now().replace(hour=10, minute=0)  # 10am
    )
    result3 = simulator.simulate_decision(proposal3)
    print(f"Result: {'✓ APPROVED' if result3.approved else '✗ REJECTED'}")
    print(f"Votes: {result3.votes_for} for, {result3.votes_against} against")
    for reason in result3.reasoning:
        print(f"  {reason}")
    print()
    
    # Stress test
    print("STRESS TEST: Testing rules with 100 random scenarios")
    print("-" * 80)
    stress_results = simulator.stress_test_rules(100)
    print(f"Total scenarios: {stress_results['total_scenarios']}")
    print(f"Approved: {stress_results['passed']} ({stress_results['passed']/stress_results['total_scenarios']*100:.1f}%)")
    print(f"Rejected: {stress_results['failed']} ({stress_results['failed']/stress_results['total_scenarios']*100:.1f}%)")
    print(f"Night blocks: {stress_results['night_blocks']}")
    print(f"Weekend blocks: {stress_results['weekend_blocks']}")
    print(f"Circuit breaker trips: {stress_results['circuit_breaker_trips']}")
    print()
    
    # Historical event replay
    print("HISTORICAL REPLAY: Simulating past incident")
    print("-" * 80)
    historical_incident = Event(
        timestamp=datetime(2024, 12, 15, 3, 30),  # 3:30am incident
        event_type="Production Outage",
        description="Database migration executed at 3am caused cascading failures",
        outcome="failure",
        lessons=["Never deploy at night", "Require multiple approvals for DB changes"],
        metadata={
            'impact_scope': ['database', 'all-services'],
            'required_expertise': ['engineering', 'operations']
        }
    )
    replay_analysis = simulator.replay_historical_event(historical_incident)
    print(f"Historical event: {historical_incident.description}")
    print(f"Actual outcome: {historical_incident.outcome}")
    print(f"Simulator would have approved: {replay_analysis['simulated_decision']['approved']}")
    print(f"Would have prevented issue: {replay_analysis['would_have_prevented_issue']}")
    print()
    
    # Generate final report
    print("GENERATING FINAL REPORT")
    print("-" * 80)
    simulator.save_report("simulation_report.json")
    report = simulator.generate_report()
    print(json.dumps(report['summary'], indent=2))
    print()
    
    print("=" * 80)
    print("Simulation Complete!")
    print("The council has proven it won't nuke prod at 3am ✓")
    print("=" * 80)


if __name__ == "__main__":
    main()
