from django import forms


class ReviewForm(forms.Form):
    name = forms.CharField(
        max_length=128,
        label='Имя',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'name',
                'aria-describedby': 'nameHelp',
                'name': 'name',
                'data-cip-id': 'name',
                'placeholder': 'Представьтесь',
            })
    )
    content = forms.CharField(
        label='Содержание',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'content',
                'name': 'description',
                'placeholder': 'Содержание',
                'rows': '',
                'cols': ''
            })
    )
    rating = forms.ChoiceField(
        label='',
        choices=(('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5)),
        widget=forms.RadioSelect(
            attrs={
                'class': 'form-check-input'
            }
        )
    )
