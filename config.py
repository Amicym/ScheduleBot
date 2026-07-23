import os, pathlib

def get_token():
    env_path = pathlib.Path("~/Bot_raspisanie/.env").expanduser()

    if env_path.exists():
        with open(env_path, mode="r", encoding="utf-8") as f:
            for line in f:
                if line.strip() or line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

    return os.getenv("BOT_TOKEN")