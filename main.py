from groq import Groq
from openai import OpenAI
from config import env_config

class LLMApp:
    def __init__(self, api_key=None, model="llama-3.3-70b-versatile", provider="groq"):
        self.provider = provider.lower()
        self.api_key = api_key or (
            env_config.groq_api_key if self.provider == "groq" else env_config.openai_api_key
        )

        if not self.api_key:
            raise ValueError(f"{self.provider.capitalize()} API key must be provided or set in config")

        if self.provider == "groq":
            self.client = Groq(api_key=self.api_key)
        elif self.provider == "openai":
            self.client = OpenAI(api_key=self.api_key)
        else:
            raise ValueError("Unsupported provider. Use 'groq' or 'openai'.")

        self.model = model
        self.conversation_history = []

    def chat(self, user_message, system_prompt=None, temperature=0.5, max_tokens=1024):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": user_message})
        
    
        if self.provider == "groq" and self.model not in ["gpt-5", "gpt-5-mini", "gpt-5-nano"]:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens, 
            )
            assistant_message = response.choices[0].message.content

        else:  # OpenAI or GPT-5 variants
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_completion_tokens=max_tokens, #OpenAI introduced a newer name `max_completion_tokens` version mid 2024. max_tokens can also be used
            )
            assistant_message = response.choices[0].message["content"]

        # Update conversation history
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": assistant_message})

        return assistant_message


if __name__ == "__main__":
    app = LLMApp()
    message = input("What do you want to ask: ")
    response = app.chat(message)
    print(f"Assistant Response: {response}")
