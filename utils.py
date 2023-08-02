import os, sys
import base64

def get_base_path():
    return os.path.dirname(os.path.abspath(sys.argv[0]))

def convert_b64_to_file(filename, b64_data):
    # with open(filename, 'wb') as file
    try:
        b64_data = base64.b64decode(b64_data).encode("utf-8")
        with open(filename, 'wb') as file:
            file.write(b64_data)
    except Exception:
        return False
    return True
