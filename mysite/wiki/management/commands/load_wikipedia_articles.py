from django.core.management.base import BaseCommand, CommandError
from datasets import load_dataset
from mysite.wiki.models import Article

class Command(BaseCommand):
    help = "Load wikipedia articles using HuggingFace datasets"

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=10)
        parser.add_argument("--subset", type=str, default="20220301.simple")

    def handle(self, *args, **options):
        subset_name = options["subset"]
        limit = options["limit"]
        wikipedia_data = load_dataset("wikipedia", subset_name, split=f"train[0:{limit}]")

        articles_to_create = self._prepare_articles(wikipedia_data)
        self._save_articles(articles_to_create)

    def _prepare_articles(self, wikipedia_data):
        articles = []
        for row in wikipedia_data:
            print(f"{row['id']=}, {row['title']=},{row['url']=}")
            articles.append(Article(**row))
        return articles

    def _save_articles(self, articles):
        try:
            Article.objects.bulk_create(articles)
            self.stdout.write(self.style.SUCCESS(f"Saved {len(articles)} Articles"))
        except Exception as err:
            self.stdout.write(self.style.ERROR(f"An error occurred while trying to save the articles\nException:\n\n{err}"))
