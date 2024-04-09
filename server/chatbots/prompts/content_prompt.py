import os
import logging
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate


class CustomFormatter(PromptTemplate):
    def __init__(self, **kwargs):
        super().__init__(template="Question: {question}\nAnswer: {answer}", **kwargs)

    def create_prompt(self, prompt):
        formatted_prompt = (
            f"Question: {prompt['question']}\nAnswer: {prompt['answer']}\n\n"
        )
        logging.info(f"Formatted Prompts in Content Prompt {formatted_prompt}")
        return formatted_prompt


example_prompts = CustomFormatter(input_variables=["question", "answer"])


def create_few_shot_prompt(combined_prompts, example_selector, user_query):
    """
    Combine various prompts between the initial_prompt file and from save questions and answer based on the users interaction with
    the chatbot.
    """
    few_shot_template = FewShotPromptTemplate(
        initial_prompts=combined_prompts,
        example_prompts=example_prompts,
        example_selector=example_selector,
        suffix="Question: {input}",
        input_variable=["input"],
    )
    logging.info(f"Creating few shot prompts in Content Prompt")
    return few_shot_template.create_prompt(user_query)


if __name__ == "__main__":
    create_few_shot_prompt()
