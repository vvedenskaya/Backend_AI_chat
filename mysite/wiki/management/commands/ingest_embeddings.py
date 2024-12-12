import pickle
from django.core.management.base import BaseCommand
from django.conf import settings
from langchain_text_splitters import CharacterTextSplitter

from ...models import Article
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from pathlib import Path
from langchain_core.documents import Document





class Command(BaseCommand):
    help = "Ingest Wikipedia articles as embeddings into a FAISS vector database."

    def add_arguments(self, parser):
        parser.add_argument("--delete", action="store_true")
        parser.add_argument("--limit", type=int, default=1)
        parser.add_argument("--path", type=str, default="./chat_with_wikipedia.pkl")

    def handle(self, *args, **options):
        # Logic for embedding articles and saving them into the vector database…
        limit = options.get("limit")
        path = options.get("path")
        if options["delete"]:
            self.stdout.write(f"Are you sure you want to delete {path} articles? (yes/no)")
            response = input()
            if response == "yes":
                self._prompt_delete_vector_database(path=path)

        article_qs = Article.objects.all()[:limit]
        vectorstore = self._populate_vectorstore(article_qs)
        self._save_vectorstore(path, vectorstore)


    def _prompt_delete_vector_database(self, path: str):
        Path(path).unlink(missing_ok=True)
        self.stdout.write(self.style.SUCCESS('Vector database deleted.'))


    def _populate_vectorstore(self, article_qs):
        documents = []
        for article in article_qs:
            self.stdout.write(f'Starting to process {article.title=}')
            try:
                title_doc = Document(
                    page_content=article.title,
                    metadata={"source": article.url, "title": article.title, "field": "title"}
                )
                text_doc = Document(
                    page_content=article.text,
                    metadata={"source": article.url, "title": article.title, "field": "text"}
                )
                text_splitter = CharacterTextSplitter(separator="\n\n", chunk_size=600, chunk_overlap=100)
                documents.extend(text_splitter.split_documents([title_doc, text_doc]))
            except Exception as err:
                self.stdout.write(self.style.ERROR(f"Error: {article.url}, {article.title}, {err}"))

        embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        return FAISS.from_documents(documents, embeddings)


    def _save_vectorstore(self, path, vectorstore):
        #with open(path, "wb") as f:
            #pickle.dump(vectorstore, f)
        # Save the vectorstore object locally
        vectorstore.save_local("vectorstore")

        # Load the vectorstore object
        #x = FAISS.load_local("vectorstore", embeddings)

        self.stdout.write(self.style.SUCCESS('Vector store saved.'))
