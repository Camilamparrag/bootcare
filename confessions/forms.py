from django import forms
from .models import AnonymousConfession, AnonymousComment


class ConfessionForm(forms.ModelForm):
    class Meta:
        model = AnonymousConfession
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"placeholder": "Comparte lo que callas...", "rows": 4, "class": "w-full border rounded p-2"})
        }


class AnonymousCommentForm(forms.ModelForm):
    class Meta:
        model = AnonymousComment
        fields = ["text"]
        widgets = {
            "text": forms.TextInput(attrs={"placeholder": "Comentario anónimo...", "class": "w-full border rounded p-2"})
        }
