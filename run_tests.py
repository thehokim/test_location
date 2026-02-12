import sys
import subprocess
from datetime import datetime


class TestRunner:
    """Test runner with predefined test configurations"""
    
    def __init__(self):
        self.test_file = "test_location_api.py"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def run_command(self, cmd):
        """Execute pytest command"""
        print(f"\n{'='*60}")
        print(f"Running: {' '.join(cmd)}")
        print(f"{'='*60}\n")
        
        result = subprocess.run(cmd)
        return result.returncode
    
    def all_tests(self):
        """Run all tests"""
        cmd = ["pytest", self.test_file, "-v"]
        return self.run_command(cmd)
    
    def smoke_tests(self):
        """Run quick smoke tests"""
        cmd = [
            "pytest", self.test_file,
            "-v",
            "-k", "test_city_valid_tashkent or test_price_range_valid or test_search_valid_term",
            "--tb=line"
        ]
        return self.run_command(cmd)
    
    def city_tests(self):
        """Run all city parameter tests"""
        cmd = ["pytest", self.test_file, "-v", "-k", "city"]
        return self.run_command(cmd)
    
    def price_tests(self):
        """Run all price parameter tests"""
        cmd = ["pytest", self.test_file, "-v", "-k", "price"]
        return self.run_command(cmd)
    
    def search_tests(self):
        """Run all search parameter tests"""
        cmd = ["pytest", self.test_file, "-v", "-k", "search"]
        return self.run_command(cmd)
    
    def time_tests(self):
        """Run all time parameter tests"""
        cmd = ["pytest", self.test_file, "-v", "-k", "time"]
        return self.run_command(cmd)
    
    def pagination_tests(self):
        """Run all pagination tests"""
        cmd = ["pytest", self.test_file, "-v", "-k", "page"]
        return self.run_command(cmd)
    
    def auth_tests(self):
        """Run authentication tests"""
        cmd = ["pytest", self.test_file, "-v", "-k", "auth"]
        return self.run_command(cmd)
    
    def performance_tests(self):
        """Run performance tests"""
        cmd = ["pytest", self.test_file, "-v", "::TestLocationAPIPerformance"]
        return self.run_command(cmd)
    
    def combined_tests(self):
        """Run tests with multiple parameters"""
        cmd = ["pytest", self.test_file, "-v", "-k", "combined"]
        return self.run_command(cmd)
    
    def with_report(self):
        """Run all tests and generate HTML report"""
        report_name = f"report_{self.timestamp}.html"
        
        # Check if pytest-html is installed
        try:
            import pytest_html
            cmd = [
                "pytest", self.test_file,
                "-v",
                "--html=" + report_name,
                "--self-contained-html"
            ]
        except ImportError:
            print("\n⚠️  pytest-html not installed. Installing now...")
            install_cmd = ["pip", "install", "pytest-html"]
            subprocess.run(install_cmd)
            print("✅ pytest-html installed. Running tests...\n")
            cmd = [
                "pytest", self.test_file,
                "-v",
                "--html=" + report_name,
                "--self-contained-html"
            ]
        
        return self.run_command(cmd)
    
    def parallel(self):
        """Run tests in parallel (requires pytest-xdist)"""
        try:
            import xdist
            cmd = [
                "pytest", self.test_file,
                "-v",
                "-n", "auto"
            ]
        except ImportError:
            print("\n⚠️  pytest-xdist not installed.")
            print("Install it with: pip install pytest-xdist")
            print("Running tests normally instead...\n")
            return self.all_tests()
        
        return self.run_command(cmd)
    
    def with_summary_report(self):
        """Run tests and save detailed text summary"""
        report_name = f"test_summary_{self.timestamp}.txt"
        cmd = [
            "pytest", self.test_file,
            "-v",
            "--tb=short",
            f"--result-log={report_name}"
        ]
        print(f"\n📄 Summary will be saved to: {report_name}")
        return self.run_command(cmd)
    
    def failed_first(self):
        """Run previously failed tests first"""
        cmd = [
            "pytest", self.test_file,
            "-v",
            "--failed-first",
            "--stepwise"
        ]
        return self.run_command(cmd)
    
    def verbose_failures(self):
        """Run tests with detailed failure information"""
        cmd = [
            "pytest", self.test_file,
            "-vv",
            "--tb=long",
            "--showlocals"
        ]
        return self.run_command(cmd)


def print_menu():
    """Display menu options"""
    print("\n" + "="*60)
    print("Location API Test Runner")
    print("="*60)
    print("\n📋 Available Test Suites:\n")
    print("  1.  Run ALL tests")
    print("  2.  Smoke tests (quick validation)")
    print("  3.  City parameter tests")
    print("  4.  Price parameter tests")
    print("  5.  Search parameter tests")
    print("  6.  Time parameter tests")
    print("  7.  Pagination tests")
    print("  8.  Authentication tests")
    print("  9.  Performance tests")
    print("  10. Combined parameter tests")
    print("\n🛠️  Special Modes:\n")
    print("  11. Run all tests + Generate HTML report")
    print("  12. Run tests in parallel (faster)")
    print("  13. Run failed tests first")
    print("  14. Run with verbose failure details")
    print("\n  0.  Exit")
    print("\n" + "="*60)


def main():
    """Main test runner"""
    runner = TestRunner()
    
    if len(sys.argv) > 1:
        option = sys.argv[1]
        
        options = {
            "all": runner.all_tests,
            "smoke": runner.smoke_tests,
            "city": runner.city_tests,
            "price": runner.price_tests,
            "search": runner.search_tests,
            "time": runner.time_tests,
            "pagination": runner.pagination_tests,
            "auth": runner.auth_tests,
            "performance": runner.performance_tests,
            "combined": runner.combined_tests,
            "report": runner.with_report,
            "parallel": runner.parallel,
            "failed": runner.failed_first,
            "verbose": runner.verbose_failures,
        }
        
        if option in options:
            return options[option]()
        else:
            print(f"Unknown option: {option}")
            print("\nAvailable options:")
            for key in options.keys():
                print(f"  - {key}")
            return 1
    
    while True:
        print_menu()
        choice = input("\nSelect option (0-14): ").strip()
        
        if choice == "0":
            print("\n👋 Goodbye!")
            break
        elif choice == "1":
            runner.all_tests()
        elif choice == "2":
            runner.smoke_tests()
        elif choice == "3":
            runner.city_tests()
        elif choice == "4":
            runner.price_tests()
        elif choice == "5":
            runner.search_tests()
        elif choice == "6":
            runner.time_tests()
        elif choice == "7":
            runner.pagination_tests()
        elif choice == "8":
            runner.auth_tests()
        elif choice == "9":
            runner.performance_tests()
        elif choice == "10":
            runner.combined_tests()
        elif choice == "11":
            runner.with_report()
        elif choice == "12":
            runner.parallel()
        elif choice == "13":
            runner.failed_first()
        elif choice == "14":
            runner.verbose_failures()
        else:
            print("\n❌ Invalid choice. Please select 0-14.")
        
        input("\n\nPress Enter to continue...")


if __name__ == "__main__":
    sys.exit(main())