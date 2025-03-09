from llama_index.core import SimpleDirectoryReader
from llama_index.core import SummaryIndex, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.tools import QueryEngineTool
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from typing import List
from llama_index.core.vector_stores import FilterCondition, MetadataFilters

from utils.AppConfig import AppConfig

config = AppConfig()

def _create_nodes(file_path: str):

    """create nodes from document"""

    # load documents
    documents = SimpleDirectoryReader(input_files=[file_path]).load_data()

    splitter = SentenceSplitter(chunk_size=1024)
    return splitter.get_nodes_from_documents(documents)

def get_summary_tool(file_path,llm):

    nodes = _create_nodes(file_path)
    summary_index = SummaryIndex(nodes)

    summary_query_engine = summary_index.as_query_engine(
        response_mode="tree_summarize",
        use_async=True,
        llm=llm
    )

    return QueryEngineTool.from_defaults(
        name="summary_tool",
        query_engine=summary_query_engine,
        description=(
            "Useful if you want to get a summary of MetaGPT"
        )
    )


def get_router_query_engine(file_path: str, llm = None, embed_model = None):

    """Get router query engine."""

    llm = llm or OpenAI(model=config.get_open_ai_model())
    embed_model = embed_model or OpenAIEmbedding(model=config.get_open_ai_embedding_model())

    nodes = _create_nodes(file_path)

    vector_index = VectorStoreIndex(nodes, embed_model=embed_model)
    
    vector_query_engine = vector_index.as_query_engine(llm=llm)
    
    summary_tool = get_summary_tool(file_path,llm)
    
    vector_tool = QueryEngineTool.from_defaults(
        query_engine=vector_query_engine,
        description=(
            "Useful for retrieving specific context from the MetaGPT paper."
        ),
    )
    
    query_engine = RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(),
        query_engine_tools=[
            summary_tool,
            vector_tool,
        ],
        verbose=True
    )
    return query_engine

def get_vector_query_response(file_path:str,query:str, page_numbers: List[str]):
    """
    perform a vector search over an index

    query (str): the string query to be embedded.
    page_numbers (List[str]): Filter by set of pages.
    Leave it blank if want to include all pages. Otherwise
    filter by set of specified pages
    """
    nodes = _create_nodes(file_path)
    vector_index = VectorStoreIndex(nodes)

    metadata_dicts = [
        {"key": "page_label", "value": p} for p in page_numbers
    ]

    query_engine = vector_index.as_query_engine(
                    similarity_top_k = 2,
                    filters=MetadataFilters.from_dicts(
                                metadata_dicts,condition=FilterCondition.OR
                            )
    )

    result = query_engine.query(query)
    return result

if __name__ == "__main__":
    response = get_vector_query_response("metagpt.pdf",
                                         "What are some high-level results of MetaGPT?",
                                         ["2"])
    print(f"response=\n{str(response)}")

    print(f"metadata=")
    for n in response.source_nodes:
        print(n.metadata)
        print("-" * 50)


