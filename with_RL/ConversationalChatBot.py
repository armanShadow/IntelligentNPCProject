from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders import JSONLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from config import NUM_DOCS_TO_BE_RETRIEVED, TEMPERATURE, OPEN_AI_MODEL

load_dotenv()


class ConversationalChatBot:
    def __init__(self, template_str):
        self.docs = self.get_documents_from_json()
        self.vectorStore = self.__create_db(self.docs)
        self.chain = self.create_chain(self.vectorStore, template_str)
        self.chat_history = []
        self.context = []
        #self.difficulty_level = ""

    @staticmethod
    def __create_db(docs):
        embedding = OpenAIEmbeddings()
        vector_store = Chroma.from_documents(docs, embedding=embedding)
        return vector_store

    @staticmethod
    def get_documents_from_json():
        loader = JSONLoader(
        file_path='./data/training.json',
        jq_schema='.',
        text_content=False)
        docs = loader.load()

        #splitter = RecursiveCharacterTextSplitter(
        #    chunk_size=400,
        #    chunk_overlap=20
        #)
        #split_docs = splitter.split_documents(docs)
        return docs

    @staticmethod
    def create_chain(vector_store, template_str):
        model = ChatOpenAI(
            model=OPEN_AI_MODEL,
            temperature=TEMPERATURE
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", template_str),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")]
        )

        # chain = prompt | model
        chain = create_stuff_documents_chain(
            llm=model,
            prompt=prompt
        )

        retriever = vector_store.as_retriever(search_kwargs={"k": NUM_DOCS_TO_BE_RETRIEVED})

        retriever_prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="chat_history"),
            MessagesPlaceholder(variable_name="context"),
            #MessagesPlaceholder(variable_name="difficulty_level"),
            ("human", "{input}"),
            ("human",
             "Given the above conversation, generate a search query to look up {context} or {chat_history}"
             "in order to get information relevant to the conversation.")
        ])

        history_aware_retriever = create_history_aware_retriever(
            llm=model,
            retriever=retriever,
            prompt=retriever_prompt
        )

        retrieval_chain = create_retrieval_chain(
            #retriever,
            history_aware_retriever,
            chain
        )

        return retrieval_chain

    def generate_response(self, user_input, input_variables):
        temp_dict = {
            "input": user_input,
            "chat_history": self.chat_history,
            "context": self.context,
            #"difficulty_level": self.difficulty_level
        }
        temp_dict.update(input_variables)
        print(temp_dict)
        response = self.chain.invoke(temp_dict)
        print(response)
        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=response["answer"]))
        return response["answer"]
