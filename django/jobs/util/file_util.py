# -*- coding: utf-8 -*-
from pathlib import Path
import json
import yaml

class FileUtil:
  @staticmethod
  def basename(file_name: str)-> str:
    # cf.: https://stackoverflow.com/a/50876889
    return Path(file_name).stem

  @staticmethod
  def write_json(file_name: str, value):
    with FileUtil.path_for(file_name, True).open(mode='wt', encoding='utf-8') as file:
      json.dump(value, file, ensure_ascii=False, indent=2, sort_keys=True)

  @staticmethod
  def read_yml(file_name: str):
    return yaml.load(FileUtil.read_text(file_name))

  @staticmethod
  def write_yml(file_name: str, value: dict):
    return FileUtil.write_text(file_name, yaml.dump(value))

  @staticmethod
  def read_json(file_name: str):
    with FileUtil.path_for(file_name).open(mode='rt', encoding='utf-8') as file:
      return json.load(file)

  @staticmethod
  def write_text(file_name: str, data: str):
    return FileUtil.path_for(file_name, True).write_text(data, encoding='utf-8')

  @staticmethod
  def read_text(file_name: str)-> str:
    return Path(file_name).read_text(encoding='utf-8')

  @staticmethod
  def read_bytes(file_name: str):
    return Path(file_name).read_bytes()

  @staticmethod
  def last_modified(file_name: str)-> float:
    try:
      return FileUtil.path_for(file_name).stat().st_mtime
    except FileNotFoundError:
      return 0

  @staticmethod
  def path_for(file_name: str, ensure_dirs: bool = False)-> Path:
    path = Path(file_name)
    if ensure_dirs:
      path.parent.mkdir(parents=True, exist_ok=True)
    return path

  @staticmethod
  def glob(directory: str, pattern: str)-> iter:
    return [str(name) for name in Path(directory).glob(pattern)]
