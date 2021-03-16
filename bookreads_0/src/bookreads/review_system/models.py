from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.template.defaultfilters import slugify
from PIL import Image
from io import BytesIO
from django.core.files import File

# Create your models here.

def image_upload_filter(instance, filename):
    print(type(instance))
    ext = filename.split('.')[1]
    filename = str(instance.serial_no) + '.' + ext
    return 'images/%s' % (filename)


def turn_tags_to_list(book):
    tagList = []
    for field in book._meta.fields:
        if field.name == 'serial_no' or field.name == 'title' or field.name == 'author' or field.name == 'slug' or field.name == 'cover_photo':
            continue
        if field.value_from_object(book) == True:
            tagList.append(field.name[2:])
    return tagList


def make_thumbnail(image, size=(250, 400)):
    im = Image.open(image)
    im = im.convert('RGB')
    im = im.resize(size)
    # im.thumbnail(size)
    thumb_io = BytesIO()
    im.save(thumb_io, 'JPEG', quality=85)
    thumbnail = File(thumb_io,name=image.name)
    return thumbnail

class Book(models.Model):
    serial_no = models.AutoField(primary_key=True)
    # isbn_no = models.CharField(max_length=13, unique=True, null=False)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=20)
    slug = models.SlugField(null=True, blank=True)
    tags = models.ManyToManyField(to='Tag', blank=True)
    cover_photo = models.ImageField(null=True, blank=True, upload_to=image_upload_filter, default='')

    def as_json(self):
        dict = {
            'serial_no': self.serial_no,
            'title': self.title,
            'author': self.author,
            'slug': self.slug,
            'tags': str(self.tags),
            'cover_photo': self.cover_photo.name
        }
        return dict


    # Automatically create a slugfield, on save()
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.cover_photo:
            try:
                this = Book.objects.get(serial_no=self.serial_no)
                if this.cover_photo != self.cover_photo:
                    this.cover_photo.delete()
            except: pass
            self.cover_photo = make_thumbnail(self.cover_photo, size=(550, 800))
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return self.title



class Tag(models.Model):
    data = models.CharField(max_length=20, unique=True, null=False, blank=False)

    def __str__(self):
        return str(self.data)
        


class Review(models.Model):
    serial_no = models.AutoField(primary_key=True)
    contents = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(default=now)

    def as_json(self):
        if self.parent:
            dict = {
                'serial_no': self.serial_no,
                'contents': self.contents,
                'user': self.user.username,
                'book': self.book.as_json(),
                'parent': self.parent.as_json(),
                'timestamp': self.timestamp
            }
        else:
            dict = {
                'serial_no': self.serial_no,
                'contents': self.contents,
                'user': self.user.username,
                'book': self.book.as_json(),
                'parent': None,
                'timestamp': self.timestamp
            }
        return dict

    def __str__(self):
        displayed_review = ''
        if self.parent:
            displayed_review = '[Reply] '
        displayed_review = displayed_review + self.user.get_full_name() + self.contents[:20]
        return displayed_review


