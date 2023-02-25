from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin.models import LogEntry
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.widgets import AdminFileWidget


admin.site.site_header = _('Salma Style')
admin.site.index_title = _('Salma Style Administration')
admin.site.site_title = _('Salma Style Administration')


# Register your models here.
# LogEntry.objects.all().delete()


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(
                f'<a href="{image_url}" target="_blank">'
                f'<img src="{image_url}" alt="{file_name}" width="150" height="150" '
                f'style="object-fit: cover;"/> </a>')
        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        return mark_safe(u''.join(output))



class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'image_tag', 'email', 'name', 'phone', 'is_admin', 'created_at', 'updated_at')
    list_display_links = ('id', 'email', 'name', 'phone')
    list_filter = ('is_admin', 'created_at', 'updated_at')
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'phone', 'password', 'device_token')}),
        ('Personal info', {'fields': ('name', 'profile',)}),
        ('Permissions', {'fields': ('is_active', 'is_admin',)}),
        ('Dates', {'fields': ('created_at', 'updated_at',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'device_token', 'profile', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'name', 'phone')
    ordering = ('id', 'email', 'name', 'phone', 'created_at', 'updated_at')
    list_per_page = 10
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ()
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }
# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'barcode_number', 'barcode_img', 'product', 'nutritions', 'ingredients', 'brand', 'created_at', 'updated_at']
    list_display_links = ['id', 'status', 'barcode_number', 'barcode_img', 'product', 'nutritions', 'ingredients', 'brand']
    search_fields = ('status', 'barcode_number', 'brand', 'user__name')
    ordering = ('status', 'barcode_number', 'brand', 'created_at', 'updated_at')
    list_per_page = 5
    filter_horizontal = ()
    list_filter = ['status', 'user', 'created_at', 'updated_at']
    readonly_fields = ('created_at', 'updated_at')
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }


# @admin.register(Stores)
# class StoresAdmin(admin.ModelAdmin):
#     list_display = ['id', 'product', 'name', 'country', 'currency', 'price', 'created_at', 'updated_at']
#     search_fields = ('product__barcode_number', 'name', 'country', 'currency', 'price')
#     ordering = ('id', 'product', 'name', 'country', 'currency', 'price', 'created_at', 'updated_at')
#     list_per_page = 10
#     filter_horizontal = ()


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['id',  'heading', 'description', 'language', 'created_at', 'updated_at']
    search_fields = ('heading',)
    ordering = ('id', 'heading', 'created_at', 'updated_at')
    list_per_page = 10
    list_filter = ('language',)
    filter_horizontal = ()
    readonly_fields = ('created_at', 'updated_at')



@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'heading', 'description', 'language', 'created_at', 'updated_at']
    search_fields = ('heading',)
    ordering = ('id', 'heading', 'created_at', 'updated_at')
    list_per_page = 10
    list_filter = ('language',)
    filter_horizontal = ()
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ['id', 'heading', 'description', 'created_at', 'updated_at']
    search_fields = ('heading',)
    ordering = ('id', 'heading', 'created_at', 'updated_at')
    list_per_page = 10
    filter_horizontal = ()
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CountryCode)
class CountryCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'country_code', 'created_at', 'updated_at']
    list_display_links = ['id', 'country_code']
    search_fields = ('country_code',)
    ordering = ('id', 'country_code', 'created_at', 'updated_at')
    list_per_page = 10
    filter_horizontal = ()
    readonly_fields = ('created_at', 'updated_at')


# @admin.register(UserProductImages)
# class UserProductImagesAdmin(admin.ModelAdmin):
#     list_display = ['id', 'status', 'barcode_number', 'product', 'nutrition_facts', 'ingredients', 'created_at', 'created_by']
#     search_fields = ('barcode_number', 'product_image', 'nutrition_facts_image', 'ingredients_image')
#     ordering = ('id','barcode_number', 'product_image', 'nutrition_facts_image', 'ingredients_image', 'created_at', 'created_by')
#     list_filter = ('created_by', 'status')
#     list_per_page = 5
#     filter_horizontal = ()
#     readonly_fields = ('product', 'nutrition_facts', 'ingredients')


@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'sender', 'title', 'message', 'recieved_date', 'created_at', 'updated_at']
    list_display_links = ['id', 'product', 'title', 'message']
    search_fields = ('title',)
    ordering = ('id','sender', 'title', 'message', 'recieved_date', 'created_at', 'updated_at')
    list_per_page = 10
    filter_horizontal = ()
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }