import subprocess
import sys

def main():
    print("\n" + "="*70)
    print("AGENCY STATISTICS API TESTS")
    print("="*70)
    print("\nTesting all statistics endpoints:")
    print("  - Learning Center Statistics (city/district/neighbour)")
    print("  - Student Age Statistics (city/district/neighbourhood)")
    print("  - Application Cards")
    print("\nParameters tested: city, district, languages, start_date, end_date\n")
    print("="*70 + "\n")
    
    # Run statistics tests
    cmd = [
        "pytest",
        "test_agency_statistics_api.py",
        "-v",
        "--tb=short"
    ]
    
    result = subprocess.run(cmd)
    
    print("\n" + "="*70)
    print("STATISTICS TESTS COMPLETED")
    print("="*70)
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())