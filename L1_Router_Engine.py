import nest_asyncio
import utils.utils as utils
from utils.AppConfig import AppConfig


def show_output(question,response):
    print(f"question:\n{question}")
    print(f"answer:\n{str(response)}")
    print(f"no. of nodes used to arrive at the response={len(response.source_nodes)}")
    print("-" * 50)

if __name__ == "__main__":

    _ = AppConfig()  #we just have to load the env
    nest_asyncio.apply()
    query_engine = utils.get_router_query_engine("metagpt.pdf")

    question = "What is the summary of the document?"
    response = query_engine.query(question)
    show_output(question,response)

    question = "How do agents share information with other agents?"
    response = query_engine.query(question)
    show_output(question,response)

    question = "Tell me about the ablation study results?"
    response = query_engine.query(question)
    show_output(question,response)

