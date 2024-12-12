from django.core.management.base import BaseCommand, CommandError
from datasets import load_dataset
from mysite.wiki.models import Article

class Command(BaseCommand):
    help = "Load dataset using HuggingFace datasets"

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=10)
        parser.add_argument("--subset", type=str, default="20220301.simple")

    def handle(self, *args, **options):
        subset_name = options["subset"]
        limit = options["limit"]
        ds = load_dataset("Spiderman01/Domestic_violence_info_support_fromposts")

        articles_to_create = self._prepare_articles(ds)
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
            self.stdout.write(
                self.style.ERROR(f"An error occurred while trying to save the articles\nException:\n\n{err}"))









        # dataset_1 = load_dataset("infinite-dataset-hub/SmallTalkDialogues", split=f"train[0:{limit}]")
        # dataset_2 = load_dataset("infinite-dataset-hub/ViolenceAgainstMinorities", split=f"train[0:{limit}]")
        # dataset_3 = load_dataset("RedaAlami/hate_lgbtq_dataset", split=f"train[0:{limit}]")
        # dataset_4 = load_dataset("RedaAlami/lgbtq_dataset2", split=f"train[0:{limit}]")


        # self._process_and_save(dataset_1)
        # self._process_and_save(dataset_2)
        # self._process_and_save(dataset_3)
        # self._process_and_save(dataset_4)


    # def _process_and_save(self, dataset):
    #     # Подготовка и сохранение статей
    #     articles_to_create = self._prepare_articles(dataset)
    #     self._save_articles(articles_to_create)
    #
    # def _prepare_articles(self, dataset):
    #     articles = []
    #     for row in dataset:
    #         print(f"{row['id']=}, {row['title']=}, {row['url']=}")
    #         articles.append(Article(**row))  # Создаем объект статьи
    #     return articles
    #
    # def _save_articles(self, articles):
    #     try:
    #         # Сохраняем статьи в базе данных
    #         Article.objects.bulk_create(articles)
    #         self.stdout.write(self.style.SUCCESS(f"Сохранено {len(articles)} статей"))
    #     except Exception as err:
    #         self.stdout.write(self.style.ERROR(f"Произошла ошибка при сохранении статей:\n{err}"))













        #articles_to_create = self._prepare_articles(wikipedia_data)
        #self._save_articles(articles_to_create)

    # def _prepare_articles(self, wikipedia_data):
    #     articles = []
    #     for row in wikipedia_data:
    #         print(f"{row['id']=}, {row['title']=},{row['url']=}")
    #         articles.append(Article(**row))
    #     return articles
    #
    # def _save_articles(self, articles):
    #     try:
    #         Article.objects.bulk_create(articles)
    #         self.stdout.write(self.style.SUCCESS(f"Saved {len(articles)} Articles"))
    #     except Exception as err:
    #         self.stdout.write(self.style.ERROR(f"An error occurred while trying to save the articles\nException:\n\n{err}"))
