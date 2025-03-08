# agentic_rag
Python based application to build agentic RAG with LlamaIndex. 

Install virtual environment and activate it
$ python -m venv .venv
$ source .venv/bin/activate

verify that you are inside the virtual environment. The path 
should point to .venv folder inside your project folder  
$ which python
/Users/adiyen/poc/python/agentic_rag/.venv/bin/python


$ pip list

Upgrade pip if needed
$ pip install --upgrade pip

$ pip install -r requirements.txt

Running L1_Router_Engine.py gave abstract class error - OpenAI cannot be instantiated
  File "/Users/adiyen/temp/backup/agentic_rag/L1_Router_Engine.py", line 60, in <module>
    Settings.llm = OpenAI(model="gpt-3.5-turbo")
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: Can't instantiate abstract class OpenAI without an implementation for abstract method '_prepare_chat_with_tools'

googled and found this solution

$ pip install -U llama-index llama-index-llms-openai
Captured the installed packages back in requirements.txt

$ pip freeze > requirements.txt 





