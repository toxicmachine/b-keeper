import datetime
import os
import sys

from django.core.management.base import BaseCommand
from pages.models import KeeperObject


PROJECT_ROOT = '/home/rust/PycharmProjects/B-keeper/'
sys.path.insert(0, PROJECT_ROOT)


class Command(BaseCommand):
    help = 'Run folder rotation based on settings.'
    def handle(self, *args, **options):
        for keeper_object in KeeperObject.objects.all():
            current_date = datetime.date.today()

            # Формируем имя файла с добавлением текущей даты
            filename = f'/home/rust/{keeper_object.name}_file_{current_date}.txt'

            # Создаем пустой файл с заданным именем
            with open(filename, 'w') as file:
                pass