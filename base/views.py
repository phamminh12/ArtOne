from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Picture, Comment, Genre, User, Like
from .forms import PictureForm, UserForm, MyUserCreationForm

from django.views.decorators.csrf import csrf_protect, csrf_exempt

# from more_itertools import chunked
from math import ceil

# Create your views here.
# m > f > v > u

# @csrf_protect
@csrf_exempt
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else: 
            messages.error(request, 'Username OR Password does not exist')
    
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


@csrf_exempt
def registerPage(request):
    page = 'register'
    form = MyUserCreationForm()

    if request.method=='POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #dữ liệu trên form vào bộ nhớ tạm (chưa lưu trên csdl)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    context = {'form': form, 'page': page}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    pictures = Picture.objects.filter(
        Q(genre__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    genres = Genre.objects.all()
    context = {'pictures': pictures, 'genres': genres}
    return render(request, 'base/home.html', context)


def discover(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    pictures = Picture.objects.filter(
        Q(genre__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    groups = [pictures[i:i+4] for i in range(0, len(pictures), 4)]
    genres = Genre.objects.all()
    context = {'pictures': pictures, 'genres': genres, 'groups': groups}
    return render(request, 'base/discover.html', context)


def news(request):
    return render(request, 'base/news.html')

def blog(request):
    return render(request,'base/blog.html')

# @login_required(login_url='login')
@csrf_exempt
def picture(request, pk):
    picture = Picture.objects.get(id=pk)
    picture_comments = picture.comment_set.all()
    # participant

    if request.method == 'POST':
        comment = Comment.objects.create(
            user = request.user,
            picture = picture, 
            body = request.POST.get('body')
        )
        return redirect('picture', pk=picture.id)
    context = {'picture': picture, 'picture_comments': picture_comments}
    return render(request, 'base/picture.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    pictures = user.picture_set.all()
    total_likes = 0
    for picture in pictures:
        total_likes += picture.likes.count()
    picture_comments = user.comment_set.all()
    genres = Genre.objects.all()
    context = {'user': user, 'pictures': pictures,
               'picture_comments': picture_comments, 'genres': genres, 'total_likes': total_likes}
    return render(request, 'base/profile.html', context)
    
@csrf_exempt
@login_required(login_url='login')
def createPicture(request):
    form = PictureForm()
    genres = Genre.objects.all()
    if request.method == 'POST':
        genre_name = request.POST.get('genre')
        genre, created = Genre.objects.get_or_create(name=genre_name)
        form = PictureForm(request.POST, request.FILES)
        # if form.is_valid():
        #     picture = form.save(commit=False)
        #     picture.host = request.user
        #     picture.image.save('post_images/' + form.image.name, form.image)
        #     picture.save()
        #     return redirect('home')
        
        Picture.objects.create(
            host = request.user,
            genre = genre,
            name = request.POST.get('name'),
            image = request.FILES.get('image'),
            description = request.POST.get('description')
        )
        return redirect('discover')

    context = {'form': form, 'genres': genres}
    return render(request, 'base/picture_form.html', context)


@csrf_exempt
@login_required(login_url='login')
def updatePicture(request, pk):
    picture = Picture.objects.get(id=pk)
    form = PictureForm(instance=picture)
    genres = Genre.objects.all()
    if request.user != picture.host:
        return HttpResponse('You are not allowed here!!')
    
    # lỗi nhận số thứ tự của trường genre thay vì tên
    # if request.method == 'POST':
    #     genre_name = request.POST.get('genre')
    #     genre, created = Genre.objects.get_or_create(name=genre_name)

    #     picture.name = request.POST.get('name')
    #     picture.genre = genre
    #     if 'image' in request.FILES:
    #         picture.image.delete()
    #         picture.image = request.FILES['image']  
    #     else:
    #         picture.image = picture.image  # Giữ nguyên tệp hình ảnh cũ
    #     picture.description = request.POST.get('description')
    #     picture.save()
    #     return redirect('home')
    
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES, instance=picture)
        genre_name = request.POST.get('genre')
        genre, created = Genre.objects.get_or_create(name=genre_name)
        picture.name = request.POST.get('name')
        picture.genre = genre
        picture.description = request.POST.get('description')
        if 'image' in request.FILES:
            picture.image.delete()
            picture.image = request.FILES['image']  
        else:
            picture.image = picture.image
        picture.save()
        return redirect('discover')
    context = {'form': form, 'genres': genres, 'picture': picture}
    return render(request, 'base/picture_form.html',context)


@csrf_exempt
@login_required(login_url='login')
def deletePicture(request, pk):
    picture = Picture.objects.get(id=pk)

    if request.user != picture.host:
        return HttpResponse('You are not allowed here!')
    
    if request.method == 'POST':
        picture.delete()
        return redirect('discover')
    return render(request, 'base/delete.html', {'obj': picture})


@csrf_exempt
@login_required(login_url='login')
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.user != comment.user:
        return HttpResponse('You are not allowed here!')
    
    if request.method == 'POST':
        comment.delete()
        return redirect('picture', comment.picture.id)
    return render(request, 'base/delete.html', {'obj': comment})


@csrf_exempt
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', user.id)
        
    context = {'form': form}
    return render(request, 'base/update-user.html', context)


@csrf_exempt
@login_required(login_url='login')
def like_picture_home(request, pk):
    picture = Picture.objects.get(id=pk)
    user = request.user
    if request.method == 'POST':
        if request.user in picture.likes.all():
            picture.likes.remove(user)
        else:
            picture.likes.add(user)
    return redirect('home')


@csrf_exempt
@login_required(login_url='login')
def like_picture_detail(request, pk):
    picture = Picture.objects.get(id=pk)
    # like = Like.objects.get(id=pk)
    user = request.user
    if request.method == 'POST':
        if request.user in picture.likes.all():
            picture.likes.remove(user)
        else:
            picture.likes.add(user)
    return redirect('picture', pk=pk)

# @login_required(login_url='login')
# def like_picture_detail(request, pk):
#     picture = Picture.objects.get(id=pk)
#     user = request.user
#     if request.method == 'POST':
#         if request.user in picture.likes.all():
#             picture.likes.remove(user)
#             likes_count = picture.likes.count() - 1
#         else:
#             picture.likes.add(user)
#             likes_count = picture.likes.count() + 1
#     response_data = {'likes_count': likes_count}

#     # Thêm URL chuyển hướng vào response_data
#     response_data['redirect_url'] = reverse('picture', args=[pk])

#     return JsonResponse(response_data)
#     # return JsonResponse({'likes_count':likes_count})