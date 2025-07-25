import unittest
import subprocess
import sys
import os

class TestPlayCluedo(unittest.TestCase):
    def test_play_cluedo_import(self):
        # Ensure play_cluedo.py can be imported without error
        try:
            import play_cluedo
        except Exception as e:
            self.fail(f"Importing play_cluedo.py failed: {e}")

    def test_play_cluedo_runs(self):
        # Run play_cluedo.py with --help or no input, expect it to start and exit (simulate non-interactive)
        result = subprocess.run(
            [sys.executable, "play_cluedo.py"],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            input=b"0\n",  # Simulate selecting quit immediately
            capture_output=True,
            timeout=10
        )
        try:
            self.assertIn(b"Welcome to Cluedo", result.stdout)
            self.assertEqual(result.returncode, 0)
        except Exception as e:
            self.fail(f"play_cluedo.py CLI run check failed: {e}")

if __name__ == "__main__":
    unittest.main()
