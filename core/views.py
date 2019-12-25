from django.shortcuts import render

from .models import Mark, Alternative, Vector, Criterion


def quality_criterions_have_range():
	urls = []
	marks = Mark.objects.all()
	for mark in marks:
		if mark.number == None:
			urls.append({
				'link': 'http://127.0.0.1:8000/admin/core/mark/{}/change/'.format(mark.id),
				'mark': mark,
			})
	return urls


def basic_decision(request):
	alternatives = Alternative.objects.all()
	criterions = Criterion.objects.all()
	
	marks = {}
	for alternative in alternatives:
		vectors = Vector.objects.filter(alternative=alternative)
		marks[alternative] = vectors

	urls = quality_criterions_have_range()
	quality_check = True if len(urls) == 0 else False

	context = {
		'alternatives': alternatives,
		'marks': marks,
		'quality_check': quality_check,
		'quality_urls': urls,
		'criterions': criterions,
	}

	return render(request, 'core/basic_decision.html', context)



def paretto(alternatives, marks):
	res_alternatives = alternatives[::]
	res_marks = marks.copy()
	for alt1 in alternatives:
		for alt2 in alternatives:
			if alt1 != alt2:
				if marks[alt1][0].mark.rate <= marks[alt2][0].mark.rate and \
					marks[alt1][1].mark.rate <= marks[alt2][1].mark.rate and \
					marks[alt1][2].mark.rate <= marks[alt2][2].mark.rate and \
					marks[alt1][3].mark.rate <= marks[alt2][3].mark.rate and \
					marks[alt1][4].mark.rate <= marks[alt2][4].mark.rate and \
					marks[alt1][5].mark.rate <= marks[alt2][5].mark.rate:
						res_alternatives.remove(alt2)
						del res_marks[alt2]
	return res_alternatives, res_marks


def is_normalized(marks):
	for item in marks.values():
		for vector in item:
			if vector.mark.normalized == None:
				return False
	return True


def normalize(marks):
	for item in marks.values():
		for vector in item:
			vector.mark.normalize()


def weights_check():
	urls = []
	for criterion in Criterion.objects.all():
		if criterion.weight == None:
			urls.append({
				'url': 'http://127.0.0.1:8000/admin/core/criterion/{}/change/'.format(criterion.id),
				'name': criterion.name
			})
	return urls


def make_convolution(marks):
	results = {}
	for alternative in marks.keys():
		conv = 0
		for vector in marks[alternative]:
			conv += vector.mark.normalized * vector.mark.criterion.weight
		results[alternative] = conv
	return results


def paretto_view(request):
	alternatives = Alternative.objects.all()
	
	marks = {}
	for alternative in alternatives:
		vectors = Vector.objects.filter(alternative=alternative)
		marks[alternative] = vectors

	p_alternatives, p_marks = paretto(alternatives, marks)

	context = {
		'alternatives': alternatives,
		'marks': marks,
		'p_alternatives': p_alternatives,
		'p_marks': p_marks
	}

	return render(request, 'core/basic_decision_1.html', context)


def normalized_view(request):
	alternatives = Alternative.objects.all()
	
	marks = {}
	for alternative in alternatives:
		vectors = Vector.objects.filter(alternative=alternative)
		marks[alternative] = vectors

	normalize(marks)
	is_norm = is_normalized(marks)

	p_alternatives, p_marks = paretto(alternatives, marks)
	context = {
		'alternatives': alternatives,
		'marks': marks,
		'p_alternatives': p_alternatives,
		'p_marks': p_marks,
		'is_normalized': is_norm,
	}

	return render(request, 'core/basic_decision_2.html', context)


def weights_view(request):
	alternatives = Alternative.objects.all()
	
	marks = {}
	for alternative in alternatives:
		vectors = Vector.objects.filter(alternative=alternative)
		marks[alternative] = vectors

	alternatives, marks = paretto(alternatives, marks)
	criterions = weights_check()

	context = {
		'alternatives': alternatives,
		'marks': marks,
		'weights_check': False if len(criterions) != 0 else True,
		'weights_urls': criterions
	}

	return render(request, 'core/basic_decision_3.html', context)


def convolution_view(request):
	alternatives = Alternative.objects.all()
	
	marks = {}
	for alternative in alternatives:
		vectors = Vector.objects.filter(alternative=alternative)
		marks[alternative] = vectors

	alternatives, marks = paretto(alternatives, marks)
	results = make_convolution(marks)

	context = {
		'alternatives': alternatives,
		'marks': marks,
		'results': results
	}

	return render(request, 'core/basic_decision_4.html', context)
