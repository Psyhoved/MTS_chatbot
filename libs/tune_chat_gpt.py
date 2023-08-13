from langchain.chat_models import ChatOpenAI
from llama_index import SimpleDirectoryReader, PromptHelper, GPTVectorStoreIndex
from llama_index import LLMPredictor, ServiceContext
from pathlib import Path

root_dir = Path(__file__).parent.parent.absolute()


def construct_index(directory_path: str) -> None:
    # set number of output tokens
    num_outputs = 256

    # define LLM
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.5, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
    index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)

    index.storage_context.persist(persist_dir=f"{root_dir}\index.json")


if __name__ == '__main__':
    construct_index(f"{root_dir}\data\MTS")
