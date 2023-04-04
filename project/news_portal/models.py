from django.db import models
from django.contrib.auth.models import User  # при работе со встроенной моделью, её нужно импортировать
from django.db.models import Sum


class Author(models.Model):
    """ Класс автор с полями User - связь один к одному, rating"""
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)  # поле со связью один к одному и встроенной моделью User
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):  # метод обновления рейтинга автора
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    """ Модель 'категория' с полем name, имеющее уникальное значение."""
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # author со связью один ко многим с моделью Author

    NEWS = 'NW'  # Новость
    ARTICLE = 'AR'  # Статья
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)  # поле с выбором
    dateCreation = models.DateTimeField(auto_now_add=True)  # автоматическое добавления даты создания поста
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'


class PostCategory(models.Model):
    postThrougt = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrougt = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

