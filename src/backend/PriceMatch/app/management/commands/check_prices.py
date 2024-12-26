from django.core.management.base import BaseCommand
from app.tasks import check_price_changes

class Command(BaseCommand):
    help = '检查商品价格变化'

    def handle(self, *args, **kwargs):
        self.stdout.write('开始检查价格...')
        check_price_changes()
        self.stdout.write(self.style.SUCCESS('价格检查完成')) 