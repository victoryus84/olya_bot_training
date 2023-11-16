from django.contrib import admin

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
    list_display = ['course', 'name', 'message','language','step']
    list_display_links = ['name', 'message']
    list_filter = ['name', 'course']
    search_fields = ['name', 'course']
    save_on_top = True  
    ordering = ['id', 'course']  
        
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