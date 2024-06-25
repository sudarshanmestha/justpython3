from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.urls import reverse

class Course(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(upload_to="thumnails/")
    description = models.TextField()
    active = models.BooleanField(default=False)
    #price
    price = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.name 
    
    def get_absolute_url(self):
        return reverse("content:course-detail", kwargs={
            "slug": self.slug
        })    
        
    def price_display(self):
        rupees = self.price // 100
        paise = self.price % 100
        return "₹{}.{}".format(rupees, paise)        
    
    
    
class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')  
    vimeo_id = models.CharField(max_length=20)
    title = models.CharField(max_length=150)
    timeline = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    order = models.IntegerField(default=1) 
       
    class Meta:
        ordering = ["order"]
    
    def __str__(self):
        return self.title
    
    
def pre_save_course(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
    
  
def pre_save_video(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
    
pre_save.connect(pre_save_course, sender=Course)        
pre_save.connect(pre_save_video, sender=Video)         