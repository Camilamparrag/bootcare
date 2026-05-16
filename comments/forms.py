from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.TextInput(attrs={"placeholder": "Escribe un comentario...", "class": "w-full border rounded p-2"})
        }
