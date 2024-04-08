from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter



class ConversationalChatBot:
    def __init__(self, url, template_str):
        self.docs = self.get_documents_from_web_url(url)
        self.vectorStore = self.__create_db(self.docs)
        self.chain = self.create_chain(self.vectorStore, template_str)
        self.chat_history = []

    @staticmethod
    def __create_db(docs):
        embedding = OpenAIEmbeddings()
        vector_store = Chroma.from_documents(docs, embedding=embedding)
        return vector_store

    @staticmethod
    def get_documents_from_web_url(url):
        loader = WebBaseLoader(url)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=20
        )
        split_docs = splitter.split_documents(docs)
        return split_docs

    @staticmethod
    def create_chain(vector_store, template_str):
        model = ChatOpenAI(
            model="gpt-3.5-turbo-1106",
            temperature=0.4
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

        retriever = vector_store.as_retriever(search_kwargs={"k": 3})

        retriever_prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            ("human",
             "Given the above conversation, generate a search query to look up in order to get information relevant "
             "to the conversation")
        ])

        history_aware_retriever = create_history_aware_retriever(
            llm=model,
            retriever=retriever,
            prompt=retriever_prompt
        )

        retrieval_chain = create_retrieval_chain(
            # retriever,
            history_aware_retriever,
            chain
        )

        return retrieval_chain

    def generate_response(self, user_input, input_variables):
        temp_dict = {
            "input": user_input,
            "chat_history": self.chat_history
        }
        temp_dict.update(input_variables)
        response = self.chain.invoke(temp_dict)
        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=response["answer"]))
        return response["answer"]
