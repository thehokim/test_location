import pytest
import requests
from datetime import datetime
import json


class TestStudentCountByRegion:
    """Test to generate student count report for all regions"""
    
    BASE_URL = "https://api.qa.2plus6.uz/api/v1/statistics/agency"
    
    ALL_REGIONS = {
        "Tashkent": 1,
        "Jizzakh": 2,
        "Sirdaryo": 3,
        "Bukhara": 4,
        "Fergana": 5,
        "Navoiy": 6,
        "Karakalpakstan": 8,
        "Namangan": 9,
        "Samarqand": 10,
        "Tashkent Region": 12,
        "Surxondaryo": 170,
        "Andijon": 347,
        "Xorazm": 348,
        "Qashqadaryo": 349
    }
    
    @pytest.fixture(scope="class")
    def auth_session(self):
        """Get authentication session"""
        login_url = "https://api.qa.2plus6.uz/api/v1/agency/auth/login/"
        
        credentials = {
            "username": "yiaadmin@2plus6.uz",
            "password": "_b#1mv5^X2T0"
        }
        
        response = requests.post(
            login_url,
            json=credentials,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code != 200:
            pytest.fail(f"Login failed: {response.status_code}")
        
        session = requests.Session()
        session.cookies.update(response.cookies)
        session.headers.update({
            "accept": "application/json",
            "Content-Type": "application/json"
        })
        
        return session
    
    @pytest.fixture
    def session(self, auth_session):
        return auth_session
    
    def test_student_count_all_regions(self, session):
        """
        Get student count for ALL regions
        Generates a detailed report
        """
        url = f"{self.BASE_URL}/student-statistic/age/city/"
        
        print("\n" + "="*80)
        print("STUDENT COUNT BY REGION REPORT")
        print("="*80)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        results = []
        total_students = 0
        
        for region_name, region_id in sorted(self.ALL_REGIONS.items()):
            params = {"city": region_id}
            response = session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                student_count = self._extract_student_count(data)
                
                results.append({
                    "region": region_name,
                    "region_id": region_id,
                    "student_count": student_count,
                    "status": "OK"
                })
                
                if student_count is not None:
                    total_students += student_count
                
                print(f"\n{region_name:.<30} (ID: {region_id:>3}) | Students: {student_count if student_count is not None else 'N/A':>10} | ✅")
            else:
                results.append({
                    "region": region_name,
                    "region_id": region_id,
                    "student_count": None,
                    "status": f" Error {response.status_code}"
                })
                print(f"\n{region_name:.<30} (ID: {region_id:>3}) |  Error {response.status_code}")
        
        print("\n" + "="*80)
        print(f"TOTAL STUDENTS ACROSS ALL REGIONS: {total_students}")
        print("="*80)
        
        self._save_report(results, total_students)
        
        assert len([r for r in results if r["status"] == "OK"]) > 0, "No regions returned data"
    
    def test_student_count_by_region_detailed(self, session):

        url = f"{self.BASE_URL}/student-statistic/age/city/"
        
        print("\n" + "="*80)
        print("DETAILED STUDENT STATISTICS BY REGION")
        print("="*80)
        
        for region_name, region_id in sorted(self.ALL_REGIONS.items()):
            params = {"city": region_id}
            response = session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"\n {region_name} (ID: {region_id})")
                print("-" * 60)
                
                if isinstance(data, dict):
                    if "result" in data:
                        print(f"   Data: {json.dumps(data['result'], indent=2, ensure_ascii=False)[:500]}...")
                    elif "results" in data:
                        print(f"   Count: {len(data['results'])} records")
                    else:
                        print(f"   Response keys: {list(data.keys())}")
                elif isinstance(data, list):
                    print(f"   Records: {len(data)} items")
                else:
                    print(f"   Response type: {type(data)}")
        
        print("\n" + "="*80)
    
    def test_learning_centers_by_region(self, session):
        """
        Count learning centers in each region
        """
        url = f"{self.BASE_URL}/learning-center-statistic/city/"
        
        print("\n" + "="*80)
        print("LEARNING CENTERS BY REGION")
        print("="*80)
        
        results = []
        total_centers = 0
        
        for region_name, region_id in sorted(self.ALL_REGIONS.items()):
            params = {"city": region_id}
            response = session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                center_count = self._extract_center_count(data)
                
                if center_count is not None:
                    total_centers += center_count
                
                results.append({
                    "region": region_name,
                    "centers": center_count
                })
                
                print(f"{region_name:.<30} | Centers: {center_count if center_count is not None else 'N/A':>10}")
        
        print("-" * 80)
        print(f"{'TOTAL':.<30} | Centers: {total_centers:>10}")
        print("="*80)
        
        assert total_centers >= 0
    
    def test_compare_regions(self, session):

        url = f"{self.BASE_URL}/student-statistic/age/city/"
        
        print("\n" + "="*80)
        print("REGIONAL COMPARISON")
        print("="*80)
        
        region_data = []
        
        for region_name, region_id in self.ALL_REGIONS.items():
            params = {"city": region_id}
            response = session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                student_count = self._extract_student_count(data)
                
                if student_count is not None:
                    region_data.append({
                        "name": region_name,
                        "id": region_id,
                        "students": student_count
                    })
        
        region_data.sort(key=lambda x: x["students"], reverse=True)
        
        print("\n TOP 5 REGIONS BY STUDENT COUNT:")
        print("-" * 80)
        for i, region in enumerate(region_data[:5], 1):
            print(f"{i}. {region['name']:.<30} {region['students']:>10,} students")
        
        print("\n📉 BOTTOM 5 REGIONS BY STUDENT COUNT:")
        print("-" * 80)
        for i, region in enumerate(region_data[-5:], 1):
            print(f"{i}. {region['name']:.<30} {region['students']:>10,} students")
        
        print("\n" + "="*80)
    
    def _extract_student_count(self, data):

        if isinstance(data, dict):
            if "total_students" in data:
                return data["total_students"]
            elif "total" in data:
                return data["total"]
            elif "count" in data:
                return data["count"]
            elif "student_count" in data:
                return data["student_count"]
            elif "result" in data:
                if isinstance(data["result"], dict):
                    return self._extract_student_count(data["result"])
                elif isinstance(data["result"], list):
                    return len(data["result"])
            elif "results" in data:
                return len(data["results"])
            
            if "age_groups" in data:
                total = sum(group.get("count", 0) for group in data["age_groups"])
                if total > 0:
                    return total
        
        elif isinstance(data, list):
            return len(data)
        
        return None
    
    def _extract_center_count(self, data):
        """Extract learning center count from response"""
        if isinstance(data, dict):
            if "total_centers" in data:
                return data["total_centers"]
            elif "total" in data:
                return data["total"]
            elif "count" in data:
                return data["count"]
            elif "result" in data:
                if isinstance(data["result"], list):
                    return len(data["result"])
            elif "results" in data:
                return len(data["results"])
        elif isinstance(data, list):
            return len(data)
        
        return None
    
    def _save_report(self, results, total):
        """Save report to JSON and text files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        json_filename = f"student_count_report_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump({
                "generated_at": datetime.now().isoformat(),
                "total_students": total,
                "regions": results
            }, f, indent=2, ensure_ascii=False)
        
        txt_filename = f"student_count_report_{timestamp}.txt"
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("STUDENT COUNT BY REGION REPORT\n")
            f.write("="*80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            for r in results:
                count = r["student_count"] if r["student_count"] is not None else "N/A"
                f.write(f"{r['region']:.<30} (ID: {r['region_id']:>3}) | Students: {count:>10} | {r['status']}\n")
            
            f.write("\n" + "="*80 + "\n")
            f.write(f"TOTAL STUDENTS: {total}\n")
            f.write("="*80 + "\n")
        
        print(f"\n Reports saved:")
        print(f"   - {json_filename}")
        print(f"   - {txt_filename}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])