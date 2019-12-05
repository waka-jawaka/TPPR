from django.core.management.base import BaseCommand
from core.models import Alternative, Person, Result, Criterion, Mark

class Command(BaseCommand):
	args = '<foo bar ...>'
	help = 'our help string comes here'

	def _clear_database(self):
		Result.objects.all().delete()
		Mark.objects.all().delete()
		Criterion.objects.all().delete()
		Person.objects.all().delete()
		Alternative.objects.all().delete()


	def _create_houses(self):
		self.houses = []
		for i in range(1, 7):
			house_name = 'House ' + str(i)
			house = Alternative(name=house_name)
			house.save()
			self.houses.append(house)

	def _create_people(self):
		self.people = []
		for i in range(1, 4):
			person_name = 'Person ' + str(i)
			person = Person(name=person_name, rate=i)
			person.save()
			self.people.append(person)

	def _create_criterions(self):

		DATA = (
			('Житлоплоща', 1, 'quan', 'max', 'кв. м', 'ratio'),
			('Вартість житла', 1, 'quan', 'min', '$', 'ratio'),
			('Віддаленість від центру', 1, 'quan', 'min', 'м', 'ratio'),
			('Поверх', 1, 'qual', None, None, 'nominal'),
			('Тип будинку', 1, 'qual', None, None, 'nominal'),
			('Наявність ремонту', 1, 'qual', None, None, 'ordinal'),
		)

		for e in DATA:
			criterion = Criterion(
				name=e[0], rate=e[1], criterion_type=e[2], 
				optimization_type=e[3], measurement=e[4], scale=e[5]
			)
			criterion.save()

	def _create_marks(self):
		DATA = {
			'Житлоплоща' : [
				('Житлоплоща 60 кв. м', 2, 60),
				('Житлоплоща 75.4 кв. м', 1, 75.4),
				('Житлоплоща 45.24 кв. м', 3, 45.24),
			],
			'Наявність ремонту' : [
				('Так', 1, 1),
				('Ні', 2, 0),
			],
			'Тип будинку' : [
				('Брежневка', 2, 0),
				('Хрущевка', 4, 0),
				('Новострой', 1, 0),
				('Приватний будинок', 3, 0),
			],
			'Поверх' : [
				('1', 2, 0),
				('5', 1, 0),
				('6', 2, 0),
				('9', 1, 0),
			],
			'Віддаленість від центру' : [
				('25322 м', 1, 25322),
				('62322 м', 3, 62322),
				('35034 м', 2, 35034),
			],
			'Вартість житла' : [
				('40000 $', 2, 40000),
				('50000 $', 3, 50000),
				('35000 $', 1, 35000),
			],
		}

		criterions = Criterion.objects.all()
		for criterion in criterions:
			for v in DATA[criterion.name]:
				mark = Mark.objects.create(
					criterion=criterion, name=v[0], rate=v[1], number=v[2])

	def handle(self, *args, **options):
		self._clear_database()
		self._create_houses()
		self._create_people()
		self._create_criterions()
		self._create_marks()
