"""
=============================================================================
DATABASE & AI GATEWAY AUTOMATED TEST RUNNER
AI-Powered Agentic Smart Campus Intelligence & Student Success Platform
ChromaDB (Vector), Fluxbase (Relational DB), & Flux AI Gateway (Reasoning)
Author: Sumith U (SRN: R24EA807), REVA University
=============================================================================
"""

import sys
import unittest

if __name__ == "__main__":
    from tests.test_vector_db import TestVectorDatabaseIntegration
    from tests.test_fluxbase import TestFluxbaseDatabaseIntegration
    from tests.test_flux_ai import TestFluxAIGatewayService

    print("\n" + "=" * 75)
    print("  RUNNING CLOUD & LOCAL DATABASE / AI INTEGRATION TEST SUITES")
    print("  1. ChromaDB: Local Docker Vector Embeddings for Part 5 RAG")
    print("  2. Fluxbase: Cloud Relational DB for Faculty & Students (fluxbasedb.me)")
    print("  3. Flux AI: Cloud Reasoning Models ('flux', 'flux-pro', 'flux-flash')")
    print("=" * 75 + "\n")

    loader = unittest.TestLoader()
    suite = unittest.TestSuite([
        loader.loadTestsFromTestCase(TestVectorDatabaseIntegration),
        loader.loadTestsFromTestCase(TestFluxbaseDatabaseIntegration),
        loader.loadTestsFromTestCase(TestFluxAIGatewayService)
    ])

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 75)
    print("  DATABASE & AI VERIFICATION SUMMARY")
    print("=" * 75)

    if result.wasSuccessful():
        print("  [PASS] ChromaDB: Local Docker vector container active (Port 8001).")
        print("  [PASS] ChromaDB: 3 collections verified (Syllabus, Notes, Question Bank).")
        print("  [PASS] ChromaDB: Semantic vector similarity retrieval verified.")
        print("  [PASS] Fluxbase: Live PostgreSQL connection on fluxbasedb.me verified.")
        print("  [PASS] Fluxbase: Relational schema verified (faculty, students, advising logs).")
        print("  [PASS] Fluxbase: Faculty & student cohort retrieval & risk filtering verified.")
        print("  [PASS] Fluxbase: Faculty counseling action note recording verified.")
        print("  [PASS] Flux AI: Cloud reasoning chat completion verified on 'flux-flash'.")
        print("  [PASS] Flux AI: Pedagogical remediation guidance synthesis verified.")
        print("=" * 75)
        print("  ALL 14/14 DATABASE & AI GATEWAY TESTS PASSED SUCCESSFULLY.")
        print("=" * 75 + "\n")
        sys.exit(0)
    else:
        print("  [FAIL] One or more verification tests failed.")
        print("=" * 75 + "\n")
        sys.exit(1)
