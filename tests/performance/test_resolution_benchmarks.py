"""
Performance tests for resolution workflows

Benchmarking tests for specification generation, strategy development,
and constitutional validation performance.
"""

import pytest
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import the modules to test
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from specification.template_generator import SpecificationTemplateGenerator, SpecificationPhase
from strategy.multi_phase_generator import MultiPhaseStrategyGenerator
from resolution.constitutional_engine import ConstitutionalEngine


class TestResolutionBenchmarks:
    """Performance benchmark test suite"""
    
    @pytest.fixture
    async def benchmark_components(self):
        """Create components for performance testing"""
        template_generator = SpecificationTemplateGenerator()
        strategy_generator = MultiPhaseStrategyGenerator()
        constitutional_engine = ConstitutionalEngine()
        
        await template_generator.initialize()
        await constitutional_engine.initialize()
        
        return {
            "template_generator": template_generator,
            "strategy_generator": strategy_generator,
            "constitutional_engine": constitutional_engine
        }
    
    @pytest.fixture
    def performance_thresholds(self):
        """Define performance thresholds for benchmarking"""
        return {
            "template_generation": 5.0,  # 5 seconds maximum
            "strategy_generation": 3.0,  # 3 seconds maximum
            "constitutional_validation": 2.0,  # 2 seconds maximum
            "complete_workflow": 15.0,  # 15 seconds maximum
            "constitutional_compliance": 30.0,  # 30 seconds maximum for constitutional validation
        }
    
    @pytest.fixture
    def sample_workload_data(self):
        """Create sample workload data for performance testing"""
        return {
            "small_conflict": type('MockConflict', (), {
                'conflict_type': 'content',
                'file_paths': ['src/service.py'],
                'complexity_score': 3,
                'estimated_resolution_time': 15
            })(),
            
            "medium_conflict": type('MockConflict', (), {
                'conflict_type': 'content',
                'file_paths': [f'src/module_{i}.py' for i in range(5)],
                'complexity_score': 6,
                'estimated_resolution_time': 30
            })(),
            
            "large_conflict": type('MockConflict', (), {
                'conflict_type': 'architectural',
                'file_paths': [f'src/module_{i}.py' for i in range(15)],
                'complexity_score': 9,
                'estimated_resolution_time': 60
            })()
        }
    
    @pytest.fixture
    def sample_contexts(self):
        """Create sample contexts for different scenarios"""
        return {
            "simple_context": {
                "complexity_score": 3,
                "urgency_level": "low"
            },
            
            "standard_context": {
                "complexity_score": 6,
                "urgency_level": "medium",
                "feature_preservation_required": True
            },
            
            "complex_context": {
                "complexity_score": 9,
                "urgency_level": "high",
                "feature_preservation_required": True,
                "architectural_change": True
            }
        }

    async def test_template_generation_performance(
        self, benchmark_components, sample_workload_data, performance_thresholds
    ):
        """Benchmark template generation performance"""
        template_generator = benchmark_components["template_generator"]
        
        project_context = {
            "organization": {"name": "Test Org"},
            "technology_stack": {"language": "Python", "framework": "FastAPI"},
            "testing_phase": "improved"
        }
        
        team_context = {
            "experience_level": "intermediate",
            "preferences": {"risk_tolerance": "moderate"}
        }
        
        # Test different workload sizes
        workloads = [
            ("small", sample_workload_data["small_conflict"]),
            ("medium", sample_workload_data["medium_conflict"]),
            ("large", sample_workload_data["large_conflict"])
        ]
        
        performance_results = {}
        
        for size, conflict_data in workloads:
            times = []
            
            # Run multiple iterations for statistical analysis
            for iteration in range(3):
                start_time = time.time()
                
                specification = await template_generator.generate_specification_template(
                    conflict_data,
                    project_context,
                    team_context,
                    SpecificationPhase.IMPROVED
                )
                
                end_time = time.time()
                iteration_time = end_time - start_time
                times.append(iteration_time)
                
                assert specification is not None
            
            # Calculate statistics
            avg_time = statistics.mean(times)
            max_time = max(times)
            min_time = min(times)
            
            performance_results[size] = {
                "average_time": avg_time,
                "max_time": max_time,
                "min_time": min_time,
                "times": times
            }
            
            # Check against thresholds
            assert avg_time <= performance_thresholds["template_generation"]
        
        # Log performance results
        print("\nTemplate Generation Performance:")
        for size, results in performance_results.items():
            print(f"{size}: avg={results['average_time']:.2f}s, max={results['max_time']:.2f}s")

    async def test_strategy_generation_performance(
        self, benchmark_components, sample_workload_data, performance_thresholds
    ):
        """Benchmark strategy generation performance"""
        strategy_generator = benchmark_components["strategy_generator"]
        
        contexts = [
            ("simple", {"complexity_score": 3, "urgency_level": "low"}),
            ("standard", {"complexity_score": 6, "urgency_level": "medium"}),
            ("complex", {"complexity_score": 9, "urgency_level": "high"})
        ]
        
        performance_results = {}
        
        for context_name, context in contexts:
            times = []
            
            # Run multiple iterations
            for iteration in range(3):
                start_time = time.time()
                
                strategies = strategy_generator.generate_multi_phase_strategies(
                    sample_workload_data["medium_conflict"],
                    context,
                    "medium",
                    "normal"
                )
                
                end_time = time.time()
                iteration_time = end_time - start_time
                times.append(iteration_time)
                
                assert len(strategies) > 0
            
            # Calculate statistics
            avg_time = statistics.mean(times)
            max_time = max(times)
            
            performance_results[context_name] = {
                "average_time": avg_time,
                "max_time": max_time,
                "strategies_generated": len(strategies)
            }
            
            # Check against thresholds
            assert avg_time <= performance_thresholds["strategy_generation"]
        
        print("\nStrategy Generation Performance:")
        for context, results in performance_results.items():
            print(f"{context}: avg={results['average_time']:.2f}s, strategies={results['strategies_generated']}")

    async def test_constitutional_validation_performance(
        self, benchmark_components, sample_workload_data, performance_thresholds
    ):
        """Benchmark constitutional validation performance"""
        constitutional_engine = benchmark_components["constitutional_engine"]
        
        # Create test templates of different sizes
        small_template = {
            "template_content": {"overview": {"description": "Small template"}},
            "constitutional_validation": {"compliance_score": 0.8}
        }
        
        large_template = {
            "template_content": {
                f"section_{i}": {
                    f"subsection_{j}": f"content_{i}_{j}" 
                    for j in range(50)
                }
                for i in range(20)
            },
            "constitutional_validation": {"compliance_score": 0.8}
        }
        
        templates = [
            ("small", small_template),
            ("large", large_template)
        ]
        
        performance_results = {}
        
        for size, template in templates:
            times = []
            
            # Run multiple iterations
            for iteration in range(3):
                start_time = time.time()
                
                validation_result = await constitutional_engine.validate_template(template)
                
                end_time = time.time()
                iteration_time = end_time - start_time
                times.append(iteration_time)
                
                assert validation_result is not None
            
            # Calculate statistics
            avg_time = statistics.mean(times)
            max_time = max(times)
            
            performance_results[size] = {
                "average_time": avg_time,
                "max_time": max_time
            }
            
            # Check against thresholds
            assert avg_time <= performance_thresholds["constitutional_validation"]
        
        print("\nConstitutional Validation Performance:")
        for size, results in performance_results.items():
            print(f"{size}: avg={results['average_time']:.2f}s")

    async def test_concurrent_workflow_performance(
        self, benchmark_components, sample_workload_data, performance_thresholds
    ):
        """Test concurrent workflow execution performance"""
        template_generator = benchmark_components["template_generator"]
        
        project_context = {
            "organization": {"name": "Test Org"},
            "technology_stack": {"language": "Python", "framework": "FastAPI"},
            "testing_phase": "improved"
        }
        
        team_context = {
            "experience_level": "intermediate"
        }
        
        # Number of concurrent workflows
        num_concurrent = 5
        
        start_time = time.time()
        
        # Execute concurrent workflows
        with ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            futures = []
            
            for i in range(num_concurrent):
                future = executor.submit(
                    self._run_template_generation_sync,
                    template_generator,
                    sample_workload_data["medium_conflict"],
                    project_context,
                    team_context
                )
                futures.append(future)
            
            # Collect results
            results = []
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    pytest.fail(f"Concurrent execution failed: {e}")
        
        total_time = time.time() - start_time
        
        # Verify all workflows completed
        assert len(results) == num_concurrent
        
        # Check total time is reasonable for concurrent execution
        assert total_time <= performance_thresholds["complete_workflow"]
        
        print(f"\nConcurrent Workflow Performance ({num_concurrent} concurrent):")
        print(f"Total time: {total_time:.2f}s")

    def _run_template_generation_sync(self, template_generator, conflict_data, project_context, team_context):
        """Synchronous wrapper for async template generation"""
        import asyncio
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                template_generator.generate_specification_template(
                    conflict_data,
                    project_context,
                    team_context,
                    SpecificationPhase.IMPROVED
                )
            )
            return result
        finally:
            loop.close()

    async def test_memory_usage_benchmark(self, benchmark_components, sample_workload_data):
        """Test memory usage during workflow execution"""
        template_generator = benchmark_components["template_generator"]
        
        # Measure memory usage (simplified - in real implementation would use memory profiling)
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Generate multiple specifications
        for i in range(10):
            specification = await template_generator.generate_specification_template(
                sample_workload_data["medium_conflict"],
                {"organization": {"name": "Test"}},
                {"experience_level": "intermediate"},
                SpecificationPhase.IMPROVED
            )
            
            assert specification is not None
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB for 10 specifications)
        memory_increase_mb = memory_increase / (1024 * 1024)
        assert memory_increase_mb < 100  # Less than 100MB increase
        
        print(f"\nMemory Usage Benchmark:")
        print(f"Memory increase for 10 specifications: {memory_increase_mb:.2f}MB")

    async def test_constitutional_performance_with_large_rules(
        self, benchmark_components, performance_thresholds
    ):
        """Test constitutional validation performance with large rule sets"""
        constitutional_engine = benchmark_components["constitutional_engine"]
        
        # Add many constitutional rules to test performance
        from resolution.constitutional_engine import ConstitutionalRule
        
        large_rule_set = []
        for i in range(100):  # 100 rules
            rule = ConstitutionalRule(
                id=f"large_rule_{i}",
                name=f"Large Rule {i}",
                description=f"Test rule {i} for performance testing",
                category="performance_test",
                severity="minor",
                validation_function=lambda x: True,
                remediation_suggestion="Standard remediation"
            )
            large_rule_set.append(rule)
        
        # Register large rule set
        registration_result = await constitutional_engine.register_constitutional_rules(large_rule_set)
        assert registration_result.success
        
        # Test validation performance with large rule set
        test_template = {
            "template_content": {
                "overview": {"description": "Performance test template"},
                "constitutional_compliance": {"compliance_score": 0.8}
            }
        }
        
        start_time = time.time()
        
        validation_result = await constitutional_engine.validate_template(test_template)
        
        end_time = time.time()
        validation_time = end_time - start_time
        
        # Should still perform within reasonable time even with 100 rules
        assert validation_time <= performance_thresholds["constitutional_compliance"]
        
        print(f"\nLarge Rule Set Performance:")
        print(f"Validation with 100 rules: {validation_time:.2f}s")
        print(f"Rules processed: {len(constitutional_engine.rule_cache)}")

    async def test_workflow_scalability_performance(
        self, benchmark_components, performance_thresholds
    ):
        """Test workflow scalability with increasing complexity"""
        template_generator = benchmark_components["template_generator"]
        
        # Test with increasing complexity levels
        complexity_levels = [1, 3, 5, 7, 9]
        performance_data = []
        
        for complexity in complexity_levels:
            # Create conflict data with increasing complexity
            conflict_data = type('MockConflict', (), {
                'conflict_type': 'content',
                'file_paths': [f'src/complex_module_{i}.py' for i in range(complexity)],
                'complexity_score': complexity,
                'estimated_resolution_time': complexity * 10
            })()
            
            times = []
            
            # Run multiple iterations
            for iteration in range(3):
                start_time = time.time()
                
                specification = await template_generator.generate_specification_template(
                    conflict_data,
                    {"organization": {"name": "Test"}},
                    {"experience_level": "intermediate"},
                    SpecificationPhase.IMPROVED
                )
                
                end_time = time.time()
                times.append(end_time - start_time)
                
                assert specification is not None
            
            avg_time = statistics.mean(times)
            performance_data.append((complexity, avg_time))
        
        # Verify scalability - time should not grow exponentially
        for i in range(1, len(performance_data)):
            prev_complexity, prev_time = performance_data[i-1]
            curr_complexity, curr_time = performance_data[i]
            
            # Time increase should be reasonable (not exponential)
            time_ratio = curr_time / prev_time if prev_time > 0 else 1
            complexity_ratio = curr_complexity / prev_complexity
            
            # Allow for some scaling, but not exponential growth
            assert time_ratio <= complexity_ratio * 2  # At most 2x the complexity ratio
        
        print("\nScalability Performance:")
        for complexity, avg_time in performance_data:
            print(f"Complexity {complexity}: {avg_time:.2f}s")

    async def test_performance_regression_detection(self, benchmark_components, sample_workload_data):
        """Test ability to detect performance regressions"""
        template_generator = benchmark_components["template_generator"]
        
        # Establish baseline performance
        baseline_times = []
        
        for iteration in range(5):
            start_time = time.time()
            
            specification = await template_generator.generate_specification_template(
                sample_workload_data["medium_conflict"],
                {"organization": {"name": "Test"}},
                {"experience_level": "intermediate"},
                SpecificationPhase.IMPROVED
            )
            
            end_time = time.time()
            baseline_times.append(end_time - start_time)
            
            assert specification is not None
        
        baseline_avg = statistics.mean(baseline_times)
        baseline_std = statistics.stdev(baseline_times) if len(baseline_times) > 1 else 0
        
        # Test subsequent runs
        regression_times = []
        
        for iteration in range(5):
            start_time = time.time()
            
            specification = await template_generator.generate_specification_template(
                sample_workload_data["medium_conflict"],
                {"organization": {"name": "Test"}},
                {"experience_level": "intermediate"},
                SpecificationPhase.IMPROVED
            )
            
            end_time = time.time()
            regression_times.append(end_time - start_time)
            
            assert specification is not None
        
        regression_avg = statistics.mean(regression_times)
        
        # Check for significant regression (more than 2 standard deviations)
        regression_threshold = baseline_avg + (2 * baseline_std) if baseline_std > 0 else baseline_avg * 1.5
        
        assert regression_avg <= regression_threshold
        
        print(f"\nPerformance Regression Detection:")
        print(f"Baseline: {baseline_avg:.2f}s ± {baseline_std:.2f}s")
        print(f"Current: {regression_avg:.2f}s")
        print(f"Threshold: {regression_threshold:.2f}s")
        print(f"Regression detected: {regression_avg > regression_threshold}")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--benchmark-only"])