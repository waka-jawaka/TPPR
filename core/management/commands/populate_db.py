from django.core.management.base import BaseCommand
from core.models import Alternative, Person, Result, Criterion, Mark, Vector


MARKS = {
	'Житлоплоща' : [
		('Житлоплоща 60 кв. м', 2, 60),
		('Житлоплоща 75.4 кв. м', 1, 75.4),
		('Житлоплоща 45.24 кв. м', 3, 45.24),
	],
	'Наявність ремонту' : [
		('Так', None, None),
		('Ні', None, None),
	],
	'Тип будинку' : [
		('Брежневка', 2, 3),
		('Хрущевка', 4, 1),
		('Новострой', 1, 4),
		('Приватний будинок', 3, 2),
	],
	'Поверх' : [
		('1', 2, 1),
		('5', 1, 2),
		('6', 2, 1),
		('9', 2, 1),
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

CRITERIONS = (
	('Житлоплоща', 1, 'quan', 'max', 'кв. м', 'ratio', None),
	('Вартість житла', 1, 'quan', 'min', '$', 'ratio', None),
	('Віддаленість від центру', 1, 'quan', 'min', 'м', 'ratio', 2.5),
	('Поверх', 1, 'qual', None, None, 'nominal', 1),
	('Тип будинку', 1, 'qual', None, None, 'nominal', 2),
	('Наявність ремонту', 1, 'qual', None, None, 'ordinal', 4),
)


RESULTS = {
	'Person 1': [
		('House 1', 2),
		('House 2', 5),
		('House 3', 3),
		('House 4', 1),
		('House 5', 4),
	],
	'Person 2': [
		('House 1', 4),
		('House 2', 5),
		('House 3', 2),
		('House 4', 3),
		('House 5', 1),
	],
	'Person 3': [
		('House 1', 2),
		('House 2', 5),
		('House 3', 4),
		('House 4', 1),
		('House 5', 3),
	],
}


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
		for i in range(1, 6):
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

		for e in CRITERIONS:
			criterion = Criterion(
				name=e[0], rate=e[1], criterion_type=e[2], 
				optimization_type=e[3], measurement=e[4], scale=e[5], weight=e[6]
			)
			criterion.save()

	def _create_marks(self):
		criterions = Criterion.objects.all()
		for criterion in criterions:
			for v in MARKS[criterion.name]:
				mark = Mark.objects.create(
					criterion=criterion, name=v[0], rate=v[1], number=v[2])

	def _create_results(self):
		persons = Person.objects.all()
		for person in persons:
			for result in RESULTS[person.name]:
				alternative = Alternative.objects.get(name=result[0])
				Result.objects.create(
					alternative=alternative, person=person, rate=result[1])

	def _create_vectors(self):
		DATA = {
			'House 1': [
				'Житлоплоща 75.4 кв. м', 'Так', 'Новострой', '5', '25322 м', '40000 $'
			],
			'House 2': [
				'Житлоплоща 75.4 кв. м', 'Ні', 'Хрущевка', '6', '62322 м', '50000 $'
			],
			'House 3': [
				'Житлоплоща 45.24 кв. м', 'Ні', 'Новострой', '9', '25322 м', '40000 $'
			],
			'House 4': [
				'Житлоплоща 60 кв. м', 'Так', 'Приватний будинок', '1', '62322 м', '35000 $'
			],
			'House 5': [
				'Житлоплоща 45.24 кв. м', 'Так', 'Брежневка', '1', '35034 м', '50000 $'
			],
		}

		for k, v in DATA.items():
			alternative = Alternative.objects.get(name=k)
			for mark_name in v:
				mark = Mark.objects.get(name=mark_name)
				Vector.objects.create(alternative=alternative, mark=mark)

	def handle(self, *args, **options):
		self._clear_database()
		self._create_houses()
		self._create_people()
		self._create_criterions()
		self._create_marks()
		self._create_vectors()
		self._create_results()
