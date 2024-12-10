from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
import pickle
from django.core.management.base import BaseCommand
from django.conf import settings
from langchain_text_splitters import CharacterTextSplitter

from mysite.wiki.models import Article
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from pathlib import Path
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory




class Command(BaseCommand):
    help = "Ingest Wikipedia articles as embeddings into a FAISS vector database."

    def add_arguments(self, parser):
        parser.add_argument("--delete", action="store_true")
        parser.add_argument("--limit", type=int, default=1)
        parser.add_argument("--path", type=str, default="./chat_with_wikipedia.pkl")

    def handle(self, *args, **options):

        # Command-line loop for chatting with Wikipedia data…

        print("[bold]Chat with wikipedia!")
        print("[bold red]---------------")
        qa_chain = get_qa_chain()
        while True:
            default_question = "Ask wikipedia: what is August?"
            question = input("Your Question: ")
            result = qa_chain({"question": question})
            print(f"[green]Answer: [/green]{result['answer']}")
            print("[bold red]---------------")


def get_qa_chain():
    """Initialize a ConversationalRetrievalChain for Q&A."""
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)
    embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    retriever = FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization = True)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory)


