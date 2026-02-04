from backend.agent.personas import RETIREE_TRAPPER
from backend.agent.rules import AGENT_RULES
from backend.agent.prompt import build_prompt
from backend.api.gemini_client import GeminiClient


class AgentController:
    def __init__(self):
        """
        Initializes the agent with persona, rules, goal, and Gemini client.
        """
        self.client = GeminiClient()

        # Persona (string)
        self.persona = RETIREE_TRAPPER["system_prompt"]

        # Goal (string)
        self.goal = "Extract payment details like UPI ID without alerting the scammer."

        # Rules (list -> formatted string)
        self.rules = "\n".join(f"- {rule}" for rule in AGENT_RULES)

    def generate_reply(self, scammer_message: str) -> str:
        """
        Generates a persona-based reply to the scammer.
        """

        prompt = build_prompt(
            persona=self.persona,
            goal=self.goal,
            rules=self.rules,
            message=scammer_message
        )

        return self.client.generate(prompt)
