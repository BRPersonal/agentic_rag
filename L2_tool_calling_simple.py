import nest_asyncio
from llama_index.core.tools import FunctionTool
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI


def add(x:int,y:int) -> int:
    """Adds two integers together"""
    return x + y

def mystery(x:int, y:int) -> int:
    """mystery function that operates on top of two numbers"""
    return  (x+y) * (x+y)

if __name__ == "__main__":
    load_dotenv(override=True)
    nest_asyncio.apply()

    add_tool = FunctionTool.from_defaults(fn=add)
    mystery_tool = FunctionTool.from_defaults(fn=mystery)

    llm = OpenAI(model="gpt-3.5-turbo")
    response = llm.predict_and_call(
        [
            add_tool,
            mystery_tool
        ]
        ,"Tell me the output of mystery function on 8 and 7"
        ,verbose=True
    )
    print(f"output={str(response)}")


