from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField('Имя', max_length=100, blank=True)
    city = models.CharField('Город', max_length=100, blank=True)
    status = models.CharField('Кто вы', max_length=50, blank=True)
    about = models.TextField('О себе', blank=True)

    def __str__(self):
        return self.user.username


class Subject(models.Model):

    name = models.CharField('Предмет', max_length=100, unique=True)

    def __str__(self):
        return self.name


class StudyRequest(models.Model):

    EXAM_CHOICES = [
        ('ege', 'ЕГЭ'),
        ('oge', 'ОГЭ'),
        ('uni', 'Экзамен в вузе'),
        ('other', 'Другое'),
    ]
    FORMAT_CHOICES = [
        ('online', 'Онлайн'),
        ('offline', 'Офлайн'),
        ('any', 'Любой'),
    ]
    TIME_CHOICES = [
        ('morning', 'Утро'),
        ('day', 'День'),
        ('evening', 'Вечер'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_requests')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Предмет')
    exam_type = models.CharField('Экзамен', max_length=10, choices=EXAM_CHOICES)
    exam_date = models.DateField('Дата экзамена')
    goal = models.TextField('Цель', blank=True)
    format = models.CharField('Формат', max_length=10, choices=FORMAT_CHOICES, default='any')
    time_of_day = models.CharField('Удобное время', max_length=10, choices=TIME_CHOICES)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.subject} ({self.exam_date})'


class PartnerRequest(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Ожидает ответа'),
        ('accepted', 'Принята'),
        ('declined', 'Отклонена'),
    ]

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_partner_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_partner_requests')
    study_request = models.ForeignKey(StudyRequest, on_delete=models.CASCADE, verbose_name='Запрос')
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user}  {self.to_user} ({self.status})'


class Friendship(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Ожидает ответа'),
        ('accepted', 'Друзья'),
    ]

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_requests')
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user}  {self.to_user} ({self.status})'


class Message(models.Model):

    friendship = models.ForeignKey(Friendship, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('Сообщение')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender}: {self.text[:30]}'


class StudySession(models.Model):
    
    partner_request = models.ForeignKey(PartnerRequest, on_delete=models.CASCADE, related_name='sessions')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField('Тема занятия', max_length=200)
    start_time = models.DateTimeField('Дата и время')
    link = models.URLField('Ссылка на звонок', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.topic} ({self.start_time})'