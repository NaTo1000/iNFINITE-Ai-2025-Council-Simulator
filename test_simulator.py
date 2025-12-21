#!/usr/bin/env python3
"""
Test suite for the iNFINITE AI 2025 Council Simulator
Comprehensive tests for all simulation components
"""

import unittest
from datetime import datetime, timedelta
from simulator import (
    CouncilMember, Proposal, DecisionType, RiskLevel, TimeWindow,
    SafetyGuard, CouncilSimulator, Event, create_default_council
)


class TestCouncilMember(unittest.TestCase):
    """Test CouncilMember functionality"""
    
    def setUp(self):
        self.member = CouncilMember(
            name="Test Member",
            role="Engineering",
            risk_tolerance=0.5,
            expertise=["engineering", "security"],
            voting_weight=1.0
        )
    
    def test_member_creation(self):
        """Test council member creation"""
        self.assertEqual(self.member.name, "Test Member")
        self.assertEqual(self.member.role, "Engineering")
        self.assertEqual(self.member.risk_tolerance, 0.5)
        self.assertIn("engineering", self.member.expertise)
    
    def test_evaluate_low_risk_proposal(self):
        """Test evaluation of low risk proposal"""
        proposal = Proposal(
            id="TEST-001",
            title="Low risk test",
            decision_type=DecisionType.DEPLOY,
            risk_level=RiskLevel.LOW,
            impact_scope=["test"],
            required_expertise=["engineering"],
            timestamp=datetime.now()
        )
        
        vote, confidence, reasoning = self.member.evaluate_proposal(
            proposal, {'time_window': TimeWindow.BUSINESS_HOURS}
        )
        
        self.assertTrue(vote)  # Should approve low risk
        self.assertGreater(confidence, 0.5)
    
    def test_evaluate_critical_risk_proposal(self):
        """Test evaluation of critical risk proposal"""
        proposal = Proposal(
            id="TEST-002",
            title="Critical risk test",
            decision_type=DecisionType.DEPLOY,
            risk_level=RiskLevel.CRITICAL,
            impact_scope=["production"],
            required_expertise=["engineering"],
            timestamp=datetime.now()
        )
        
        vote, confidence, reasoning = self.member.evaluate_proposal(
            proposal, {'time_window': TimeWindow.BUSINESS_HOURS}
        )
        
        # Critical risk should be rejected by moderate risk tolerance member
        self.assertFalse(vote)


class TestProposal(unittest.TestCase):
    """Test Proposal functionality"""
    
    def test_proposal_creation(self):
        """Test proposal creation"""
        proposal = Proposal(
            id="PROP-001",
            title="Test Proposal",
            decision_type=DecisionType.DEPLOY,
            risk_level=RiskLevel.MEDIUM,
            impact_scope=["service-a", "service-b"],
            required_expertise=["engineering"],
            timestamp=datetime.now()
        )
        
        self.assertEqual(proposal.id, "PROP-001")
        self.assertEqual(proposal.decision_type, DecisionType.DEPLOY)
        self.assertEqual(len(proposal.impact_scope), 2)
    
    def test_risk_score_calculation(self):
        """Test risk score calculation"""
        # Low risk proposal
        low_risk = Proposal(
            id="LOW-001",
            title="Low risk",
            decision_type=DecisionType.DEPLOY,
            risk_level=RiskLevel.LOW,
            impact_scope=["test"],
            required_expertise=["engineering"],
            timestamp=datetime.now()
        )
        self.assertLess(low_risk.calculate_risk_score(), 0.5)
        
        # Critical risk proposal with minimal scope
        critical_risk = Proposal(
            id="CRIT-001",
            title="Critical risk",
            decision_type=DecisionType.DEPLOY,
            risk_level=RiskLevel.CRITICAL,
            impact_scope=["all"],
            required_expertise=["engineering"],
            timestamp=datetime.now()
        )
        # Critical risk base is 0.95, but scope multiplier reduces it
        # With 1 service: 0.95 * 0.6 = 0.57
        self.assertGreater(critical_risk.calculate_risk_score(), 0.5)


