import requests
import sys
import os

# Configuration
DOJO_URL = "http://172.17.0.1:8081" # Host IP so Docker can reach it
API_KEY = os.environ.get('DOJO_API_KEY')
PRODUCT_NAME = "CodeFortress App"
ENGAGEMENT_NAME = "CI/CD Pipeline Scan"

def upload_scan(scan_type, file_path):
    print(f"Uploading {scan_type} from {file_path}...")
    
    headers = {'Authorization': f"Token {API_KEY}"}
    
    # 1. Get Engagement ID (Simplified: We assume it exists)
    # In a real script, we would query the API to find the ID dynamically.
    # For this lab, let's hardcode the Engagement ID = 1 (usually the first one created).
    engagement_id = 1 

    files = {'file': open(file_path, 'rb')}
    data = {
        'engagement': engagement_id,
        'scan_type': scan_type,
        'active': 'true',
        'verified': 'false',
        'close_old_findings': 'true'
    }

    response = requests.post(f"{DOJO_URL}/api/v2/import-scan/", headers=headers, files=files, data=data)

    if response.status_code == 201:
        print("✅ Upload Successful!")
    else:
        print(f"❌ Upload Failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 defectdojo_upload.py <Scan_Type> <File_Path>")
        sys.exit(1)

    scan_type = sys.argv[1]
    file_path = sys.argv[2]
    
    upload_scan(scan_type, file_path)