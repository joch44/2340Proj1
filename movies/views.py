from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, ReviewReport
from django.contrib.auth.decorators import login_required


def index(request):

  search_response = request.GET.get('search')
  if search_response:
    movies = Movie.objects.filter(name__icontains = search_response)
  else:
    movies = Movie.objects.all()

  return render(request, "movies/index.html", {'template_data' : {
        'title': 'Movies',
        'movies': movies
      }})

def show(request, id):
  movies = Movie.objects.get(id=id)
  reviews = Review.objects.filter(movie=movies).exclude(reported_by=request.user)

  return render(request, "movies/show.html", {'template_data' : {
      'title' : movies.name,
      'movie' : movies,
      'reviews': reviews
    }})

@login_required
def create_review(request, id):
  if request.method == 'POST' and request.POST['comment'] != '':
    movie = Movie.objects.get(id=id)
    review = Review()
    review.comment = request.POST['comment']
    review.movie = movie
    review.user = request.user
    review.save()
    return redirect("movies.show", id=id)
  else:
    return redirect("movies.show", id=id)

@login_required
def edit_review(request, id, review_id):
  review = get_object_or_404(Review, id=review_id)
  if request.user != review.user:
    return redirect("movies.show", id=id)
  if request.method == 'GET':
    t = {}
    t['title'] = 'Edit Review'
    t['review'] = review
    return render(request, "movies/edit_review.html", {'template_data' : t})
  elif request.method == 'POST':
    review = Review.objects.get(id=review_id)
    review.comment = request.POST['comment']
    review.save()
    return redirect("movies.show", id=id)
  return redirect("movies.show", id=id)

@login_required
def delete_review(request, id, review_id):
  review = get_object_or_404(Review, id=review_id)
  review.delete()
  return redirect("movies.show", id=id)

@login_required
def report_review(request, id, review_id):
  review = get_object_or_404(Review, id=review_id)
  if request.user == review.user:
    return redirect("movies.show", id=id)
  if request.method == "POST":
    if request.POST['reason'] == "":
      return redirect("movies.show", id=id)
    report = ReviewReport()
    report.reported_by = request.user
    report.review =  review
    report.reason = request.POST['reason']
    report.save()
    review = Review.objects.get(id=review_id)
    review.reported_by.add(request.user)
    review.save()
    return redirect("movies.show", id=id)

  t = {}
  t['title'] = 'Report Review'
  t['review'] = review
  return render(request, "movies/report_review.html", {'template_data' : t})
