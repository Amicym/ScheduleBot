import os, pathlib

def get_token():
    env_path = pathlib.Path(__file__).parent / ".env"

    if env_path.exists():
        with open(env_path, mode="r", encoding="utf-8") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

    return os.getenv("BOT_TOKEN")