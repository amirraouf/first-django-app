from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify


# Create your models here.
class Category(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(default=None)

    def __str__(self):
        return u'%s' % self.name

    def clean(self):
        return self.clean_fields()

    def get_absolute_url(self):
        self.slug = slugify(self.name)
        return reverse('category_detail', kwargs={'category_name':self.slug})

    class Meta:
        order_with_respect_to = 'name'
        verbose_name_plural = "Categories"
        db_table = 'courses_categories'


class Specialization(models.Model):
    id_S = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(default=None)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        self.slug = slugify(self.name)
        self.id_S.slug = slugify(self.id_S.name)
        return reverse('spec_detail', kwargs={'spec_name':self.slug,'category_name':self.id_S.slug})

    class Meta:
        order_with_respect_to = 'name'
        db_table = 'courses_specializations'


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, username, password, first_name,
        last_name and user type.
        :param first_name: text
        :param last_name: text
        :param username: text
        :param email: Email
        :param password: password

        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            last_name=last_name,
            first_name=first_name,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, password=password, username=username
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Person(AbstractBaseUser):
    '''
        This is the main class of customers
    '''
    username = models.CharField(max_length=80, unique=True, auto_created=r'^gocourses\d+r{5,8}$')
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(blank=False)

    USER_TYPE_CHOICES = {
        'training_center': 'Training center',
        'instructor': 'Instructor',
        'user': 'User',
    }
    about = models.CharField(default="No Information", max_length=400)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    # is_instructor = models.BooleanField(default=False)
    # is_gouser = models.BooleanField(default=True)
    # is_tcenter = models.BooleanField(default=False)
    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']

    def __str__(self):
        return self.username

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name, self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    def get_absolute_url(self):
        slug = slugify(self.username)
        return reverse('profile', kwargs={'slug':slug})

    def go_user_create(self, *args, **kwargs):
        user = Go_User.objects.create()
        user.save()


    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_admin

class Go_User(models.Model):
    person = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.IntegerField(default=None)
    mobile = models.CharField(max_length=20, default=None)
    img = models.ImageField(upload_to='static/img/profile/', default='static/img/profile/no_image.gif')

    def __str__(self):
        return self.person.username

    class Meta:
        verbose_name_plural = "Go_Users"
        db_table = "customer_go_users"


class Instructor(models.Model):
    person = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.IntegerField(default=None)
    mobile = models.CharField(max_length=20, default=None)
    img = models.ImageField(upload_to='static/img/profile/', default='static/img/profile/no_image.gif')

    def __str__(self):
        return self.person.username

    class Meta:
        verbose_name_plural = "Instructors"
        db_table = "customer_instructors"


class Training_Center(models.Model):
    person = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    training_center_name = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    logo = models.ImageField(upload_to='static/img/profile/', default='static/img/profile/no_image.gif')

    def __str__(self):
        return self.person.username

    class Meta:
        order_with_respect_to = 'training_center_name'
        db_table = 'customers_training_center'


class Training_Center_Admin(models.Model):
    admin = models.ForeignKey(Training_Center)
    name = models.CharField(max_length=60)
    email = models.EmailField()

    def __str__(self):
        return Training_Center_Admin.email


class Training_Center_Admin_Levone(models.Model):
    admin_one = models.OneToOneField(Training_Center_Admin)

    class Meta:
        db_table = 'training_center_admin_1'
        permissions = [
            ('reply_message', 'reply message'),
            ('edit_data_courses', 'edit some data of courses'),
        ]


class Training_Center_Admin_Levtwo(models.Model):
    admin_two = models.OneToOneField(Training_Center_Admin)

    class Meta:
        db_table = 'training_center_admin_2'
        permissions = [
            ('reply_message', 'reply message'),
            ('edit_data_courses', 'edit some data of courses'),
            ('add_data_courses', 'add some data of courses'),
            ('delete_data_courses', 'delete some data of courses'),
        ]


class Course_dir(models.Model):
    id_CO = models.ForeignKey(Specialization, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100)
    no_hours = models.DurationField()
    no_seats = models.IntegerField()
    description = models.CharField(max_length=300)
    price = models.IntegerField()
    certification = models.BooleanField(default=False)
    type_of_degree = models.TextField()
    date = models.DateTimeField()
    time = models.TimeField()
    featured = models.BooleanField(default=False)
    availability = models.BooleanField(default=False)
    training_center = models.ForeignKey(Training_Center, on_delete=models.CASCADE, default=None)
    user = models.ManyToManyField(Go_User, default=None)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, default=None,null=True)
    slug = models.SlugField(default=None)

    def get_absolute_url(self):
        self.slug = slugify(self.name)
        return reverse('course_detail', kwargs={'course_name':self.slug})

    def publish(self):
        self.availability = True
        self.training_center = Person.username
        self.save()

    def move_draft(self):
        self.published_date = None
        self.save()

    # def get_title(self):
    #     return "%s - %s" %(self.product.title, self.title)

    def __str__(self):
        return self.name

    class Meta:
        order_with_respect_to = 'availability'
        db_table = 'courses_courses'


class Course_Attendance_sheet(models.Model):
    person = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, blank=None, null=True)
    course = models.ManyToManyField(Course_dir, default=None, blank=None, null=True)

    def save(self, *args, **kwargs):
        super(Course_Attendance_sheet, self).save()

    def get_absolute_url(self):
        slug = slugify(self.course.name)
        return reverse('add_to_attend', kwargs={'course_name':slug})

class Course_Watch_Later(models.Model):
    person = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, blank=None)
    course = models.ManyToManyField(Course_dir, default=None, blank=None, null=True)

    def save(self,*args, **kwargs):
        super(Course_Watch_Later, self).save()

def image_upload_to(instance, filename):
    title = instance.course.name
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" %(slug, instance.pk, file_extension)
    return "img\courses\%s\%s" %(slug, new_filename)


class CourseImage(models.Model):
    course = models.ForeignKey(Course_dir)
    image = models.ImageField(upload_to=image_upload_to)

    def __str__(self):
        return self.course.name


class Like(models.Model):
    user = models.ForeignKey(Go_User)
    course = models.ForeignKey(Course_dir)
    created = models.DateTimeField(auto_now_add=True)
