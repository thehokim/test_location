import subprocess
import sys

def main():
    print("\n" + "="*70)
    print("TIME PARAMETER TESTS - Detailed Report")
    print("="*70)
    print("\nTesting time_start and time_end filtering parameters...")
    print("Note: These parameters filter results but are NOT in the response body\n")
    
    # Run only time-related tests with verbose output
    cmd = [
        "pytest",
        "test_location_api.py",
        "-v",
        "-k", "time",  # Only run tests with 'time' in the name
        "--tb=short",
        "--html=reports/time_report.html",
        "-s"  # Show print statements
    ]
    
    print("Command:", " ".join(cmd))
    print("="*70 + "\n")
    
    result = subprocess.run(cmd)
    
    print("\n" + "="*70)
    print("TIME TESTS COMPLETED")
    print("="*70)
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())