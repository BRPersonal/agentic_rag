import nest_asyncio
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI
import utils.utils as utils

from utils.AppConfig import AppConfig

if __name__ == "__main__":
    config = AppConfig()
    nest_asyncio.apply()

    vector_query_tool = FunctionTool.from_defaults(
        name="vector_tool",
        fn=utils.get_vector_query_response
    )

    llm = OpenAI(model=config.get_open_ai_model(), temperature=0)

    #key lesson: prompt makes all the difference
    #when the file name was not mentioned in the prompt, file_path arg was going as data/metagpt.pdf
    #and resulted in file not found error. Included file name in the prompt and it worked like magic
    response = llm.predict_and_call(
        [vector_query_tool],
        "What are the high-level results of MetaGPT as described on page 2 in file metagpt.pdf?",
        verbose=True
    )

    print("metadata\n-----------------")
    for n in response.source_nodes:
        print(n.metadata)

    summary_tool = utils.get_summary_tool("metagpt.pdf", llm)
    response = llm.predict_and_call(
        [vector_query_tool, summary_tool],
        "What are the MetaGPT comparisons with ChatDev described on page 8 in file metagpt.pdf?",
        verbose=True
    )

    print("metadata\n-----------------")
    for n in response.source_nodes:
        print(n.metadata)

    response = llm.predict_and_call(
        [vector_query_tool, summary_tool],
        "What is a summary of the paper?",
        verbose=True
    )