
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.query_constructor.schema import AttributeInfo
from langchain.retrievers import SelfQueryRetriever
from langchain.retrievers.self_query.chroma import ChromaTranslator
from langchain_community.document_loaders.json_loader import JSONLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import OpenAIEmbeddings, ChatOpenAI


class ConversationalChatBot:
    def __init__(self, path, template_str, sample_conversation):
        self.vectorStore = self.__create_db(self.get_documents(path))
        self.retrieval_chain, self.stuff_chain = self.create_chain(self.vectorStore, template_str)
        self.chat_history = []
        self.sample_conversation = sample_conversation

    @staticmethod
    def __create_db(docs):
        embedding = OpenAIEmbeddings()
        vector_store = Chroma.from_documents(docs, embedding=embedding)
        return vector_store

    @staticmethod
    def get_documents(path):
        def metadata_func(record: dict, metadata: dict) -> dict:
            metadata["difficulty"] = record.get("difficulty")
            metadata["category"] = record.get("category")
            metadata["asked"] = record.get("asked")
            return metadata

        loader = JSONLoader(
            file_path=path,
            jq_schema='.results[]',
            metadata_func=metadata_func,
            text_content=False)

        docs = loader.load()

        return docs

    @staticmethod
    def create_chain(vector_store, template_str):
        model = ChatOpenAI(
            model="gpt-3.5-turbo-1106",
            temperature=0.4
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", template_str),
            MessagesPlaceholder(variable_name="sample_conversation"),
            ("human", "Follow the above sample conversation to generate response"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{user_input}")]
        )

        # chain = prompt | model
        stuff_chain = create_stuff_documents_chain(
            llm=model,
            prompt=prompt,
        )

        metadata_field_info = [

            AttributeInfo(
                name="category",
                description="The category of the question",
                type="string",
            ),
            AttributeInfo(
                name="difficulty",
                description="The difficulty of the question. One of ['easy', 'medium', 'hard']",
                type="string",
            ),

            AttributeInfo(
                name="asked",
                description="if the question is asked before. One of ['false', 'true']",
                type="String"
            ),
        ]

        document_content_description = "set of different questions"

        retriever = SelfQueryRetriever.from_llm(
            model,
            vector_store,
            document_content_description,
            metadata_field_info,
            structuredQueryTranslator=ChromaTranslator(),
            search_kwargs={"k": 1}
        )

        retriever_prompt = ChatPromptTemplate.from_messages([
            ("human",
             "attribute asked is equal to {asked} and Attribute difficulty equal to {difficulty}."),
        ])

        retrieval_chain = retriever_prompt | retriever

        return retrieval_chain, stuff_chain

    def generate_response(self, user_input, stuff_input_variables, retrieval_input_variables):
        retrieved_docs = self.retrieval_chain.invoke(retrieval_input_variables)
        print(retrieved_docs)
        temp_dict = {
            "user_input": user_input,
            "chat_history": self.chat_history,
            "sample_conversation": self.sample_conversation,
            "context": retrieved_docs
        }
        temp_dict.update(stuff_input_variables)
        response = self.stuff_chain.invoke(temp_dict)

        all_docs = self.vectorStore.get()
        for retrieved_doc in retrieved_docs:
            for doc in all_docs['documents']:
                if doc == retrieved_doc.page_content:
                    doc_index = all_docs['documents'].index(doc)
                    doc_id = all_docs['ids'][doc_index]
                    retrieved_doc.metadata.update({"asked": 'true'})
                    self.vectorStore.update_document(doc_id, retrieved_doc)
                    break

        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=response))
        return response

    def getChatHistoryString(self):
        chat_history = []
        for message in self.chat_history:
            chat_history.append({"type": type(message).__name__, "content": message.content})
        return chat_history
