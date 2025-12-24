import requests
import sys

BASE_URL = "http://127.0.0.1:8000"
EMAIL = f"ssh_tester_{sys.argv[1]}@example.com" if len(sys.argv) > 1 else "ssh_tester@example.com"
PASSWORD = "password123"

def run_ssh_test():
    # 1. Register & Login
    print(f"Registering {EMAIL}...")
    requests.post(f"{BASE_URL}/register", json={"email": EMAIL, "password": PASSWORD})
    login_res = requests.post(f"{BASE_URL}/login", data={"username": EMAIL, "password": PASSWORD})
    if login_res.status_code != 200:
        print("Login failed")
        return
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create Dummy Server
    print("Creating dummy server...")
    server_data = {
        "name": "Test Server",
        "ip_address": "127.0.0.1",
        "username": "testuser",
        "password": "testpassword",
        "port": 2222 
    }
    create_res = requests.post(f"{BASE_URL}/servers/", json=server_data, headers=headers)
    server_id = create_res.json()["id"]
    print(f"Created Server ID: {server_id}")

    # 3. Test Destructive Command
    print("\n--- Testing Destructive Command (rm -rf /) ---")
    bad_cmd = {"command": "sudo rm -rf /"}
    bad_res = requests.post(f"{BASE_URL}/servers/{server_id}/execute", json=bad_cmd, headers=headers)
    print(f"Status: {bad_res.status_code}") # Should be 400
    print(f"Response: {bad_res.json()}")

    # 4. Test Normal Command (Will fail connection but pass API check)
    print("\n--- Testing Normal Command (ls -la) ---")
    good_cmd = {"command": "ls -la"}
    good_res = requests.post(f"{BASE_URL}/servers/{server_id}/execute", json=good_cmd, headers=headers)
    print(f"Status: {good_res.status_code}")
    # We expect a connection error in stderr because 127.0.0.1:2222 likely doesn't exist/accept our fake creds
    print(f"Response: {good_res.json()}")

if __name__ == "__main__":
    run_ssh_test()
