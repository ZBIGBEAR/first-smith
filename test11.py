from langchain.prompts import StringPromptTemplate
from pydantic import BaseModel, field_validator
import inspect

def test():
    print("test")

def get_source_code(function_name):
    # Get the source code of the function
    return inspect.getsource(function_name)


class FunctionExplainerConfig(BaseModel):
    input_variables: list

    # @validator("input_variables")
    @field_validator("input_variables", mode="before")
    def validate_input_variables(cls, v):
        """Validate that the input variables are correct."""
        if len(v) != 1 or "function_name" not in v:
            raise ValueError("function_name must be the only input_variable.")
        return v


class FunctionExplainerPromptTemplate:
    """A custom prompt template that takes in the function name as input, 
       and formats the prompt template to provide the source code of the function."""

    def __init__(self, config: FunctionExplainerConfig):
        self.config = config

    def format(self, **kwargs) -> str:
        # Get the source code of the function
        source_code = get_source_code(kwargs["function_name"])

        # Generate the prompt to be sent to the language model
        prompt = f"""
        Given the function name and source code, generate an English language explanation of the function.
        Function Name: {kwargs["function_name"].__name__}
        Source Code:
        {source_code}
        Explanation:
        """
        return prompt

    def _prompt_type(self):
        return "function-explainer"


config = FunctionExplainerConfig(input_variables=["function_name"])
fn_explainer = FunctionExplainerPromptTemplate(config=config)

# 为函数"get_source_code"生成一个提示
prompt = fn_explainer.format(function_name=test)
print(prompt)