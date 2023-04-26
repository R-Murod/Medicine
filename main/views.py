from hashlib import md5

from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from main.forms import addQuestionform
from main.models import *
import re
import random
import requests


def get_random_number(random_len):
    random_len = int(random_len)
    a = pow(10, random_len)
    b = pow(10, random_len - 1)
    n = random.randint(b, a)
    return n


def send_message(phone, sms):
    sms_domain = 'https://smsc.kz/sys/send.php'
    sms_params = {
        'login': 'rakhmetov2718',
        'psw': '283746Mu',
        'mes': sms,
        'fmt': 3,
        'phones': phone,
    }
    r = requests.post(sms_domain, data=sms_params)
    print(r.status_code)
    print(r.json())
    print(phone)
    print(sms)


email_regex = re.compile(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
phone_regexp = re.compile(r'^77[0-9]{9}$')
iin_regexp = re.compile(r'[0-9]{12}$')


# Create your views here.
def indexHandler(request):
    user_id = request.session.get('user_id', None)
    active_user = None
    if user_id:
        active_user = SiteUser.objects.get(id=int(user_id))

    recent_post = History.objects.filter(recent_post=True)[:4]
    doctors = Doctor.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        cat = request.POST.get('category', 0)

        if email:
            subscriber = Email.objects.filter(email=email)
            if not subscriber:
                subscriber = Email()
                subscriber.email = email
                subscriber.name = name
                subscriber.cat_id = cat
                subscriber.sent_at = datetime.now()
                subscriber.save()

        data = {
            'name': name,
            'email': email,
            'message': message,
            'phone': phone,
            'cat': cat,
        }
        email_text = f'Ближайшие дни мы вам звоним'
        print(data)
        html_content = render_to_string('./mail.html')
        send_mail(data['name'] + ", спасибо за подписку!", email_text, '', [data['email']])
        return redirect('/')

    return render(request, 'index.html', {
        'user_id': user_id,
        'active_user': active_user,
        'recent_post': recent_post,
        'doctors': doctors,
        'categories': categories,
    })


def doctorHandler(request):
    user_id = request.session.get('user_id', None)
    active_user = None
    if user_id:
        active_user = SiteUser.objects.get(id=int(user_id))

    doctors = Doctor.objects.all()

    return render(request, 'doctor.html', {
        'user_id': user_id,
        'active_user': active_user,
        'doctors': doctors,
    })


def aboutHandler(request):
    user_id = request.session.get('user_id', None)
    active_user = None
    if user_id:
        active_user = SiteUser.objects.get(id=int(user_id))

    categories = Category.objects.all()

    return render(request, 'about.html', {
        'user_id': user_id,
        'active_user': active_user,
        'categories': categories,
    })


def categoryHandler(request):
    user_id = request.session.get('user_id', None)
    active_user = None
    if user_id:
        active_user = SiteUser.objects.get(id=int(user_id))

    categories = Category.objects.all()
    doctors = Doctor.objects.all()

    return render(request, 'category.html', {
        'user_id': user_id,
        'active_user': active_user,
        'categories': categories,
        'doctors': doctors,
    })


def loginHandler(request):
    post_error = ''
    if request.POST:
        login = request.POST.get('login', '')
        password = request.POST.get('password', '')
        if login and password:
            temp_hash = md5()
            temp_hash.update(password.encode())
            password_hash = temp_hash.hexdigest()

            site_user = SiteUser.objects.filter(phone=login, password=password_hash)
            if not site_user:
                site_user = SiteUser.objects.filter(email=login, password=password_hash)

            if site_user:
                site_user = site_user[0]
                request.session['user_id'] = site_user.id
                return redirect('/')
            else:
                post_error = "USER_NOT_FOUND"
        else:
            post_error = "ERROR ARGUMENTS"

    return render(request, 'login.html', {
        'post_error': post_error,
    })


def logoutHandler(request):
    request.session['user_id'] = None
    redirect('/')

    return render(request, 'logout.html', {
    })


def registerHandler(request):
    if request.POST:
        phone = request.POST.get('phone', '')
        if phone:
            if len(phone) == 11:
                site_user = SiteUser.objects.filter(phone=phone)
                if site_user:
                    new_site_user = site_user[0]
                    old_password = str(get_random_number(4))
                    print(old_password)
                    password_hash = md5()
                    password_hash.update(old_password.encode())
                    new_password = password_hash.hexdigest()

                    new_site_user.password = new_password
                    new_site_user.save()
                    message = "Код для регистрация: " + str(old_password)
                    send_message(phone, message)
                    return redirect('/')
                else:
                    new_site_user = SiteUser()
                    new_site_user.phone = phone

                    old_password = str(get_random_number(4))
                    print(old_password)
                    password_hash = md5()
                    password_hash.update(old_password.encode())
                    new_password = password_hash.hexdigest()

                    new_site_user.password = new_password
                    new_site_user.save()
                    message = "Код для регистрация: " + str(old_password)
                    send_message(phone, message)
                    return redirect('/')
            else:
                print("FORMAT ERROR")
        else:
            print("NO ARGUMENT")

    return render(request, 'register.html', {
    })


def editHandler(request):
    user_id = request.session.get('user_id', None)
    active_user = None
    post_errors = []

    if user_id:
        active_user = SiteUser.objects.get(id=int(user_id))
        if request.POST:
            last_name = request.POST.get('last_name', '')
            first_name = request.POST.get('first_name', '')
            middle_name = request.POST.get('middle_name', '')
            iin = request.POST.get('iin', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            active_password = request.POST.get('active_password', '')
            new_password = request.POST.get('new_password', '')
            new_password_repeat = request.POST.get('new_password_repeat', '')

            active_user.last_name = last_name
            active_user.first_name = first_name
            active_user.middle_name = middle_name

            if iin:
                if iin_regexp.match(iin):
                    active_user.iin = iin
                else:
                    post_errors.append("IIN_FORMAT_ERROR")
            if email:
                if email_regex.match(email):
                    email_users = SiteUser.objects.filter(email=email)
                    if email_users:
                        email_users = email_users[0]
                        if email_users.id == active_user.id:
                            pass
                        else:
                            post_errors.append("EMAIL_REGISTERED")
                    else:
                        active_user.email = email
                else:
                    post_errors.append("EMAIL_FORMAT_ERROR")
            if phone:
                if phone_regexp.match(phone):
                    phone_users = SiteUser.objects.filter(phone=phone)
                    if phone_users:
                        email_user = phone_users[0]
                        if email_user.id == active_user.id:
                            pass
                        else:
                            post_errors.append('PHONE_REGISTERED')
                    else:
                        active_user.phone = phone
                else:
                    post_errors.append('PHONE_FORMAT_ERROR')
            if active_password and new_password and new_password_repeat:
                temp_hash = md5()
                temp_hash.update(active_password.encode())
                active_password_hash = temp_hash.hexdigest()
                if active_user.password == active_password_hash:
                    if new_password == new_password_repeat:
                        new_temp_hash = md5()
                        new_temp_hash.update(new_password.encode())
                        new_password_hash = new_temp_hash.hexdigest()
                        active_user.password = new_password_hash
                    else:
                        print("NEW_PASSWORD_INCORRECT")
                else:
                    post_errors.append("ACTIVE_PASSWORD_INCORRECT")
            active_user.save()

    return render(request, 'edit.html', {
        'user_id': user_id,
        'active_user': active_user,
        'post_errors': post_errors,
    })


def addQuestion(request):
    if request.user.is_staff:
        form = addQuestionform()
        if (request.method == 'POST'):
            form = addQuestionform(request.POST)
            if (form.is_valid()):
                form.save()
                return redirect('/question')
        context = {'form': form}
        return render(request, 'addQuestion.html', context)
    else:
        return redirect('/')


def home(request):
    if request.method == 'POST':
        print(request.POST)
        questions = QuesModel.objects.all()
        score = 0
        wrong = 0
        correct = 0
        total = 0
        for q in questions:
            total += 1
            print(request.POST.get(q.question))
            print(q.ans)
            print()
            if q.ans == request.POST.get(q.question):
                score += 10
                correct += 1
            else:
                wrong += 1
        percent = score / (total * 10) * 100
        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total
        }
        return render(request, 'result.html', context)
    else:
        questions = QuesModel.objects.all()
        context = {
            'questions': questions
        }
        return render(request, 'home.html', context)
