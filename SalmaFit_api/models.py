from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None):
        """
        Creates and saves a User with the given email, name, phone and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, password=None):
        """
        Creates and saves a superuser with the given email, name, phone and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            name=name,
            phone=phone,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name=_('Email'),
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    phone = models.CharField(max_length=20, unique=True, verbose_name=_('Phone'))
    profile = models.ImageField(upload_to='profile', null=True, blank=True, verbose_name=_('Profile'))
    device_token = models.CharField(max_length=500, null=True, blank=True, verbose_name=_('Device Token'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    is_admin = models.BooleanField(default=False, verbose_name=_('Is Admin'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone',]

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.profile:
            return mark_safe('<img src="{}" width="100" height="100"/>'.format(self.profile.url))
        return None
    image_tag.short_description = 'Profile'
    image_tag.allow_tags = True


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CountryCode(BaseModel):
    country_code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.country_code

    class Meta:
        verbose_name = _('Country Code')
        verbose_name_plural = _('Country Codes')


class Products(BaseModel):
    STATUS_CHOICES = [
        ("Approved", 'Approved'),
        ("Rejected", 'Rejected'),
        ("Pending", 'Pending'),
        ("Not Clear Photos", 'Not Clear Photos'),
        ("Occasionally", 'Occasionally'),
        ("Rejected While Dieting", 'Rejected While Dieting'),
    ]
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pending')
    barcode_number = models.CharField(unique=True, max_length=100, help_text="Barcode Number Can Not Be Blank")
    title = models.CharField(max_length=100, null=True, blank=True)
    عنوان = models.CharField(max_length=100, null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)
    نامتجاری = models.CharField(max_length=100, null=True, blank=True)
    barcode_image = models.ImageField(max_length=200, upload_to='user_images/barcode_image')
    product_image = models.ImageField(max_length=200, upload_to='user_images/product_image')
    nutrition_facts_image = models.ImageField(max_length=200, upload_to='user_images/nutrition_facts_image')
    ingredients_image = models.ImageField(max_length=200, upload_to='user_images/ingredients_image')
    review = models.TextField(max_length=1000, null=True, blank=True)
    مرور = models.TextField(max_length=1000, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='users', help_text="User Can Not Be Blank")
    last_update = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.barcode_number

    def barcode_img(self):
        if self.barcode_image:
            return mark_safe('<img src="{}" width="110" height="110"/>'.format(self.barcode_image.url))
        return None
    barcode_img.short_description = 'Barcode image'
    barcode_img.allow_tags = True

    def product(self):
        if self.product_image:
            return mark_safe('<img src="{}" width="110" height="110"/>'.format(self.product_image.url))
        return None
    product.short_description = 'Product image'
    product.allow_tags = True

    def nutritions(self):
        if self.nutrition_facts_image:
            return mark_safe('<img src="{}" width="110" height="110"/>'.format(self.nutrition_facts_image.url))
        return None
    nutritions.short_description = 'Nutrition facts image'
    nutritions.allow_tags = True

    def ingredients(self):
        if self.ingredients_image:
            return mark_safe('<img src="{}" width="110" height="110"/>'.format(self.ingredients_image.url))
        return None
    ingredients.short_description = 'Ingredients image'
    ingredients.allow_tags = True

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


# class Stores(BaseModel):
#     product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='stores')
#     name = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)
#     currency = models.CharField(max_length=100)
#     price = models.CharField(max_length=100)
#     link = models.URLField(max_length=500, null=True, blank=True)
#     last_update = models.DateTimeField(auto_now=True)


#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = _('Store')
#         verbose_name_plural = _('Stores')


# class UserProductImages(BaseModel):
#     class Meta:
#         verbose_name = _('User Product Image')
#         verbose_name_plural = _('User Product Images')

#     STATUS_CHOICES = [
#         ("Pending", 'Pending'),
#         ("Not Clear Photos", 'Not Clear Photos'),
#     ]
#     barcode_number = models.CharField(max_length=100, null=True, blank=True)
#     status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pending')
#     product_image = models.ImageField(max_length=200, upload_to='user_images/product_image')
#     nutrition_facts_image = models.ImageField(max_length=200, upload_to='user_images/nutrition_facts_image')
#     ingredients_image = models.ImageField(max_length=200, upload_to='user_images/ingredients_image')

#     def product(self):
#         return mark_safe('<img src="{}" width="140" height="140"/>'.format(self.product_image.url))
#     product.short_description = 'Product image'
#     product.allow_tags = True

#     def nutrition_facts(self):
#         return mark_safe('<img src="{}" width="140" height="140"/>'.format(self.nutrition_facts_image.url))
#     nutrition_facts.short_description = 'Nutrition facts image'
#     nutrition_facts.allow_tags = True

#     def ingredients(self):
#         return mark_safe('<img src="{}" width="140" height="140"/>'.format(self.ingredients_image.url))
#     ingredients.short_description = 'Ingredients image'
#     ingredients.allow_tags = True


class AboutUs(BaseModel):
    LANG_CHOICES = [
        ("English", 'English'),
        ("فارسی", 'فارسی'),
    ]
    language = models.CharField(max_length=100, choices=LANG_CHOICES, default='English', verbose_name=_('Language'))
    heading = models.CharField(max_length=100, verbose_name=_('Heading'))
    description = models.TextField(max_length=1000, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('About Us')
        verbose_name_plural = _('About Us')


class TermsAndConditions(BaseModel):
    LANG_CHOICES = [
        ("English", 'English'),
        ("فارسی", 'فارسی'),
    ]
    language = models.CharField(max_length=100, choices=LANG_CHOICES, default='English', verbose_name=_('Language'))
    heading = models.CharField(max_length=100, verbose_name=_('Heading'))
    description = models.TextField(max_length=1000, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Term And Condition')
        verbose_name_plural = _('Terms And Conditions')


class PrivacyPolicy(BaseModel):
    heading = models.CharField(max_length=200, verbose_name=_('Heading'))
    description = models.TextField(max_length=4000, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Privacy Policy')
        verbose_name_plural = _('Privacy Policies')


class Notifications(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sender_notification')
    recipient = models.ManyToManyField(User, related_name='recipient_notification')
    title = models.CharField(max_length=100)
    عنوان = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(max_length=1000)
    پیام = models.TextField(max_length=1000, null=True, blank=True)
    product_image = models.ImageField(upload_to='notification_image')
    barcode = models.CharField(max_length=100)
    recieved_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    def product(self):
        if self.product_image:
            return mark_safe('<img src="{}" width="110" height="110"/>'.format(self.product_image.url))
        return None
    product.short_description = 'Product image'
    product.allow_tags = True
