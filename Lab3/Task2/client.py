
#change the localhost to the server ip address for accessing lab pc or same router
import requests

localhost ="localhost"

def download_file(url):
    response = requests.get(url)

    if response.status_code == 200:
        with open('downloaded_file.pdf', 'wb') as f:
            f.write(response.content)
        print("File downloaded successfully.")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


def list_files(url):
    response = requests.get(url)

    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Failed to list files. Status code: {response.status_code}")


def upload_file(url, file_path):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        print("File uploaded successfully.")
    else:
        print(f"Failed to upload file. Status code: {response.status_code}")


if __name__ == "__main__":
    while True:
        print("1. List files")
        print("2. Upload file")
        print("3. Download file")
        print("4. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            list_files(f"http://{localhost}:8000/list")
        elif choice == 2:
            file_path = input("Enter the file path: ")
            upload_file(f"http://{localhost}:8000/upload", file_path)
        elif choice == 3:
            file_name = input("Enter the file name: ")
            download_file(f"http://{localhost}:8000/download/{file_name}")
        elif choice == 4:
            break
        else:
            print("Invalid choice. Please try again.")

            