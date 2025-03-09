import nest_asyncio
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI

from utils.AppConfig import AppConfig


def add(x:int,y:int) -> int:
    """Adds two integers together"""
    return x + y

def mystery(x:int, y:int) -> int:
    """mystery function that operates on top of two numbers"""
    return  (x+y) * (x+y)

if __name__ == "__main__":
    config = AppConfig()
    nest_asyncio.apply()

    add_tool = FunctionTool.from_defaults(fn=add)
    mystery_tool = FunctionTool.from_defaults(fn=mystery)

    llm = OpenAI(model=config.get_open_ai_model())
    response = llm.predict_and_call(
        [
            add_tool,
            mystery_tool
        ]
        ,"Tell me the output of mystery function on 8 and 7"
        ,verbose=True
    )
    print(f"output={str(response)}")


