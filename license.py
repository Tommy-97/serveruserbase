# license.py
import hashlib
import os


def check_license(license_path):
    try:
        with open(license_path, "r") as f:
            license_key = f.read().strip()
            hashed_key = hash_license_key(license_key)
            if hashed_key == "4e26e0c6668f5465c6589f16cb7b677b50b8b87d0dc162b987cb43a1687c1124":
                return True
    except FileNotFoundError:
        pass
    return False

def hash_license_key(license_key):
    hasher = hashlib.sha256()
    hasher.update(license_key.encode('utf-8'))
    hashed_key = hasher.hexdigest()
    return hashed_key

def main():
    license_path = input("Введите путь к файлу лицензии: ")
    if not os.path.exists(license_path):
        print("Указанный файл лицензии не найден.")
        return False

    if not check_license(license_path):
        print("Пожалуйста, укажите действительный лицензионный ключ в файле лицензии.")
        return False
    return True

if __name__ == "__main__":
    main()

