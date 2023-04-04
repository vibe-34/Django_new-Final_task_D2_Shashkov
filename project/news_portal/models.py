from django.db import models
from django.contrib.auth.models import User  # при работе со встроенной моделью User, её нужно импортировать
from django.db.models import Sum


class Author(models.Model):
    """ Класс автор, с полями authorUser - связь один к одному с встроенной моделью User,
        ratingAuthor - рейтинг автора"""
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)  # рейтинг автора, по умолчанию = 0

    def update_rating(self):
        """ Метод обновления рейтинга автора. """
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        # К связанной модели post применяем функцию aggregate, которая применяет функцию Sum к полю rating.
        # Функция aggregate суммирует все значения поля rating у модели Post, связанной с автором
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    """ Модель 'категория' с полем name, имеющее уникальное значение и длиной не более 64 символов."""
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    """ Модель 'пост' с полем author и связью один ко многим с моделью Author """
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'               # Новость
    ARTICLE = 'AR'            # Статья
    CATEGORY_CHOICES = (      # Выбор категории
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)  # поле выбора
    dateCreation = models.DateTimeField(auto_now_add=True)  # автоматическое добавления даты создания поста
    postCategory = models.ManyToManyField(Category, through='PostCategory')  # поле категория сообщения, связанное
    # с моделью Category и промежуточным полем PostCategory
    title = models.CharField(max_length=128)
    text = models.TextField()  # текст для пользователей не ограничен по количеству символов
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:123]} ...'


class PostCategory(models.Model):
    """ Промежуточная модель. """
    postThrougt = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrougt = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    """ Модель комментариев. """
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

