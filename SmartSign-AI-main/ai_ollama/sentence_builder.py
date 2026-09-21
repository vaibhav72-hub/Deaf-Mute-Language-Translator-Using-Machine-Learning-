import subprocess
import re

def build_sentence(text):
    text = text.strip().upper()

    # 🔹 Convert joined words like ILOVEYOU → I LOVE YOU
    text = re.sub(r"(I)(LOVE)(YOU)", r"\1 \2 \3", text)

    words = text.split()

    # ✅ If single word → return directly (NO LLM)
    if len(words) == 1:
        return words[0]

    prompt = (
        "You are a sentence corrector.\n"
        "Rules:\n"
        "- Do NOT explain anything\n"
        "- Do NOT ask questions\n"
        "- Do NOT add extra words\n"
        "- Only return a short simple sentence\n\n"
        f"Input: {text}\n"
        "Output:"
    )

    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt,
            text=True,
            encoding="utf-8",
            errors="ignore",
            capture_output=True
        )
        output = result.stdout.strip()
        # 🛡️ Safety fallback
        return output if output else text
    except FileNotFoundError:
        # If Ollama is not installed or not in PATH, just return the text
        return text
