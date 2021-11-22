from django.core.management.base import BaseCommand
from vacancies.models import City
import json



class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('concert_file', type=str)

    def handle(self, *args, **options):
        with open(options["concert_file"], encoding="utf-8") as jsonfile:
            json_file = json.load(jsonfile)
            for el in json_file["file"]:
                City.objects.create(city_name=el["city"])