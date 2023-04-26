import random
import uuid

from django.db import models
from datetime import datetime


# Create your models here.
class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class CategoryQuestion(BaseModel):
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name


class Category(models.Model):
    name = models.CharField(max_length=200, blank=True)
    logo_icon = models.CharField(max_length=200, blank=True)
    text = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    mini_desc = models.CharField(max_length=200, blank=True)
    desc = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.mini_desc + " --> " + self.category.name


class Doctor(models.Model):
    name = models.CharField(max_length=200, blank=True)
    profession = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to='upload', blank=True)
    twitter = models.CharField(max_length=200, blank=True)
    whatsapp = models.CharField(max_length=200, blank=True)
    facebook = models.CharField(max_length=200, blank=True)
    instagram = models.CharField(max_length=200, blank=True)
    desc = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class History(models.Model):
    title = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    posted_date = models.DateTimeField(default=datetime.now())
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=True, null=True)
    logo = models.ImageField(upload_to='upload', blank=True)
    logo1 = models.ImageField(upload_to='upload', blank=True)
    desc1 = models.CharField(max_length=200, blank=True)
    desc2 = models.CharField(max_length=200, blank=True)
    desc3 = models.CharField(max_length=200, blank=True)
    twitter = models.CharField(max_length=200, blank=True)
    whatsapp = models.CharField(max_length=200, blank=True)
    facebook = models.CharField(max_length=200, blank=True)
    instagram = models.CharField(max_length=200, blank=True)
    recent_post = models.BooleanField(default=False)
    recent_post_photo = models.ImageField(upload_to='upload', blank=True)

    def __str__(self):
        return self.title


class SiteUser(models.Model):
    last_name = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200, blank=True)
    middle_name = models.CharField(max_length=200, blank=True)
    iin = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.last_name + ' ' + self.phone


class Email(models.Model):
    name = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    sent_at = models.CharField(max_length=200, blank=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.name} --> {self.email} -- > {self.sent_at}'


class Question(BaseModel):
    category = models.ForeignKey(CategoryQuestion, related_name='category', on_delete=models.CASCADE, blank=True, null=True)
    question = models.CharField(max_length=200, blank=True)
    marks = models.IntegerField(default=5)

    def __str__(self):
        return self.question

    def get_answers(self):
        answer_objs = list(Answer.objects.filter(question=self))
        random.shuffle(answer_objs)
        data = []
        for answer_obj in answer_objs:
            data.append({
                'answer': answer_obj.answer,
                'is_correct': answer_obj.is_correct
            })
        return data


class Answer(BaseModel):
    question = models.ForeignKey(Question, related_name='question_answer', on_delete=models.CASCADE, blank=True, null=True)
    answer = models.CharField(max_length=200, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer


class QuesModel(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Категория ")
    question = models.CharField(max_length=200, null=True, verbose_name="Сұрақ: ")
    op1 = models.CharField(max_length=200, null=True, verbose_name="Сұрақ: option1")
    op2 = models.CharField(max_length=200, null=True, verbose_name="Сұрақ: option2")
    op3 = models.CharField(max_length=200, null=True, verbose_name="Сұрақ: option3")
    op4 = models.CharField(max_length=200, null=True, verbose_name="Сұрақ: option4")
    ans = models.CharField(max_length=200, null=True, verbose_name="дұрыс жауап: option1/2/3 болмаса option4")

    def __str__(self):
        return self.question