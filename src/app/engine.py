from typing import cast
from llama_index.prompts.prompts import SimpleInputPrompt
from llama_index.llm_predictor import HuggingFaceLLMPredictor
from llama_index import (
    KeywordTableIndex,
    Response,
    ServiceContext,
    SimpleDirectoryReader,
)

libbnb = "/opt/conda/lib/python3.10/site-packages/bitsandbytes/libbitsandbytes_"
from os import system
system(f'cp {libbnb}cuda117.so {libbnb}cpu.so')

class Engine:
    def __init__(self):
        system_prompt = """<|SYSTEM|># StableLM Tuned (Alpha version)
- StableLM is a helpful and harmless open-source AI language model developed by StabilityAI.
- StableLM is excited to be able to help the user, but will refuse to do anything that could be considered harmful to the user.
- StableLM will refuse to participate in anything that could harm a human.
"""
        query_wrapper_prompt = SimpleInputPrompt("<|USER|>{query_str}<|ASSISTANT|>")
        stablelm_predictor = HuggingFaceLLMPredictor(
#            model_name="stabilityai/stablelm-tuned-alpha-3b",
#            tokenizer_name="stabilityai/stablelm-tuned-alpha-3b",
            max_new_tokens=256,
            generate_kwargs={"temperature": 0.7, "do_sample": False},
            system_prompt=system_prompt,
            query_wrapper_prompt=query_wrapper_prompt,
            device_map="sequential",
            model_kwargs={"load_in_4bit": True},
        )
        service_context = ServiceContext.from_defaults(
            chunk_size=1024, llm_predictor=stablelm_predictor
        )
        documents = SimpleDirectoryReader("data").load_data()
        index = KeywordTableIndex.from_documents(
            documents, service_context=service_context
        )
        self.engine = index.as_query_engine()

    def ask(self, query):
        a = cast(Response, self.engine.query(query)).response
        return a or "No response"


engine = Engine()