class TestSafetyGuard(unittest.TestCase):
    """Test SafetyGuard functionality"""
    
    def setUp(self):
        self.guard = SafetyGuard()
    
    def test_business_hours_safe(self):
        """Test business hours are marked as safe"""
        # Create a Monday timestamp
        today = datetime.now()
        days_to_monday = (7 - today.weekday()) % 7  # Days until next Monday
        if days_to_monday == 0 and today.weekday() == 0:
            monday = today
        else:
            monday = today + timedelta(days=days_to_monday if days_to_monday != 0 else 7)
        timestamp = monday.replace(hour=14, minute=0)  # 2pm Monday
        safe, window, msg = self.guard.check_time_window(timestamp)
        
        self.assertTrue(safe)
        self.assertEqual(window, TimeWindow.BUSINESS_HOURS)
    
    def test_night_hours_unsafe(self):
        """Test night hours are blocked"""
        # Create a Monday timestamp at 3am
        today = datetime.now()
        days_to_monday = (7 - today.weekday()) % 7
        if days_to_monday == 0 and today.weekday() == 0:
            monday = today
        else:
            monday = today + timedelta(days=days_to_monday if days_to_monday != 0 else 7)
        timestamp = monday.replace(hour=3, minute=0)  # 3am Monday
        safe, window, msg = self.guard.check_time_window(timestamp)
        
        self.assertFalse(safe)
        self.assertEqual(window, TimeWindow.NIGHT)
        self.assertIn("Night operations prohibited", msg)
    
    def test_weekend_unsafe(self):
        """Test weekends are blocked"""
        # Create a Saturday timestamp
        today = datetime.now()
        days_ahead = 5 - today.weekday()  # 5 = Saturday
        if days_ahead <= 0:
            days_ahead += 7
        saturday = today + timedelta(days=days_ahead)
        saturday = saturday.replace(hour=14, minute=0)
        
        safe, window, msg = self.guard.check_time_window(saturday)
        
        self.assertFalse(safe)
        self.assertEqual(window, TimeWindow.WEEKEND)
    
    def test_circuit_breaker_normal(self):
        """Test circuit breaker in normal state"""
        ok, msg = self.guard.check_circuit_breaker(0.5)
        self.assertTrue(ok)
    
    def test_circuit_breaker_trips(self):
        """Test circuit breaker trips after failures"""
        # Record multiple failures
        for _ in range(3):
            self.guard.record_failure()
        
        ok, msg = self.guard.check_circuit_breaker(0.5)
        self.assertFalse(ok)
        self.assertIn("Circuit breaker OPEN", msg)
    
    def test_emergency_stop_bypasses(self):
        """Test emergency stop bypasses checks"""
        proposal = Proposal(
            id="EMERG-001",
            title="Emergency stop",
            decision_type=DecisionType.EMERGENCY_STOP,
            risk_level=RiskLevel.CRITICAL,
            impact_scope=["all"],
            required_expertise=["operations"],
            timestamp=datetime.now().replace(hour=3, minute=0)  # 3am
        )
        
        context = {}
        safe, warnings = self.guard.evaluate_proposal_safety(proposal, context)
        
        self.assertTrue(safe)
        self.assertTrue(any("EMERGENCY STOP" in w for w in warnings))


