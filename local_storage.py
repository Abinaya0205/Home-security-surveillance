# cloud/local_storage.py
import os
import shutil

class LocalStorage:
    def __init__(self, base_folder="cloud"):
        self.base_folder = os.path.abspath(base_folder)
        os.makedirs(self.base_folder, exist_ok=True)

    def upload(self, local_path: str, remote_name: str = None) -> str:
        if remote_name is None:
            remote_name = os.path.basename(local_path)
        remote_path = os.path.join(self.base_folder, remote_name)

        # If source and destination are the same file → skip copy
        if os.path.abspath(local_path) == os.path.abspath(remote_path):
            return remote_path

        # If destination already exists → skip copy
        if os.path.exists(remote_path):
            return remote_path

        shutil.copy(local_path, remote_path)
        return remote_path

    def download(self, remote_name: str, local_path: str) -> str:
        remote_path = os.path.join(self.base_folder, remote_name)
        if os.path.abspath(remote_path) == os.path.abspath(local_path):
            return local_path
        shutil.copy(remote_path, local_path)
        return local_path

    def exists(self, remote_name: str) -> bool:
        return os.path.exists(os.path.join(self.base_folder, remote_name))

    def delete(self, remote_name: str):
        path = os.path.join(self.base_folder, remote_name)
        if os.path.exists(path):
            os.remove(path)