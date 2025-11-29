#!/usr/bin/env python3
"""
Test script for speckit commands
"""

import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from src.speckit import speckit_analyse, speckit_checkist


def test_speckit_analyse():
    """Test the speckit analyse command"""
    print("Testing speckit.analyse command...")
    
    # Test with sample user feedback
    sample_feedback = "The application is running slowly and the interface is not very user-friendly. Please improve the performance and make it easier to use."
    
    print(f"Input feedback: {sample_feedback}")
    
    try:
        result = speckit_analyse(user_feedback=sample_feedback, analysis_type="comprehensive", output_format="json")
        print("✅ speckit.analyse executed successfully")
        print(f"Result keys: {list(result.keys())}")
        
        # Check for expected analysis components
        if "results" in result:
            if "feedback_analysis" in result["results"]:
                fb_analysis = result["results"]["feedback_analysis"]
                print(f"Feedback sentiment: {fb_analysis.get('sentiment', 'N/A')}")
                print(f"Feedback themes: {fb_analysis.get('themes', 'N/A')}")
                print(f"Actionable insights: {len(fb_analysis.get('actionable_insights', []))} items")
        
        print("\n" + "="*60 + "\n")
    except Exception as e:
        print(f"❌ Error testing speckit.analyse: {e}")
        import traceback
        traceback.print_exc()


def test_speckit_checkist():
    """Test the speckit checkist command"""
    print("Testing speckit.checkist command...")
    
    # Test with sample user feedback
    sample_feedback = "The application is running slowly and the interface is not very user-friendly."
    
    print(f"Input feedback: {sample_feedback}")
    
    try:
        result = speckit_checkist(user_feedback=sample_feedback, checklist_type="feedback", output_format="json")
        print("✅ speckit.checkist executed successfully")
        print(f"Result keys: {list(result.keys())}")
        
        # Check for checklist items
        checklist = result.get("checklist", [])
        print(f"Generated {len(checklist)} checklist items:")
        for i, item in enumerate(checklist[:3]):  # Show first 3 items
            print(f"  {i+1}. [{item.get('priority', 'N/A')}] {item['item']} (Category: {item.get('category', 'N/A')})")
        
        print("\n" + "="*60 + "\n")
    except Exception as e:
        print(f"❌ Error testing speckit.checkist: {e}")
        import traceback
        traceback.print_exc()


def test_speckit_without_feedback():
    """Test speckit commands without feedback to ensure they work with defaults"""
    print("Testing speckit commands without feedback (default behavior)...")
    
    try:
        # Test analyse without feedback
        result_analyse = speckit_analyse(analysis_type="codebase", output_format="json")
        print("✅ speckit.analyse (codebase analysis) executed successfully")
        
        # Test checkist without feedback
        result_checkist = speckit_checkist(checklist_type="development", output_format="json")
        print("✅ speckit.checkist (development checklist) executed successfully")
        
        checklist = result_checkist.get("checklist", [])
        print(f"Default checklist has {len(checklist)} items")
        
        print("\n" + "="*60 + "\n")
    except Exception as e:
        print(f"❌ Error testing speckit without feedback: {e}")
        import traceback
        traceback.print_exc()


def test_command_integration():
    """Test integration with launch.py command system"""
    print("Testing command integration...")
    
    try:
        # Import the command factory to verify it works
        from src.speckit.command_factory import SpeckitCommandFactory, SpeckitAnalyseCommand, SpeckitCheckistCommand
        import argparse
        
        # Create mock args
        args = argparse.Namespace()
        args.feedback = "Test feedback for integration"
        args.analysis_type = "comprehensive"
        args.checklist_type = "feedback"
        args.output_format = "json"
        
        # Test factory
        factory = SpeckitCommandFactory()
        analyse_cmd = factory.create_command('speckit.analyse', args)
        checkist_cmd = factory.create_command('speckit.checkist', args)
        
        if analyse_cmd and checkist_cmd:
            print("✅ Command factory creates commands successfully")
            print(f"✅ Analyse command type: {type(analyse_cmd)}")
            print(f"✅ Checkist command type: {type(checkist_cmd)}")
        else:
            print("❌ Command factory failed to create commands")
            
        print("\n" + "="*60 + "\n")
    except Exception as e:
        print(f"❌ Error testing command integration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("Running speckit command tests...\n")
    
    test_speckit_analyse()
    test_speckit_checkist()
    test_speckit_without_feedback()
    test_command_integration()
    
    print("All tests completed!")
