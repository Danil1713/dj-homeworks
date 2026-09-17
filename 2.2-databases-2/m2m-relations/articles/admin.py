from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from .models import Article, Scope, Tag


class ScopeInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        if any(self.errors):
            return

        main_count = 0

        for form in self.forms:
            if not form.cleaned_data:
                continue

            if form.cleaned_data.get('DELETE', False):
                continue

            if form.cleaned_data.get('is_main', False):
                main_count += 1

        if main_count != 1:
            raise ValidationError(
                'У статьи должен быть ровно один основной раздел.'
            )


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormSet
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at')
    inlines = [ScopeInline]