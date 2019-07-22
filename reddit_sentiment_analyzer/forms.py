from django import forms

class SubredditForm(forms.Form):
    subreddit = forms.CharField(widget=forms.TextInput(attrs={'class' : 'uk-input uk-width-auto', 'placeholder': 'r/'}), label='')