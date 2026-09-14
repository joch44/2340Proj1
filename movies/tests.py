from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Movie, Review, ReviewReport


class ReviewReportTests(TestCase):
  def setUp(self):
    self.author = User.objects.create_user('author', password='pw')
    self.reporter = User.objects.create_user('reporter', password='pw')
    self.other = User.objects.create_user('other', password='pw')
    self.movie = Movie.objects.create(name='M', price=5, description='d', image='movie_images/x.jpg')
    self.review = Review.objects.create(comment='hidden-after-report', movie=self.movie, user=self.author)
    self.show_url = reverse('movies.show', kwargs={'id': self.movie.id})
    self.report_url = reverse('movies.report_review', kwargs={'id': self.movie.id, 'review_id': self.review.id})

  def report_as_reporter(self):
    self.client.force_login(self.reporter)
    self.client.post(self.report_url, {'reason': 'spam'})
    self.client.logout()

  def assertSeesReview(self, user, visible):
    if user:
      self.client.force_login(user)
    response = self.client.get(self.show_url)
    self.assertEqual(response.status_code, 200)
    (self.assertContains if visible else self.assertNotContains)(response, 'hidden-after-report')
    self.client.logout()

  def test_reporter_no_longer_sees_review(self):
    self.report_as_reporter()
    self.assertEqual(ReviewReport.objects.count(), 1)
    self.assertSeesReview(self.reporter, False)

  def test_other_users_still_see_reported_review(self):
    self.report_as_reporter()
    self.assertSeesReview(self.author, True)
    self.assertSeesReview(self.other, True)

  def test_anonymous_users_still_see_reported_review(self):
    self.report_as_reporter()
    self.assertSeesReview(None, True)
