from django import forms


class QualitiveFieldsForm(forms.Form):
	improvement_yes = forms.CharField(label='Ремонт: так', max_length=100)
	improvement_no = forms.CharField(label='Ремонт: ні', max_length=100)

	house_type_br = forms.CharField(label='Брежневка', max_length=100)
	house_type_hr = forms.CharField(label='Хрущевка', max_length=100)
	house_type_novo = forms.CharField(label='Новострой', max_length=100)
	house_type_priv = forms.CharField(label='Приватний будинок', max_length=100)
