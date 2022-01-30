from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


STATUS = ((0, "Draft"), (1, "Published"))


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=195, unique=True)
    slug = models.SlugField(max_length=195, unique=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="main_posts"
    )
    recipe_image = CloudinaryField('image', default='placeholder')
    highlight = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    loves = models.ManyToManyField(
        User, related_name='main_loves', blank=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.recipe_name

    def number_of_loves(self):
        return self.loves.count()


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")
    display_name = models.CharField(max_length=125)
    email = models.EmailField()
    comment_text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"Comment {self.comment_text} by {self.display_name}"
