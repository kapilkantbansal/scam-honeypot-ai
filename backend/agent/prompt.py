def build_prompt(persona: str, goal: str, rules: str, message: str) -> str:
    return f"""
Persona:
{persona}

Goal:
{goal}

Rules:
{rules}

Scammer message:
{message}

Respond as the persona. Do not explain your reasoning.
"""
