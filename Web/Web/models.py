from django.db import models
from django.db.models.fields.related import ForeignKey

# Many [videos] to one [Up]
class Up(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.TextField()
    signature = models.TextField()
    level = models.IntegerField()
    avatarUrl = models.TextField()
    followerCount = models.TextField()
    followingCount = models.TextField()

class Video(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    abstract = models.TextField()
    authorId: models.IntegerField()
    author = models.ForeignKey(Up, related_name='videos', on_delete=models.CASCADE)
    uploadTime = models.DateTimeField()
    playCount = models.IntegerField()
    commentCount = models.IntegerField()
    bulletCommentCount = models.IntegerField()
    imageUrl = models.TextField()
    like = models.TextField()
    coin = models.TextField()
    star = models.TextField()
    share = models.TextField()
    # comments: using foreign key
    # tags: using many to many field

# Many [comments] to one [Video]
class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    video = models.ForeignKey(
        Video, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()

# One [Video] to many [tags]
class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    video = models.ForeignKey(
        Video, related_name='tags', on_delete=models.CASCADE)
    tagName = models.TextField()


