from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required


def add(request, id):
  get_object_or_404(Movie, id=id)
  cart = request.session.get('cart', {})
  cart[id] = request.POST['quantity']
  request.session['cart'] = cart
  return redirect("cart.index")

def clear(request):
  request.session['cart'] = {}
  return redirect('cart.index')

def index(request):
  total = 0
  movies = []
  cart = request.session.get('cart', {})
  movie_ids = list(cart.keys())
  if movie_ids != []:
    movies = Movie.objects.filter(id__in=movie_ids)
    total = calculate_cart_total(cart, movies)

  t = {}
  t['title'] = "My Cart"
  t['movies_in_cart'] = movies
  t['cart_total'] = total

  return render(request, 'cart/index.html', {'template_data' : t})

@login_required
def purchase(request):
  cart = request.session.get('cart', {})
  movie_ids = list(cart.keys())
  if movie_ids == []:
    return redirect("cart.index")

  movies = Movie.objects.filter(id__in = movie_ids)
  cart_total = calculate_cart_total(cart, movies)

  order = Order()
  order.user = request.user
  order.total = cart_total
  order.save()
  for m in movies:
    item = Item()
    item.movie = m
    item.price = m.price
    item.order = order
    item.quantity = cart[str(m.id)]

  request.session['cart'] = {}
  t = {}
  t['title'] = "Purchase Confirmation"
  t['order_id'] = order
  return render(request, 'cart/purchase.html',
    {'template_data': t})
