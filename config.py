import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if not os.path.exists(dotenv_path):
    raise Exception('.env file does not exist')

load_dotenv(dotenv_path)


class SystemConfig:

    db_user = os.getenv('db_user')
    db_password = os.getenv('db_password')
    db_name = os.getenv('db_name')
    db_host = os.getenv('db_host')
    db_async_url = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"
    fast_api_config = {
        "host": os.getenv("fast_api_host"),
        "reload": os.getenv("fast_api_reload"),
        "port": int(os.getenv("fast_api_port")),
        "log_level": os.getenv("fast_api_log_level")
    }

    max_sentences = int(os.getenv('max_sentences'))


system_config = SystemConfig()
