"""
Configuration for pytest with Nash AI test mode support.
"""
import pytest
import sys
import time
from cluedo_game.ai import NashAIPlayer

def pytest_configure(config):
    """Enable test mode for Nash AI player during test runs."""
    print("\n=== pytest_configure: Starting test configuration ===")
    try:
        # Enable test mode for Nash AI to prevent hangs
        NashAIPlayer.set_test_mode(True)
        print("✓ Nash AI test mode enabled")
    except Exception as e:
        print(f"⚠ Error in pytest_configure: {e}", file=sys.stderr)
    print("=== pytest_configure: Test configuration complete ===\n")

def pytest_unconfigure(config):
    """Disable test mode after tests complete."""
    print("\n=== pytest_unconfigure: Cleaning up test configuration ===")
    try:
        # Disable test mode when tests are done
        NashAIPlayer.set_test_mode(False)
        print("✓ Nash AI test mode disabled")
    except Exception as e:
        print(f"⚠ Error in pytest_unconfigure: {e}", file=sys.stderr)
    print("=== pytest_unconfigure: Cleanup complete ===\n")

# Add a timeout to prevent infinite test hangs
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Set a timeout for each test to prevent hanging."""
    # Set a 10-second timeout per test
    item._test_timeout = time.time() + 10

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    """Check for test timeouts during execution."""
    start_time = time.time()
    yield
    elapsed = time.time() - start_time
    if hasattr(item, '_test_timeout') and time.time() > item._test_timeout:
        pytest.fail("Test timed out after 10 seconds")
