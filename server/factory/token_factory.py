from langchain.callbacks import get_openai_callback
from pprint import pprint


class TokenCounterFactory:
    def create_token_counter(self, agent):
        def count_tokens(query):
            with get_openai_callback() as cb:
                result = agent(query)
                self._log_token_usage(cb)
            return result

        return count_tokens

    def _log_token_usage(self, callback):
        # Log the token usage and costs
        pprint(f"Spent a total of {callback.total_tokens} tokens")
        pprint(f"Prompt Tokens: {callback.prompt_tokens}")
        pprint(f"Completion Tokens: {callback.completion_tokens}")
        pprint(f"Total Cost (USD): ${callback.total_cost}")


# Usage
# token_counter_factory = TokenCounterFactory()
# token_counter = token_counter_factory.create_token_counter(your_agent)
# result = token_counter("Your query here")
