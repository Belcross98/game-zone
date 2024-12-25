from django import forms

class FeedbackForm(forms.Form):

    RATING_CHOICES = ((i, i) for i in range(1, 11))
    rating = forms.ChoiceField(choices=RATING_CHOICES)

class SearchForm(forms.Form):
    searchField = forms.CharField(label='search for games',max_length=20,required=False)
