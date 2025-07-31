#!/bin/bash
pytest tests/test_board_and_movement.py::TestMovement::test_get_optimal_path_adjacent tests/test_board_and_movement.py::TestMovement::test_get_optimal_path_multiple_steps tests/test_board_and_movement.py::TestMovement::test_get_optimal_path_unreachable tests/test_board_and_movement.py::TestMovement::test_get_optimal_path_limited_steps -vv
