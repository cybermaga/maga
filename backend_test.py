#!/usr/bin/env python3
"""
Backend API Testing for EU AI Act Compliance Repository Scanning
Tests all repository scanning endpoints and functionality
"""

import requests
import sys
import os
from datetime import datetime
import json

class RepoScanAPITester:
    def __init__(self, base_url="https://aicomply-1.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.scan_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, files=None):
        """Run a single API test"""
        url = f"{self.api_base}/{endpoint}"
        headers = {}
        
        # Don't set Content-Type for multipart/form-data (files)
        if not files:
            headers['Content-Type'] = 'application/json'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=30)
            elif method == 'POST':
                if files:
                    response = requests.post(url, data=data, files=files, timeout=120)
                else:
                    response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                
                # Try to parse JSON response
                try:
                    response_data = response.json()
                    if isinstance(response_data, dict):
                        # Print key information
                        if 'id' in response_data:
                            print(f"   ID: {response_data['id']}")
                        if 'system_name' in response_data:
                            print(f"   System: {response_data['system_name']}")
                        if 'coverage_stats' in response_data:
                            stats = response_data['coverage_stats']
                            print(f"   Coverage: {stats.get('coverage_percentage', 0)}%")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   Error: {error_detail}")
                except:
                    print(f"   Response: {response.text[:200]}")
                return False, {}

        except requests.exceptions.Timeout:
            print(f"❌ Failed - Request timeout")
            return False, {}
        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test API health check"""
        success, response = self.run_test(
            "API Health Check",
            "GET",
            "health",
            200
        )
        return success

    def test_get_controls(self):
        """Test getting compliance controls"""
        success, response = self.run_test(
            "Get Compliance Controls",
            "GET", 
            "controls",
            200
        )
        if success and 'controls' in response:
            print(f"   Found {len(response['controls'])} controls")
        return success

    def test_upload_repository(self):
        """Test repository upload and scan"""
        # Check if demo file exists
        demo_file_path = "/tmp/demo-ai-project.zip"
        if not os.path.exists(demo_file_path):
            print(f"❌ Demo file not found at {demo_file_path}")
            return False

        # Prepare file upload
        with open(demo_file_path, 'rb') as f:
            files = {'zip_file': ('demo-ai-project.zip', f, 'application/zip')}
            data = {'system_name': 'Test AI System via Backend API'}
            
            success, response = self.run_test(
                "Upload Repository and Scan",
                "POST",
                "compliance/scan/repo",
                200,
                data=data,
                files=files
            )
            
            if success and 'id' in response:
                self.scan_id = response['id']
                print(f"   Scan ID saved: {self.scan_id}")
            
            return success

    def test_get_scan_result(self):
        """Test getting scan results"""
        if not self.scan_id:
            print("❌ No scan ID available - skipping test")
            return False
            
        success, response = self.run_test(
            "Get Scan Results",
            "GET",
            f"compliance/scan/repo/{self.scan_id}",
            200
        )
        
        if success:
            # Validate response structure
            required_fields = ['id', 'system_name', 'findings', 'evidence_items', 'coverage_stats']
            missing_fields = [field for field in required_fields if field not in response]
            
            if missing_fields:
                print(f"⚠️  Missing fields in response: {missing_fields}")
            else:
                print(f"   ✅ All required fields present")
                print(f"   Findings: {len(response.get('findings', []))}")
                print(f"   Evidence: {len(response.get('evidence_items', []))}")
        
        return success

    def test_get_all_scans(self):
        """Test getting all repository scans"""
        success, response = self.run_test(
            "Get All Repository Scans",
            "GET",
            "compliance/scan/repo",
            200
        )
        
        if success and isinstance(response, list):
            print(f"   Found {len(response)} scans")
        
        return success

    def test_invalid_file_upload(self):
        """Test uploading invalid file type"""
        # Create a dummy text file
        dummy_content = b"This is not a ZIP file"
        files = {'zip_file': ('test.txt', dummy_content, 'text/plain')}
        data = {'system_name': 'Invalid Test'}
        
        success, response = self.run_test(
            "Upload Invalid File Type",
            "POST",
            "compliance/scan/repo",
            400,  # Expecting 400 Bad Request
            data=data,
            files=files
        )
        
        return success

    def test_missing_system_name(self):
        """Test upload without system name"""
        demo_file_path = "/tmp/demo-ai-project.zip"
        if not os.path.exists(demo_file_path):
            print(f"❌ Demo file not found - skipping test")
            return False

        with open(demo_file_path, 'rb') as f:
            files = {'zip_file': ('demo-ai-project.zip', f, 'application/zip')}
            # Missing system_name
            data = {}
            
            success, response = self.run_test(
                "Upload Without System Name",
                "POST",
                "compliance/scan/repo",
                422,  # Expecting validation error
                data=data,
                files=files
            )
            
            return success

    def test_nonexistent_scan(self):
        """Test getting non-existent scan"""
        fake_id = "nonexistent-scan-id"
        success, response = self.run_test(
            "Get Non-existent Scan",
            "GET",
            f"compliance/scan/repo/{fake_id}",
            404
        )
        
        return success

    def cleanup_test_scan(self):
        """Clean up test scan if created"""
        if self.scan_id:
            print(f"\n🧹 Cleaning up test scan: {self.scan_id}")
            success, response = self.run_test(
                "Delete Test Scan",
                "DELETE",
                f"compliance/scan/repo/{self.scan_id}",
                200
            )
            return success
        return True

def main():
    """Run all backend tests"""
    print("=" * 60)
    print("🧪 EU AI Act Compliance Repository Scanning API Tests")
    print("=" * 60)
    
    tester = RepoScanAPITester()
    
    # Test sequence
    tests = [
        ("Health Check", tester.test_health_check),
        ("Get Controls", tester.test_get_controls),
        ("Upload Repository", tester.test_upload_repository),
        ("Get Scan Result", tester.test_get_scan_result),
        ("Get All Scans", tester.test_get_all_scans),
        ("Invalid File Upload", tester.test_invalid_file_upload),
        ("Missing System Name", tester.test_missing_system_name),
        ("Non-existent Scan", tester.test_nonexistent_scan),
    ]
    
    # Run tests
    for test_name, test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            tester.tests_run += 1
    
    # Cleanup
    try:
        tester.cleanup_test_scan()
    except Exception as e:
        print(f"⚠️  Cleanup failed: {e}")
    
    # Print results
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    print(f"Success Rate: {(tester.tests_passed/tester.tests_run*100):.1f}%" if tester.tests_run > 0 else "No tests run")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())