PROMPTS_DIR = "src/prompts"

def load_prompt(name: str) -> str:
    path = PROMPTS_DIR + "/" + name + ".txt"
    with open(path) as prompt_file:
        return prompt_file.read().strip()