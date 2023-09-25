import os
import logging

from malevich_space.schema import Setup
from malevich_space.parser import YAMLParser


def get_file_path(name: str):
    home_dir = os.path.expanduser("~")
    file_path = os.path.join(home_dir, name)
    return file_path


def set_active(path: str, active_cache_name: str):
    config = Setup(**YAMLParser.parse_yaml(path))
    target_path = get_file_path(active_cache_name)
    YAMLParser.dump_yaml(target_path, config.model_dump())
    logging.info(f">> Active host: {config.space}")


def get_active(active_cache_name: str) -> Setup:
    src_path = get_file_path(active_cache_name)
    try:
        return Setup(**YAMLParser.parse_yaml(src_path))
    except ValueError:
        raise ValueError("Env is not set. Use: space env set")
