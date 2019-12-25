from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Alternative(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.name


class Criterion(models.Model):
	TYPES = (
		('quan', 'качественный'),
		('qual', 'количественный'),
	)

	OPTIMIZATION_TYPES = (
		('max', 'Максимум'),
		('min', 'Минимум'),
	)

	SCALE_TYPES = (
		('nominal', 'Наименований'),
		('ordinal', 'Порядковая'),
		('interval', 'Интервалов'),
		('ratio', 'Отношений'),
		('difference', 'Разностей'),
		('absolute', 'Абсолютная'),
	)

	name = models.CharField(max_length=100, unique=True)
	rate = models.PositiveIntegerField()
	weight = models.FloatField(
		validators = [MinValueValidator(0)],
		null=True, blank=True
	)
	criterion_type = models.CharField(max_length=4, choices=TYPES)
	optimization_type = models.CharField(max_length=3, choices=OPTIMIZATION_TYPES, null=True, blank=True)
	measurement = models.CharField(max_length=20, null=True, blank=True)	
	scale = models.CharField(max_length=10, choices=SCALE_TYPES)

	def __str__(self):
		return self.name


class Mark(models.Model):
	criterion = models.ForeignKey('Criterion', on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	rate = models.PositiveIntegerField(null=True, blank=True)
	number = models.FloatField(
		validators = [MinValueValidator(0)], null=True, blank=True
	)
	normalized = models.FloatField(
		null=True, blank=True,
		validators = [MinValueValidator(0), MaxValueValidator(1)],
	)

	def __str__(self):
		return "Оценка \"{}\" по критерию \"{}\"".format(self.name, self.criterion.name)

	def normalize(self):
		marks_by_criterion = Mark.objects.filter(criterion=self.criterion)
		min_mark = marks_by_criterion.aggregate(models.Min('number')).get('number__min')
		max_mark = marks_by_criterion.aggregate(models.Max('number')).get('number__max')
		if min_mark  == max_mark:
			return
		if self.number is None:
			return

		if self.criterion.optimization_type == 'max' or self.criterion.criterion_type == 'qual':
			self.normalized = (self.number - min_mark) / (max_mark - min_mark)
			self.save()
		elif self.criterion.optimization_type == 'min':
			self.normalized = (self.number - max_mark) / (min_mark - max_mark)
			self.save()


class Person(models.Model):
	name = models.CharField(max_length=100, unique=True)
	rate = models.PositiveIntegerField()
	alternatives = models.ManyToManyField(Alternative, through='Result')

	def __str__(self):
		return self.name


class Result(models.Model):
	person = models.ForeignKey('Person', on_delete=models.CASCADE)
	alternative = models.ForeignKey('Alternative', on_delete=models.CASCADE)
	rate = models.PositiveIntegerField(null=True, blank=True)
	weight = models.FloatField(
		validators = [MinValueValidator(0)],
		null=True, blank=True
	)

	def __str__(self):
		return "{} - {}".format(str(self.person), str(self.alternative))


class Vector(models.Model):
	alternative = models.ForeignKey('Alternative', on_delete=models.CASCADE)
	mark = models.ForeignKey('Mark', on_delete=models.CASCADE)

	def __str__(self):
		return "{} - {}".format(str(self.alternative), str(self.mark))
