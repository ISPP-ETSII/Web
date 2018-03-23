"""ISPP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views


from RoomBnB import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # ex: /flats/
    path('flats', views.list, name='flatList'),
    path('flats/', views.list, name='flatList'),
    path('room/rent/<int:room_id>', views.request_rent_room, name='requestRentRoom'),
    path('requests/list', views.requests_list, name='requestsList'),
    path('requests/accept/<int:request_id>/', views.accept_request, name='acceptRequest'),
    path('requests/deny/<int:request_id>/', views.deny_request, name='denyRequest'),
    # ex: /flats/5/
    path('flats/<int:flat_id>/', views.detail, name='flatDetail'),
    path('flats/keyword=<keyword>', views.listWithKeyword, name='flatListWithKeyword'),
    path('flats/create',views.flatCreate, name='flatCreate'),
    path('profile/create',views.profileCreate, name='profileCreate'),
    path('flats/delete/<int:flat_id>/', views.flatDelete, name='flatDelete'),
    path('rooms/create/<int:flat_id>/', views.roomCreate, name='roomCreate'),
    path('rooms/<int:room_id>/', views.detailRoom, name='roomDetail'),
    path('roomReview/<int:room_id>/', views.roomReview, name='roomReview'),
    path('flatReview/<int:flat_id>/', views.flatReview, name='flatReview'),
    path('userReview/<int:user_id>/', views.userReview, name='userReview'),
    path('ownerReview/<int:user_id>/', views.userReview, name='ownerReview'),
    path('writeRoomReview/<int:room_id>/', views.writeReviewRoom, name='writeRoomReview'),
    path('writeFlatReview/<int:flat_id>/', views.writeReviewFlat, name='writeFlatReview'),
    path('writeUserReview/<int:user_id>/', views.writeReviewUser, name='writeUserReview'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('', views.base, name='base'),
    #path('', views.root, name='root'),

]