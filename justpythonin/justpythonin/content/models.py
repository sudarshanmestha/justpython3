from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.urls import reverse


# class Level(models.Model):
#     name = models.CharField(max_length=100)
    
#     def __str__(self):
#         self.name
        

class Course(models.Model):
    LEVEL_CHOICES = [
        ('B', 'Basic'),
        ('I', 'Intermediate'),
        ('A', 'Advanced'),
    ]
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(upload_to="thumnails/")
    description = models.TextField()
    active = models.BooleanField(default=False)
    date = models.DateField()
    #price
    price = models.PositiveIntegerField(default=1)
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES, default='B')
    
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
          
    def get_level_display(self):
        # Method to return human-readable value of level
        for level_choice in self.LEVEL_CHOICES:
         if self.level == level_choice[0]:  # level_choice[0] is the code, level_choice[1] is the name
            return level_choice[1]  # Return the human-readable name
        return None 
        
# class Chapter(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="chapters")
#     title = models.CharField(max_length=200)
#     number = models.PositiveIntegerField()
    
#     def __str__(self):
#         return f"Chapter {self.number}: {self.title}"
    
#     class Meta:
#         unique_together = ['course', 'number']
#         ordering = ['number']    
    
class Video(models.Model):
    # chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='videos')
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
    
    def get_absolute_url(self):
        return reverse("content:video-detail", kwargs={
            "video_slug": self.slug,
            "slug": self.course.slug
            })
    
    
def pre_save_course(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
    
  
def pre_save_video(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
    
pre_save.connect(pre_save_course, sender=Course)        
pre_save.connect(pre_save_video, sender=Video)         