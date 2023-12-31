from django.contrib import admin
from django.contrib.admin.helpers import ActionForm
from django.urls import path
from django.shortcuts import render   
from django.http import HttpResponseRedirect

from app_telegram.models import (
        TGUser, 
        University,
        Course,
        CourseMessage,
        Feedback,
        FeedbackData,
)
    
class TGUserAdmin(admin.ModelAdmin):
    list_display = ['tg_id', 'created']
    list_filter = ['created']
    search_fields = ['tg_id']
    save_on_top = True

class UniversityAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'fullname']
    list_display_links = ['name', 'fullname']
    list_filter = ['name',]
    search_fields = ['name', ]
    save_on_top = True
    ordering = ['id',]
    
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'fullname','university']
    list_display_links = ['name', 'fullname']
    list_filter = ['university']
    search_fields = ['name', 'university']
    save_on_top = True  
    ordering = ['id','university']  
               
class CoursesMsgAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'course', 'name', 'message','language','step',]
    list_display_links = ['name', 'message']
    list_filter = ['course', 'name']
    search_fields = ['name', 'course']
    save_on_top = True  
    save_as = True
    ordering = ['id', 'course']
    readonly_fields = ['id']
    fieldsets = [
        (
            None,
            {
                "fields": ['id', 'course', 'name', 'message','language','step'],
            },
        ),
    ]
    
    actions = ['duplicate_with_input_form']
    @admin.action
    def duplicate_with_input_form(self, request, queryset):
        
        for obj in queryset:
                        # Create a new object with the same attributes and the new value
                        CourseMessage.objects.create(
                            id       = None,
                            name     = obj.name,        
                            message  = obj.message, 
                            language = obj.language,
                            step     = obj.step,    
                            course   = obj.course,  
                        )
                        
        self.message_user(request, f'{queryset.count()} objects duplicated.')
        return HttpResponseRedirect(request.get_full_path())
        
    duplicate_with_input_form.short_description = "Duplicate selected objects"
            
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'message','language','step']
    list_display_links = ['name', 'message']
    list_filter = ['name','language']
    search_fields = ['name']
    save_on_top = True  
    ordering = ['id']  

class FeedbackDataAdmin(admin.ModelAdmin):
    list_display = ['created', 'userid', 'username', 'language',
                    'clarity','clarity_comment',
                    'usefulness','usefulness_comment',
                    'support','support_comment']
    list_display_links = ['created', 'userid', 'username']
    list_filter = ['userid','username','created']
    search_fields = ['username', 'userid']
    save_on_top = True  
    ordering = ['id']  

admin.site.register(TGUser, TGUserAdmin)
admin.site.register(University, UniversityAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseMessage, CoursesMsgAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(FeedbackData, FeedbackDataAdmin)