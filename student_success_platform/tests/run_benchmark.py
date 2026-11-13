#!/usr/bin/env python3
"""
Test Directory Shortcut for Student Risk Prediction Benchmark CLI
Allows running: python run_benchmark.py directly from student_success_platform/tests/
Author: Sumith U (SRN: R24EA807) | REVA University
"""

import sys
from pathlib import Path

# Automatically discover and add workspace root to sys.path
current = Path(__file__).resolve()
for parent in [current.parent, current.parent.parent, current.parent.parent.parent]:
    if (parent / "student_success_platform").exists():
        if str(parent) not in sys.path:
            sys.path.insert(0, str(parent))
        break

from student_success_platform.src.benchmark_cli import main

if __name__ == "__main__":
    main()