class TestCouncilSimulator(unittest.TestCase):
    """Test CouncilSimulator functionality"""
    
    def setUp(self):
        self.simulator = create_default_council()
    
    def test_council_creation(self):
        """Test council is created with members"""
        self.assertGreater(len(self.simulator.members), 0)
    
    def test_add_member(self):
        """Test adding a council member"""
        initial_count = len(self.simulator.members)
        
        new_member = CouncilMember(
            name="New Member",
            role="Test",
            risk_tolerance=0.5,
            expertise=["testing"],
            voting_weight=1.0
        )
        
        self.simulator.add_member(new_member)
        self.assertEqual(len(self.simulator.members), initial_count + 1)
    
    def test_simulate_safe_decision(self):
        """Test simulating a safe decision"""
        # Create a Monday timestamp
        today = datetime.now()
        days_to_monday = (7 - today.weekday()) % 7
        if days_to_monday == 0 and today.weekday() == 0:
            monday = today
        else:
            monday = today + timedelta(days=days_to_monday if days_to_monday != 0 else 7)
        
        proposal = Proposal(
            id="SAFE-001",
            title="Safe deployment",
            decision_type=DecisionType.DEPLOY,
            risk_level=RiskLevel.LOW,
            impact_scope=["test"],
            required_expertise=["engineering"],
            timestamp=monday.replace(hour=14, minute=0)  # 2pm Monday
        )
        
        result = self.simulator.simulate_decision(proposal)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.proposal_id, "SAFE-001")
        # Low risk during business hours should be approved
        self.assertTrue(result.approved)
    
    def test_simulate_unsafe_night_decision(self):
        """Test night deployment is blocked"""
        # Create a Monday timestamp at 3am
        today = datetime.now()
        days_to_monday = (7 - today.weekday()) % 7
        if days_to_monday == 0 and today.weekday() == 0:
            monday = today
        else:
            monday = today + timedelta(days=days_to_monday if days_to_monday != 0 else 7)
        
        proposal = Proposal(
            id="NIGHT-001",
            title="Night deployment",
            decision_type=DecisionType.DEPLOY,
            risk_level=RiskLevel.HIGH,
            impact_scope=["production"],
            required_expertise=["engineering"],
            timestamp=monday.replace(hour=3, minute=0)  # 3am Monday
        )
        
        result = self.simulator.simulate_decision(proposal)
        
        self.assertIsNotNone(result)
        self.assertFalse(result.approved)  # Should be blocked
        self.assertTrue(any("Night operations prohibited" in r for r in result.reasoning))
    
    def test_stress_test_runs(self):
        """Test stress test execution"""
        results = self.simulator.stress_test_rules(num_scenarios=10)
        
        self.assertEqual(results['total_scenarios'], 10)
        self.assertEqual(results['passed'] + results['failed'], 10)
        self.assertIn('night_blocks', results)
        self.assertIn('weekend_blocks', results)
    
    def test_historical_replay(self):
        """Test historical event replay"""
        event = Event(
            timestamp=datetime(2024, 12, 15, 3, 30),  # 3:30am
            event_type="Production Outage",
            description="Test incident",
            outcome="failure",
            lessons=["Don't deploy at night"],
            metadata={'impact_scope': ['production']}
        )
        
        analysis = self.simulator.replay_historical_event(event)
        
        self.assertIn('event', analysis)
        self.assertIn('simulated_decision', analysis)
        self.assertIn('would_have_prevented_issue', analysis)
    
    def test_generate_report(self):
        """Test report generation"""
        # Make some decisions first
        proposal = Proposal(
            id="REPORT-001",
            title="Test for report",
            decision_type=DecisionType.DEPLOY,
            risk_level=RiskLevel.LOW,
            impact_scope=["test"],
            required_expertise=["engineering"],
            timestamp=datetime.now().replace(hour=14, minute=0)
        )
        self.simulator.simulate_decision(proposal)
        
        report = self.simulator.generate_report()
        
        self.assertIn('summary', report)
        self.assertIn('council_members', report)
        self.assertIn('recent_decisions', report)
        self.assertGreater(report['summary']['total_decisions'], 0)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""
    
    def test_full_simulation_workflow(self):
        """Test complete simulation workflow"""
        simulator = create_default_council()
        
        # Create a Monday timestamp
        today = datetime.now()
        days_to_monday = (7 - today.weekday()) % 7
        if days_to_monday == 0 and today.weekday() == 0:
            monday = today
        else:
            monday = today + timedelta(days=days_to_monday if days_to_monday != 0 else 7)
        
        # Create multiple proposals with different characteristics
        proposals = [
            Proposal(
                id=f"INTEG-{i:03d}",
                title=f"Integration test {i}",
                decision_type=DecisionType.DEPLOY,
                risk_level=RiskLevel.LOW if i % 2 == 0 else RiskLevel.MEDIUM,
                impact_scope=["test"],
                required_expertise=["engineering"],
                timestamp=monday.replace(hour=14, minute=0)
            )
            for i in range(5)
        ]
        
        # Process all proposals
        results = [simulator.simulate_decision(p) for p in proposals]
        
        # Verify all were processed
        self.assertEqual(len(results), 5)
        self.assertEqual(len(simulator.decision_history), 5)
        
        # Verify report can be generated
        report = simulator.generate_report()
        self.assertEqual(report['summary']['total_decisions'], 5)
    
    def test_prevents_3am_disaster(self):
        """Critical test: Ensure 3am deployments are prevented"""
        simulator = create_default_council()
        
        # Create a Monday timestamp at 3am
        today = datetime.now()
        days_to_monday = (7 - today.weekday()) % 7
        if days_to_monday == 0 and today.weekday() == 0:
            monday = today
        else:
            monday = today + timedelta(days=days_to_monday if days_to_monday != 0 else 7)
        
        # The infamous 3am deployment that should never happen
        dangerous_proposal = Proposal(
            id="DANGER-3AM",
            title="Database migration at 3am",
            decision_type=DecisionType.DEPLOY,
            risk_level=RiskLevel.CRITICAL,
            impact_scope=["database", "all-services"],
            required_expertise=["engineering", "operations"],
            timestamp=monday.replace(hour=3, minute=0)
        )
        
        result = simulator.simulate_decision(dangerous_proposal)
        
        # THIS IS THE MOST IMPORTANT TEST
        # The simulator MUST block this to prevent production disasters
        self.assertFalse(result.approved, 
                        "CRITICAL FAILURE: 3am deployment was not blocked!")
        
        # Verify it was blocked by safety guard
        self.assertGreater(simulator.metrics['safety_blocks'], 0)


def run_tests():
    """Run all tests and print summary"""
    print("=" * 80)
    print("Running Test Suite for iNFINITE AI 2025 Council Simulator")
    print("=" * 80)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestCouncilMember))
    suite.addTests(loader.loadTestsFromTestCase(TestProposal))
    suite.addTests(loader.loadTestsFromTestCase(TestSafetyGuard))
    suite.addTests(loader.loadTestsFromTestCase(TestCouncilSimulator))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 80)
    print("Test Summary")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✓ All tests passed! The council is ready to prevent disasters.")
    else:
        print("\n✗ Some tests failed. Review and fix before deployment.")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
