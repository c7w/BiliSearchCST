from django.db import models
from django.db.models.fields.related import ForeignKey

# Many [videos] to one [Up]
class Up(models.Model):
    id = models.IntegerField(primary_key=True, db_index=True)
    username = models.TextField(db_index=True)
    signature = models.TextField(db_index=True)
    level = models.IntegerField()
    avatarUrl = models.TextField()
    followerCount = models.TextField()
    followingCount = models.TextField()

class Video(models.Model):
    id = models.IntegerField(primary_key=True, db_index=True)
    title = models.TextField(db_index=True)
    abstract = models.TextField(db_index=True)
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
    id = models.BigAutoField(primary_key=True, db_index=True)
    video = models.ForeignKey(
        Video, related_name='comments', on_delete=models.CASCADE, db_index=True)
    content = models.TextField(db_index=True)

# One [Video] to many [tags]
class Tag(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True)
    video = models.ForeignKey(
        Video, related_name='tags', on_delete=models.CASCADE, db_index=True)
    tagName = models.TextField(db_index=True)


