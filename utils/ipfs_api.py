import requests

IPFS_API_URL = 'http://10.0.0.176:5001/api/v0/add'

def upload_to_ipfs(file_path):
    try:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(IPFS_API_URL, files=files)

            if response.status_code == 200:
                ipfs_hash = response.json()['Hash']
                print(f"File uploaded successfully! IPFS Hash: {ipfs_hash}")
                return ipfs_hash
            else:
                print(f"Failed to upload file. Status code: {response.status_code}")
                print(response.text)
                return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
