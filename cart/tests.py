from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from movies.models import Movie
from .models import Order


class PurchaseTests(TestCase):
  def test_purchase_items_show_on_orders_page(self):
    user = User.objects.create_user('buyer', password='pw')
    movie = Movie.objects.create(name='Inception', price=7, description='d', image='movie_images/x.jpg')
    self.client.force_login(user)
    self.client.post(reverse('cart.add', kwargs={'id': movie.id}), {'quantity': '2'})
    self.client.get(reverse('cart.purchase'))

    order = Order.objects.get(user=user)
    self.assertEqual(order.item_set.count(), 1)
    self.assertEqual(order.item_set.get().quantity, 2)

    response = self.client.get(reverse('accounts.orders'))
    self.assertContains(response, 'Inception')
    self.assertContains(response, 'href="%s"' % reverse('movies.show', kwargs={'id': movie.id}))
