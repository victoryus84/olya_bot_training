
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import MyForm
from .models import CourseMessage

@require_POST
def duplicate_with_input_view(request, queryset):
    messages.success(request, "The action was performed successfully.")