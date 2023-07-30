import constant
import os
from utils import get_base_path

current_status = constant.IDLE_STATUS
current_language = constant.LANGUAGE_ID
base_url = os.environ.get('API_BASE_URL')

output_filename = os.path.join(get_base_path(), 'output.mp3')

def change_status(status):
    global current_status

    current_status = status

def change_language(lang):
    global current_language
    
    current_language = lang