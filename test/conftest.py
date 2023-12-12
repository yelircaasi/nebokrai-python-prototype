import os
from pathlib import Path

root_path_file = Path("/tmp/text_data_root_path.txt")
root_path = Path(__file__).parent / "data/default"
with open(root_path_file, "w", encoding="utf-8") as f:
    f.write(str(root_path))


os.environ.update({"NEBOKRAI_ROOT_FILE": str(root_path_file)})
