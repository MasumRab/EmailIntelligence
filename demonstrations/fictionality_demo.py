"""
Comprehensive Fictionality Detection Demonstration
================================================

Interactive demonstration showcasing the complete fictionality integration
for PR conflict resolution automation.

This script demonstrates:
- Realistic vs fictional PR conflict scenarios
- GraphQL queries and mutations
- Fictionality analysis results and strategy recommendations
- Batch processing examples
- Analytics and filtering capabilities
"""

import asyncio
import time
import sys
from typing import List, Dict, Any
from datetime import datetime, timedelta
from pathlib import Path

# Add the src directory to Python path before imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import required modules (demonstration file imports)
from ai.fictionality_analyzer import get_fictionality_analyzer
from models.fictionality_models import FictionalityContext
from database.data_access import fictionality_dao


class FictionalityDemo:
    """Interactive fictionality detection demonstration"""
    
    def __init__(self):
        self.analyzer = None
        self.demo_scenarios = self._load_demo_scenarios()
        self.demo_results = []
        
    def _load_demo_scenarios(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load demonstration scenarios"""
        return {
            "realistic": [
                {
                    "id": "real_001",
                    "pr_id": "pr_real_001",
                    "conflict_id": "conflict_real_001",
                    "title": "Fix user authentication middleware timeout",
                    "content": """
                    PR: Improve authentication middleware timeout handling
                    
                    Conflict: Authentication middleware timeout configuration is causing
                    issues in production when user load exceeds 1000 concurrent users.
                    The current timeout of 30 seconds is insufficient for database
                    connection pooling under high load.
                    
                    Technical details:
                    - Current timeout: 30 seconds (configurable via AUTH_TIMEOUT env var)
                    - Production load: 800-1200 concurrent users
                    - Database connection pool: max 100 connections
                    - Average auth request time: 2-5 seconds (99th percentile: 15s)
                    - Issue: Connections timeout during peak hours
                    
                    Proposed solution:
                    1. Increase timeout to 60 seconds for high-load scenarios
                    2. Implement connection health checking
                    3. Add retry logic with exponential backoff
                    4. Monitor connection pool metrics
                    
                    Files affected:
                    - src/middleware/auth.py (timeout logic)
                    - config/auth.yaml (timeout configuration)
                    - tests/integration/test_auth_timeout.py (new test file)
                    """,
                    "expected_score": 0.1, "confidence": "HIGHLY_REAL",
                    "indicators": ["Specific timeout values", "Realistic user numbers"]
                },
                {
                    "id": "real_002",
                    "pr_id": "pr_real_002",
                    "conflict_id": "conflict_real_002",
                    "title": "Memory leak in notification service",
                    "content": """
                    PR: Fix memory leak in notification service during high-volume events
                    
                    Conflict: The notification service exhibits a memory leak during events
                    with >10,000 notifications per hour. Memory usage grows from ~200MB
                    to ~2.5GB over 6 hours, requiring service restart.
                    
                    Technical investigation:
                    - Memory profiler shows 80% of growth in notification queue objects
                    - Event listeners not being properly removed after processing
                    - Redis connection objects accumulating over time
                    - Background worker goroutines not terminating correctly
                    
                    Observed symptoms:
                    - GC pressure increasing from 5% to 35% of CPU time
                    - Heap size growing from 200MB to 2.5GB
                    - Response time degrading from 50ms to 2.5s
                    - Service becomes unresponsive after ~6 hours
                    
                    Root cause:
                    - NotificationEvent objects held in memory indefinitely
                    - No proper cleanup in event disposal patterns
                    - Connection pooling not releasing unused connections
                    
                    Files affected:
                    src/services/notification/service.py (event cleanup)
                    src/services/notification/queue.py (connection management)
                    tests/performance/test_notification_leak.py (new test)
                    """,
                    "expected_score": 0.15,
                    "confidence": "HIGHLY_REAL",
                    "indicators": ["Specific memory numbers", "Realistic performance metrics"]
                }
            ],
            "fictional": [
                {
                    "id": "fict_001",
                    "pr_id": "pr_fict_001", 
                    "conflict_id": "conflict_fict_001",
                    "title": "Implement quantum computing authentication",
                    "content": """
                    PR: Add quantum computing based authentication system
                    
                    Conflict: We need to implement quantum computing authentication
                    to handle the massive scale of users we expect in the future.
                    The current system won't work when we have millions of users
                    logging in simultaneously.
                    
                    Technical requirements:
                    - Use quantum entanglement for secure token generation
                    - Implement quantum key distribution for encryption
                    - Create quantum-resistant hash algorithms
                    - Build quantum neural networks for user behavior analysis
                    - Deploy quantum cloud infrastructure for scaling
                    
                    Performance expectations:
                    - Handle 1 billion concurrent users
                    - Sub-nanosecond authentication response
                    - Zero security breaches guaranteed
                    - Quantum tunneling for instant communication
                    
                    Implementation approach:
                    1. Install quantum processors on all servers
                    2. Rewrite entire authentication flow
                    3. Deploy quantum blockchain
                    4. Train quantum AI models
                    5. Test with simulated reality
                    
                    Files to modify:
                    - src/auth/quantum_auth.py (new)
                    - src/security/quantum_encryption.py (new)
                    - src/ai/quantum_neural_net.py (new)
                    - config/quantum_infrastructure.yaml (new)
                    """,
                    "expected_score": 0.95,
                    "confidence": "HIGHLY_FICTIONAL", "indicators": [
                        "Impossible quantum claims", "Unrealistic performance numbers"
                    ]
                },
                {
                    "id": "fict_002",
                    "pr_id": "pr_fict_002",
                    "conflict_id": "conflict_fict_002",
                    "title": "Time travel debugging feature",
                    "content": """
                    PR: Implement time travel debugging for instant bug fixes
                    
                    Conflict: Our development process is too slow because developers
                    have to manually trace through code to find bugs. We need a time
                    travel feature that lets us go back in time to prevent bugs from
                    happening in the first place.
                    
                    Technical approach:
                    - Implement temporal version control system
                    - Create historical code state snapshots
                    - Build time-space continuum debugging interface
                    - Use quantum retrocausality for code modification
                    - Deploy distributed timeline servers
                    
                    Features to implement:
                    1. Instant time travel to any point in code execution
                    2. Reverse debugging with step-back functionality
                    3. Time-lag compensation for network delays
                    4. Parallel universe code testing
                    5. Automated time paradox prevention
                    
                    Performance metrics:
                    - Instant bug detection and prevention
                    - 100% elimination of production issues
                    - Time travel accuracy: 99.999% (quantum margin of error)
                    - Historical code preservation: infinite retention
                    
                    Files to create:
                    - src/debug/time_travel.py (temporal debugging)
                    - src/storage/timeline_server.py (historical storage)
                    - src/quantum/retrocausality.py (causality handling)
                    - config/temporal_infrastructure.yaml (time travel config)
                    - tests/time/test_chronological_debugging.py (temporal tests)
                    """,
                    "expected_score": 0.98, "confidence": "HIGHLY_FICTIONAL",
                    "indicators": ["Time travel concepts", "Impossible debugging features"]
                }
            ],
            "edge_cases": [
                {
                    "id": "edge_001",
                    "pr_id": "pr_edge_001",
                    "conflict_id": "conflict_edge_001", 
                    "title": "Cache performance optimization",
                    "content": """
                    PR: Optimize cache performance for medium-scale deployment
                    
                    Conflict: We need to improve cache performance in our application
                    that serves approximately 10,000-50,000 requests per minute.
                    The current cache hit rate is around 75% but we want to improve it.
                    
                    Current situation:
                    - 25,000 requests per minute average
                    - 75% cache hit rate
                    - Cache size: 2GB with 4-hour TTL
                    - Average response time: 150ms
                    - Target: 90% hit rate, <100ms response time
                    
                    Technical considerations:
                    - Redis cluster with 3 master nodes
                    - LRU eviction policy
                    - JSON serialization for cache values
                    - Connection pooling with 50 connections per node
                    - Monitoring shows some hot keys causing bottlenecks
                    
                    Potential improvements:
                    1. Implement cache warming strategy for frequently accessed data
                    2. Add cache compression for large objects
                    3. Optimize serialization format (JSON vs MessagePack)
                    4. Implement cache partitioning for hot/cold data
                    5. Add predictive preloading based on access patterns
                    
                    Measurement plan:
                    - Track cache hit rate per endpoint
                    - Monitor response time distribution
                    - Measure memory usage and fragmentation
                    - Analyze hot key patterns
                    """,
                    "expected_score": 0.3, "confidence": "UNCERTAIN",
                    "indicators": ["Moderate specificity", "Realistic but not detailed"]
                },
                {
                    "id": "edge_002",
                    "pr_id": "pr_edge_002",
                    "conflict_id": "conflict_edge_002",
                    "title": "Database connection pool tuning",
                    "content": """
                    PR: Tune database connection pool for optimal performance
                    
                    Conflict: The application sometimes experiences database connection
                    timeouts during peak usage. We have around 200-500 concurrent users
                    and the current pool configuration might not be optimal.
                    
                    Context:
                    - PostgreSQL 13 database
                    - Application running on 5 server instances
                    - 300-400 concurrent users during peak hours
                    - Current pool: 20 connections per instance
                    - Issue: Occasional connection timeouts (5-10 per hour)
                    
                    Potential factors:
                    - Connection pool might be too small
                    - Long-running queries holding connections
                    - Network latency between app and database
                    - Connection leak in some code paths
                    
                    Investigation needed:
                    - Analyze query performance and duration
                    - Check for connection leaks in monitoring
                    - Review connection timeout configuration
                    - Examine database server resource utilization
                    - Test different pool sizes under load
                    
                    Budget considerations:
                    - Database upgrade would be expensive
                    - Prefer tuning existing configuration
                    - May need to optimize slow queries instead
                    """,
                    "expected_score": 0.35, "confidence": "UNCERTAIN",
                    "indicators": ["Realistic scenario but lacks specifics", "Common uncertainty"]
                }
            ]
        }
    
    async def initialize(self):
        """Initialize the demo"""
        print("🚀 Initializing Fictionality Detection Demo...")
        self.analyzer = await get_fictionality_analyzer()
        print("✅ Fictionality analyzer initialized")
    
    async def run_demo(self):
        """Run the complete demonstration"""
        print("\n" + "="*80)
        print("🎭 FICTIONALITY DETECTION INTEGRATION DEMONSTRATION")
        print("="*80)
        
        # 1. Health Check
        await self._demo_health_check()
        
        # 2. Single Analysis Demo
        await self._demo_single_analysis()
        
        # 3. Realistic vs Fictional Comparison
        await self._demo_realistic_vs_fictional()
        
        # 4. Batch Processing Demo
        await self._demo_batch_processing()
        
        # 5. Filtering and Analytics Demo  
        await self._demo_filtering_analytics()
        
        # 6. Performance Metrics Demo
        await self._demo_performance_metrics()
        
        # 7. Strategy Integration Demo
        await self._demo_strategy_integration()
        
        # 8. Interactive Analysis Demo
        await self._demo_interactive_analysis()
        
        # Final summary
        await self._demo_summary()
    
    async def _demo_health_check(self):
        """Demonstrate health check functionality"""
        print("\n🏥 DEMO 1: Fictionality Service Health Check")
        print("-" * 50)
        
        try:
            health = await self.analyzer.health_check()
            print(f"Status: {health.get('status', 'unknown')}")
            print(f"Healthy: {health.get('healthy', False)}")
            print(f"Response Time: {health.get('response_time', 0):.3f}s")
            print(f"Uptime: {health.get('uptime', 0):.0f}s")
            print(f"Circuit Breaker: {health.get('circuit_breaker_state', 'unknown')}")
            print(f"Cache Hit Rate: {health.get('cache_hit_rate', 0):.2%}")
            print("✅ Health check completed successfully")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
    
    async def _demo_single_analysis(self):
        """Demonstrate single fictionality analysis"""
        print("\n🔍 DEMO 2: Single Fictionality Analysis")
        print("-" * 50)
        
        # Use a realistic scenario
        scenario = self.demo_scenarios["realistic"][0]
        
        pr_data = {"id": scenario["pr_id"], "title": scenario["title"]}
        conflict_data = {
            "id": scenario["conflict_id"],
            "type": "technical",
            "description": "Technical implementation details"
        }
        
        context = FictionalityContext(
            pr_data=pr_data,
            conflict_data=conflict_data,
            content_to_analyze=scenario["content"],
            analysis_depth="standard",
            include_strategies=True
        )
        
        print("Analyzing: {}".format(scenario['title']))
        print("Expected: {} (score: {})".format(
            scenario['confidence'], scenario['expected_score']))
        
        # start_time = time.time()  # assigned but never used
        result = await self.analyzer.analyze_fictionality(context)
        # analysis_time = time.time() - start_time  # assigned but never used
        
        if result.success and result.analysis:
            analysis = result.analysis
            print("\n📊 Analysis Results:")
            print(f"   Score: {analysis.fictionality_score:.3f}")
            print(f"   Confidence: {analysis.confidence_level.value}")
            print(f"   Processing Time: {analysis.processing_time:.3f}s")
            print(f"   Cached: {result.cached}")
            print(f"   Model: {analysis.model}")
            
            if analysis.fictionality_indicators:
                print("   Fictionality Indicators: {}".format(len(analysis.fictionality_indicators)))
                for indicator in analysis.fictionality_indicators[:3]:
                    print(f"     - {indicator}")
            
            if analysis.realism_indicators:
                print("   Realism Indicators: {}".format(len(analysis.realism_indicators)))
                for indicator in analysis.realism_indicators[:3]:
                    print(f"     - {indicator}")
            
            if analysis.strategy_adjustments:
                print("   Strategy Adjustments: {}".format(len(analysis.strategy_adjustments)))
                for adjustment in analysis.strategy_adjustments[:2]:
                    print(f"     - {adjustment}")
            
            print("✅ Single analysis completed")
            self.demo_results.append(("single_analysis", result))
        else:
            print(f"❌ Analysis failed: {result.error}")
    
    async def _demo_realistic_vs_fictional(self):
        """Demonstrate realistic vs fictional scenario detection"""
        print("\n⚖️ DEMO 3: Realistic vs Fictional Comparison")
        print("-" * 50)
        
        # Analyze one realistic and one fictional scenario
        realistic = self.demo_scenarios["realistic"][0]
        fictional = self.demo_scenarios["fictional"][0]
        
        scenarios = [
            ("Realistic", realistic, "🟢"),
            ("Fictional", fictional, "🔴")
        ]
        
        results = []
        
        for scenario_type, scenario, emoji in scenarios:
            print(f"\n{emoji} Analyzing {scenario_type} Scenario: {scenario['title']}")
            
            pr_data = {"id": scenario["pr_id"], "title": scenario["title"]}
            conflict_data = {"id": scenario["conflict_id"], "type": "technical"}
            
            context = FictionalityContext(
                pr_data=pr_data,
                conflict_data=conflict_data,
                content_to_analyze=scenario["content"],
                analysis_depth="standard"
            )
            
            result = await self.analyzer.analyze_fictionality(context)
            results.append((scenario_type, result))
            
            if result.success and result.analysis:
                analysis = result.analysis
                print(f"   Score: {analysis.fictionality_score:.3f} (Expected: {scenario['expected_score']})")
                print(f"   Confidence: {analysis.confidence_level.value}")
                print(f"   Reasoning: {analysis.reasoning[:100]}...")
            else:
                print(f"   ❌ Analysis failed: {result.error}")
        
        print("\n📈 Comparison Summary:")
        for i, (scenario_type, result) in enumerate(results):
            if result.success and result.analysis:
                score = result.analysis.fictionality_score
                confidence = result.analysis.confidence_level.value
                emoji = "🟢" if score < 0.5 else "🔴"
                print(f"   {emoji} {scenario_type}: {score:.3f} ({confidence})")
        
        print("✅ Realistic vs fictional comparison completed")
    
    async def _demo_batch_processing(self):
        """Demonstrate batch processing capabilities"""
        print("\n📦 DEMO 4: Batch Processing")
        print("-" * 50)
        
        # Create a mixed batch of realistic and fictional scenarios
        batch_scenarios = []
        batch_scenarios.extend(self.demo_scenarios["realistic"][:2])
        batch_scenarios.extend(self.demo_scenarios["fictional"][:2])
        batch_scenarios.append(self.demo_scenarios["edge_cases"][0])
        
        print(f"Processing {len(batch_scenarios)} scenarios in batch...")
        
        contexts = []
        for scenario in batch_scenarios:
            pr_data = {"id": scenario["pr_id"], "title": scenario["title"]}
            conflict_data = {"id": scenario["conflict_id"], "type": "technical"}
            
            context = FictionalityContext(
                pr_data=pr_data,
                conflict_data=conflict_data,
                content_to_analyze=scenario["content"],
                analysis_depth="standard"
            )
            contexts.append(context)
        
        start_time = time.time()
        results = await self.analyzer.batch_analyze_fictionality(contexts, max_concurrent=2)
        total_time = time.time() - start_time
        
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful
        
        print("✅ Batch processing completed:")
        print("   Total: {}".format(len(results)))
        print("   Successful: {}".format(successful))
        print("   Failed: {}".format(failed))
        print("   Total Time: {:.2f}s".format(total_time))
        print("   Average per analysis: {:.2f}s".format(total_time/len(results)))
        
        # Show distribution of fictionality scores
        scores = [r.analysis.fictionality_score for r in results if r.success and r.analysis]
        if scores:
            print("   Score Range: {:.3f} - {:.3f}".format(min(scores), max(scores)))
            print("   Average Score: {:.3f}".format(sum(scores)/len(scores)))
        
        self.demo_results.append(("batch_processing", results))
    
    async def _demo_filtering_analytics(self):
        """Demonstrate filtering and analytics capabilities"""
        print("\n🔍 DEMO 5: Filtering and Analytics")
        print("-" * 50)
        
        try:
            # Get recent analyses from database
            analyses = await fictionality_dao.get_analyses(limit=20)
            
            if analyses:
                print("Retrieved {} analyses from database".format(len(analyses)))
                
                # Calculate statistics
                scores = [a.fictionality_score for a in analyses]
                avg_score = sum(scores) / len(scores) if scores else 0
                
                high_fictional = sum(1 for s in scores if s >= 0.8)
                uncertain = sum(1 for s in scores if 0.4 <= s < 0.6)
                low_fictional = sum(1 for s in scores if s < 0.4)
                
                print("📊 Analytics Summary:")
                print("   Average Score: {:.3f}".format(avg_score))
                print("   High Fictional (≥0.8): {}".format(high_fictional))
                print("   Uncertain (0.4-0.6): {}".format(uncertain))
                print("   Low Fictional (<0.4): {}".format(low_fictional))
                
                # Show score distribution
                distribution = {
                    "High (≥0.8)": 0,
                    "Medium-High (0.6-0.8)": 0,
                    "Medium (0.4-0.6)": 0,
                    "Medium-Low (0.2-0.4)": 0,
                    "Low (<0.2)": 0
                }
                
                for score in scores:
                    if score >= 0.8:
                        distribution["High (≥0.8)"] += 1
                    elif score >= 0.6:
                        distribution["Medium-High (0.6-0.8)"] += 1
                    elif score >= 0.4:
                        distribution["Medium (0.4-0.6)"] += 1
                    elif score >= 0.2:
                        distribution["Medium-Low (0.2-0.4)"] += 1
                    else:
                        distribution["Low (<0.2)"] += 1
                
                print("📈 Score Distribution:")
                for range_name, count in distribution.items():
                    if count > 0:
                        percentage = (count / len(scores)) * 100
                        print("   {}: {} ({:.1f}%)".format(range_name, count, percentage))
            else:
                print("No analyses found in database for analytics")
                
            # Get metrics
            metrics = await fictionality_dao.get_metrics(
                start_time=datetime.utcnow() - timedelta(days=7),
                end_time=datetime.utcnow()
            )
            
            if metrics:
                print("📈 7-Day Metrics:")
                print("   Total Analyses: {}".format(metrics.total_analyses))
                print("   Average Score: {:.3f}".format(metrics.average_score))
                print("   Avg Processing Time: {:.3f}s".format(metrics.average_processing_time))
            
            print("✅ Filtering and analytics demo completed")
            
        except Exception as e:
            print("❌ Analytics demo failed: {}".format(e))
    
    async def _demo_performance_metrics(self):
        """Demonstrate performance monitoring"""
        print("\n⚡ DEMO 6: Performance Metrics")
        print("-" * 50)
        
        # Get analyzer statistics
        stats = self.analyzer.get_stats()
        
        print("📊 Analyzer Performance Stats:")
        print("   Analyses Completed: {}".format(stats['analyses_completed']))
        print("   Total Processing Time: {:.2f}s".format(stats['total_processing_time']))
        print("   Average Processing Time: {:.3f}s".format(stats['average_processing_time']))
        print("   Cache Hit Rate: {:.2%}".format(stats['cache_hit_rate']))
        print("   Cache Hits: {}".format(stats['cache_hits']))
        print("   Cache Misses: {}".format(stats['cache_misses']))
        print("   Errors: {}".format(stats['errors']))
        print("   Uptime: {:.0f}s".format(stats['uptime']))
        
        # Test performance with a small batch
        print("\n⏱️ Performance Test:")
        test_scenarios = self.demo_scenarios["realistic"][:3]
        
        contexts = []
        for scenario in test_scenarios:
            pr_data = {"id": scenario["pr_id"], "title": scenario["title"]}
            conflict_data = {"id": scenario["conflict_id"], "type": "technical"}
            
            context = FictionalityContext(
                pr_data=pr_data,
                conflict_data=conflict_data,
                content_to_analyze=scenario["content"],
                analysis_depth="quick"  # Use quick analysis for performance test
            )
            contexts.append(context)
        
        start_time = time.time()
        results = await self.analyzer.batch_analyze_fictionality(contexts, max_concurrent=1)
        test_time = time.time() - start_time
        
        successful = sum(1 for r in results if r.success)
        print("   Test Results: {}/{} successful".format(successful, len(results)))
        print("   Total Test Time: {:.2f}s".format(test_time))
        print("   Average per Analysis: {:.2f}s".format(test_time/len(results)))
        
        if successful > 0:
            avg_processing = sum(r.analysis.processing_time for r in results if r.success and r.analysis) / successful
            print("   Average AI Processing: {:.2f}s".format(avg_processing))
        
        print("✅ Performance metrics demo completed")
    
    async def _demo_strategy_integration(self):
        """Demonstrate strategy generation with fictionality awareness"""
        print("\n🎯 DEMO 7: Strategy Integration")
        print("-" * 50)
        
        # Test with different fictionality levels
        test_cases = [
            ("High Fictionality", self.demo_scenarios["fictional"][0]),
            ("Realistic Scenario", self.demo_scenarios["realistic"][0]),
            ("Uncertain Case", self.demo_scenarios["edge_cases"][0])
        ]
        
        for case_name, scenario in test_cases:
            print("\n🎲 {} Strategy Generation:".format(case_name))
            
            pr_data = {"id": scenario["pr_id"], "title": scenario["title"]}
            conflict_data = {"id": scenario["conflict_id"], "type": "technical"}
            
            context = FictionalityContext(
                pr_data=pr_data,
                conflict_data=conflict_data,
                content_to_analyze=scenario["content"],
                analysis_depth="standard",
                include_strategies=True
            )
            
            result = await self.analyzer.analyze_fictionality(context)
            
            if result.success and result.analysis:
                analysis = result.analysis
                print("   Fictionality Score: {:.3f}".format(analysis.fictionality_score))
                print("   Confidence: {}".format(analysis.confidence_level.value))
                
                if analysis.resolution_impact:
                    print("   Resolution Impact: {}".format(analysis.resolution_impact))
                
                if analysis.strategy_adjustments:
                    print("   Strategy Adjustments ({}):".format(len(analysis.strategy_adjustments)))
                    for adjustment in analysis.strategy_adjustments[:3]:
                        print("     • {}".format(adjustment))
                
                # Show how fictionality affects automation confidence
                if analysis.fictionality_score >= 0.8:
                    automation_level = "Manual Review Required"
                elif analysis.fictionality_score >= 0.6:
                    automation_level = "High Caution - Enhanced Validation"
                elif analysis.fictionality_score >= 0.4:
                    automation_level = "Standard with Monitoring"
                else:
                    automation_level = "Full Automation Recommended"
                
                print("   Automation Recommendation: {}".format(automation_level))
            else:
                print("   ❌ Analysis failed: {}".format(result.error))
        
        print("✅ Strategy integration demo completed")
    
    async def _demo_interactive_analysis(self):
        """Demonstrate interactive analysis capabilities"""
        print("\n🖥️ DEMO 8: Interactive Analysis")
        print("-" * 50)
        
        print("Enter your own content for fictionality analysis (or press Enter to skip):")
        
        # Sample content for demonstration
        sample_content = """This is a sample conflict description that we can analyze.
        The user is experiencing issues with database performance when the system
        handles more than 100 concurrent users. The current timeout of 30 seconds
        needs to be increased to 60 seconds and we should add connection pooling.
        This is a common scaling issue that many applications face."""
        
        user_input = input("Sample content: {}\nYour content (or press Enter): ".format(sample_content)).strip()
        
        if not user_input:
            user_input = sample_content
        
        print("\n🔍 Analyzing your content...")
        
        pr_data = {"id": "demo_user_input", "title": "User Input Analysis"}
        conflict_data = {"id": "user_conflict", "type": "user_input"}
        
        context = FictionalityContext(
            pr_data=pr_data,
            conflict_data=conflict_data,
            content_to_analyze=user_input,
            analysis_depth="standard",
            include_strategies=True
        )
        
        result = await self.analyzer.analyze_fictionality(context)
        
        if result.success and result.analysis:
            analysis = result.analysis
            print("\n📊 Your Content Analysis:")
            print("   Fictionality Score: {:.3f}".format(analysis.fictionality_score))
            print("   Confidence: {}".format(analysis.confidence_level.value))
            print("   Reasoning: {}".format(analysis.reasoning))
            
            if analysis.fictionality_indicators:
                print("   Fictionality Indicators Found:")
                for indicator in analysis.fictionality_indicators:
                    print("     • {}".format(indicator))
            
            if analysis.realism_indicators:
                print("   Realism Indicators Found:")
                for indicator in analysis.realism_indicators:
                    print("     • {}".format(indicator))
            
            if analysis.strategy_adjustments:
                print("   Recommended Adjustments:")
                for adjustment in analysis.strategy_adjustments:
                    print("     • {}".format(adjustment))
        else:
            print("❌ Analysis failed: {}".format(result.error))
        
        print("✅ Interactive analysis demo completed")
    
    async def _demo_summary(self):
        """Display demo summary and statistics"""
        print("\n" + "="*80)
        print("📋 DEMONSTRATION SUMMARY")
        print("="*80)
        
        stats = self.analyzer.get_stats()
        
        print("📊 Total Demonstrations Run: 8")
        print("🔬 Fictionality Analyses Completed: {}".format(stats['analyses_completed']))
        print("⏱️ Total Processing Time: {:.2f}s".format(stats['total_processing_time']))
        print("⚡ Average Analysis Time: {:.3f}s".format(stats['average_processing_time']))
        print("💾 Cache Hit Rate: {:.2%}".format(stats['cache_hit_rate']))
        print("❌ Errors Encountered: {}".format(stats['errors']))
        print("⏰ Service Uptime: {:.0f}s".format(stats['uptime']))
        
        print("\n🎯 Key Features Demonstrated:")
        print("   ✅ Health checking and monitoring")
        print("   ✅ Single and batch fictionality analysis")
        print("   ✅ Realistic vs fictional detection")
        print("   ✅ Performance optimization with caching")
        print("   ✅ Analytics and trend analysis")
        print("   ✅ Strategy generation with fictionality awareness")
        print("   ✅ Interactive content analysis")
        print("   ✅ Integration with existing resolution workflows")
        
        print("\n💡 Fictionality Detection Benefits:")
        print("   🛡️ Identifies potentially fictional or speculative content")
        print("   ⚖️ Provides confidence-based assessment (0.0-1.0 scale)")
        print("   🎯 Generates strategy adjustments based on fictionality level")
        print("   📊 Offers comprehensive analytics and monitoring")
        print("   🔄 Integrates seamlessly with existing PR resolution system")
        print("   ⚡ Optimized for performance with caching and batch processing")
        
        print("\n🚀 Next Steps:")
        print("   1. Explore the demo scenarios in tests/demo_scenarios/")
        print("   2. Try the GraphQL client in demo/demo_graphql_client.py")
        print("   3. Generate custom test data with demo_data_generator.py")
        print("   4. Review integration examples in examples/fictionality_integration.py")
        
        print("\n🎉 Fictionality Detection Demonstration Complete!")


async def main():
    """Main demonstration entry point"""
    demo = FictionalityDemo()
    
    try:
        await demo.initialize()
        await demo.run_demo()
    except KeyboardInterrupt:
        print("\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("🎭 Starting Fictionality Detection Demo...")
    asyncio.run(main())