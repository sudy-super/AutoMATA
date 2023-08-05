import os
import json

class MakeMemory:
    def __init__(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.memory_store_path = os.path.join(script_directory, "memory_store.json")

    def making_memory(self, content):
        with open(self.memory_store_path, "a", encoding = "utf-8") as f:
            load_data = json.load(f)
            content["id"] = str(len(load_data))
            json.dump(content, f, indent=4)