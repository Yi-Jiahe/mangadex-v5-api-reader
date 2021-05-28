from django import forms
from .tags import tags

class TitleSearch(forms.Form):
    title = forms.CharField(label='Title')


class AdvancedSearch(forms.Form):
    title = forms.CharField(label='Title', required=False)
    # authors = forms.CharField(label='Authors', required=False)
    # artists = forms.CharField(label='Artists', required=False)
    year = forms.IntegerField(label='Year of release', required=False)
    includedTags = forms.MultipleChoiceField(label='Tags', choices=[(tags[tag], tag) for tag in tags.keys()], required=False)