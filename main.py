# Monkeypatch CrewAI LLM to strip cache_breakpoint for non-Anthropic providers (fixes Groq error)
from crewai.llm import LLM
original_format_messages = LLM._format_messages_for_provider

def patched_format_messages(self, messages):
    formatted = original_format_messages(self, messages)
    if not self.is_anthropic:
        cleaned = []
        for msg in formatted:
            if isinstance(msg, dict):
                cleaned.append({k: v for k, v in msg.items() if k != "cache_breakpoint"})
            else:
                cleaned.append(msg)
        return cleaned
    return formatted

LLM._format_messages_for_provider = patched_format_messages

from dotenv import load_dotenv
from crew import research_crew

load_dotenv()

def run(topic: str):
    result = research_crew.kickoff(inputs={"topic": topic})

    print("-"*50)
    print(result)
    print("-" * 50)

if __name__ == "__main__":
    topic = (
        "Machine Learning Operations (MLOps)"
    )

    run(topic)
