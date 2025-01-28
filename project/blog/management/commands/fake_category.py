from blog.models import Category

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'insert the category datas'

    def handle(self, *args, **options):
        Category.objects.all().delete()

        categories = [
            # 'sports', 'technologies', 'medical', 'learning', 'cryptocurrency'
        ]

        for category_list in categories:
            Category.objects.create(name=category_list)

        self.stdout.write(self.style.SUCCESS('category insert successfully'))
