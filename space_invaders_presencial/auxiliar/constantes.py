import json

screen_w = 600
screen_h = 600
CONFIG_FILE_PATH = "space_invaders_presencial/configs/config.json"


def open_configs() -> dict:
    with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as config:
        return json.load(config)
