from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from . import util

from .models import *


def active_list(request):
    active = Item.objects.filter(is_active=True)
    items = util.get_obj_with_bid(active)
    categories = Category.objects.all()
    is_active = 'Active'
    return render(request, "auctions/active.html",{'items': items, 'categories': categories, 'is_active': is_active})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        username = username[0].upper()+username[1:]
        password = request.POST["pswrd"]
        user = authenticate(request, username=username, password=password)
    
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect('auctions:active_list')
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return redirect('auctions:active_list')


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        username = username[0].upper()+username[1:]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["pswrd"]
        confirmation = request.POST["cpswrd"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect('auctions:active_list')
    else:
        return render(request, "auctions/register.html")

def all_list(request):
    All = Item.objects.all()
    items = util.get_obj_with_bid(All)
    categories = Category.objects.all()
    is_active='All'
    return render(request, "auctions/active.html",{'items': items, 'categories': categories, 'is_active': is_active})


def watch_list(request):
    user = request.user 
    arr = user.watch_list.all()
    items = util.get_obj_with_bid(arr)
    categories = Category.objects.all()
    message=''
    if not arr:
        message = 'No items in the watchlist'
    is_active='Watch_list'
    return render(request, "auctions/active.html",{'items': items, 'message': message, 'categories': categories, 'is_active': is_active})

def add_to_watch_list(request, item_id, cur_bid_id):
    item = Item.objects.get(id=item_id)
    user = request.user 
    item.watchlist_users.add(user)
    item.save()
    cur_bid = Bid.objects.get(id=cur_bid_id)
    comments = item.comments.all()
    present = True 
    return render(request,'auctions/entry.html',{'item':item, 'cur_bid':cur_bid, 'comments': comments, 'present': present, 'success': 'Added to watch list'})

def remove_from_watch_list(request, item_id, cur_bid_id):
    item = Item.objects.get(id=item_id)
    user = request.user
    item.watchlist_users.remove(user)
    item.save()
    cur_bid = Bid.objects.get(id=cur_bid_id)
    comments = item.comments.all()
    present = False
    return render(request,'auctions/entry.html',{'item':item, 'cur_bid':cur_bid, 'comments': comments, 'present': present, 'success': 'Removed from watch list'})

def create(request):
    if request.method=="POST":
         title = request.POST['title']
         title = title[0].upper()+title[1:]
         category = request.POST.get('category','none')
         if category:
             category = category[0].upper()+category[1:]
         start_bid= request.POST['start_bid']
         image_url = request.POST['image_url']
         description = request.POST['description']
         user=request.user
         category_obj = Category.objects.filter(name=category)
         if not category_obj:
             category_obj = Category(name=category)
             category_obj.save()
         else:
             category_obj = category_obj.first()
         if image_url:
             item = Item(title=title,description=description,img=image_url,category=category_obj,creator=user)
         else:
             item = Item(title=title,description=description,category=category_obj,creator=user)
         item.save()
         bid=Bid(user=user,item=item,bid_price=start_bid)
         bid.save()
         return redirect('auctions:active_list')
    return render(request,'auctions/create.html')

def entry(request, item_id):
    item = Item.objects.get(id=item_id)
    cur_bid = util.max_bid(item)
    user = request.user
    present = False 
    if user.is_authenticated:
        present = util.user_present_in_watch_list(item,user)
    comments = item.comments.all()
    return render(request,'auctions/entry.html',{'item': item, 'cur_bid': cur_bid, 'comments': comments, 'present': present})

def bid(request, item_id, cur_bid_id):
    if request.method=='GET':
        redirect('auctions:entry',item_id)
    bid_price = int(request.POST['bid'])
    item = Item.objects.get(id=item_id)
    cur_bid=Bid.objects.get(id=cur_bid_id)
    user = request.user
    present = False 
    if user.is_authenticated:
        present = util.user_present_in_watch_list(item,user)
    comments = item.comments.all()
    if bid_price<=cur_bid.bid_price:
        return render(request,'auctions/entry.html',{'item':item, 'cur_bid':cur_bid, 'comments': comments, 'present': present, 'message': 'You bid should be larger than current price'})
    bid = Bid(user=user,item=item,bid_price=bid_price)
    bid.save()
    return render(request,'auctions/entry.html',{'item': item, 'cur_bid': bid, 'comments': comments, 'present': present})

def close(request, item_id):
    item = Item.objects.get(id=item_id)
    item.is_active=False 
    item.save()
    return redirect('auctions:entry',item_id)

def add_comment(request, item_id):
    item = Item.objects.get(id=item_id)
    user = request.user 
    if request.method=='POST':
        comment = request.POST['comment']
        comment= comment[0].upper()+comment[1:]
    comment_obj = Comment(user=user,item=item,comment=comment)
    comment_obj.save()
    return redirect('auctions:entry',item_id)
    
def Categories(request, category_id, is_active):
    category_obj = Category.objects.get(id=category_id)
    if is_active=='All':
        items = category_obj.items.all()
    elif is_active=='Active':
        items = category_obj.items.filter(is_active=True)
    else:
        user = request.user
        items = user.watch_list.filter(category=category_obj)
    items = util.get_obj_with_bid(items)
    message = ''
    if not items:
        message = 'No items in this category'
    categories = Category.objects.all()
    return render(request, "auctions/active.html",{'items': items, 'categories': categories, 'is_active': is_active, 'message': message})
