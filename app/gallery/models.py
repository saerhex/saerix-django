from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth import get_user_model
from hurry.filesize import size as convert_size
from hurry.filesize import verbose
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import re


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Publication(models.Model):
    user = models.ForeignKey(User,
                             related_name='publications',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=50, db_index=True)
    description = models.CharField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag,
                                  blank=True,
                                  related_name='publications')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class PublicationImage(models.Model):
    publication = models.ForeignKey(Publication,
                                    related_name="images",
                                    on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=False, blank=False)
    thumbnail = ImageSpecField(source='image',
                               processors=[ResizeToFill(150, 150)],
                               format='JPEG',
                               options={'quality': 60})
    filesize = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.image.name

    def set_title(self):
        self.title = re.split(r'\.', self.image.name)[0][:50]

    def calculate_filesize(self):
        self.filesize = convert_size(self.image.size, system=verbose)

    def save(self, *args, **kwargs):
        self.calculate_filesize()
        self.set_title()
        super(PublicationImage, self).save(*args, **kwargs)


class Commentary(models.Model):
    publication = models.ForeignKey(Publication,
                                    related_name='commentaries',
                                    on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             related_name='commentaries',
                             on_delete=models.CASCADE)
    text = RichTextField(max_length=5000)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"commentary on {self.publication.title} by {self.user}"

