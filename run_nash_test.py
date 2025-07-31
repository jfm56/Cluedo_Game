#!/usr/bin/env python
"""
Custom test runner for Nash AI player tests with timeout protection.
This script runs only specific tests with timeout safeguards.
"""
import sys
import unittest
import pytest
import signal

# Define a timeout handler to prevent infinite loops
def timeout_handler(signum, frame):
    print("TEST TIMEOUT - Execution took too long, possibly an infinite loop")
    sys.exit(1)

# Set a timeout for the entire script (30 seconds)
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)

def run_specific_test():
    """Run a specific test with additional timeout protection."""
    print("Running Nash AI test_init test...")
    # Run only the test_init test
    exit_code = pytest.main(['-xvs', 'tests/test_nash_ai_combined.py::TestNashAIPlayer::test_init'])
    return exit_code

if __name__ == "__main__":
    try:
        exit_code = run_specific_test()
        # Cancel the alarm once the test completes successfully
        signal.alarm(0)
        sys.exit(exit_code)
    except Exception as e:
        print(f"Error running test: {e}")
        sys.exit(1)
