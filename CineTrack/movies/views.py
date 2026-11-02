from urllib import request

from django.core.serializers import python
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Movie
from .forms import MovieForm
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth import login
from django.core.mail import send_mail
from .utils import generate_otp, get_otp_expiry
import time

def home(request):
    query = request.GET.get('q', '')
    if query:
        movies = Movie.objects.filter(
        Q(title__icontains=query) |
        Q(genre__icontains=query)
    )
    else:
        movies = Movie.objects.all()
    return render(
        request,
        'movies/home.html',
    {
        'movies': movies,
        'query': query
    }
     )

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request,
    'movies/movie_detail.html',
    {'movie': movie}
    )
@login_required
def add_movie(request):
        if request.method == 'POST':
         form = MovieForm(request.POST)
         if form.is_valid():
                form.save()
                messages.success(request, 'Movie added successfully!')
                return redirect('home')
        else:
            form = MovieForm()
        return render(request, 'movies/add_movie.html', {'form': form})

@login_required
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)

        if form.is_valid():
         form.save()
         messages.success(request, 'Movie updated successfully!')
         return redirect('home')

    else:
        form = MovieForm(instance=movie)

    return render(
        request,
        'movies/edit_movie.html',
        {
            'form': form,
            'movie': movie
        }
    )

@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        movie.delete()
        messages.success(request, 'Movie deleted successfully!')
        return redirect('home')

    return render(
        request,
        'movies/delete_movie.html',
        {'movie': movie}
    )


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            otp = generate_otp()

            request.session['registration_otp'] = otp
            request.session['otp_attempts'] = 0
            request.session['registration_user_id'] = user.id
            request.session['otp_expiry'] = get_otp_expiry()

            send_mail(
                'CineTrack Email Verification',
                f'Your verification OTP is {otp}. It expires in 5 minutes.',
                None,
                [user.email],
                fail_silently=False,
            )

            return redirect('verify_otp')

    else:
        form = RegistrationForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )
def verify_otp(request):

    # Handle GET request
    if request.method != 'POST':
        return render(request, 'registration/verify_otp.html')

    # Get OTP entered by the user
    entered_otp = request.POST.get('otp', '').strip()

    # Retrieve OTP details from session
    stored_otp = request.session.get('registration_otp')
    expiry_time = request.session.get('otp_expiry')
    user_id = request.session.get('registration_user_id')
    attempts = request.session.get('otp_attempts', 0)

    # Check whether OTP exists
    if not stored_otp or not expiry_time:

        return render(
            request,
            'registration/verify_otp.html',
            {'error': 'OTP expired or not found. Please register again.'}
        )

    # Check maximum attempts
    if attempts >= 3:

        return render(
            request,
            'registration/verify_otp.html',
            {'error': 'Maximum attempts exceeded. Please register again.'}
        )

    # Check OTP expiry
    import time

    if time.time() > expiry_time:

        request.session.pop('registration_otp', None)
        request.session.pop('registration_user_id', None)
        request.session.pop('otp_expiry', None)
        request.session.pop('otp_attempts', None)

        return render(
            request,
            'registration/verify_otp.html',
            {'error': 'OTP has expired. Please register again.'}
        )

    # Compare entered OTP with stored OTP
    if entered_otp != stored_otp:

        attempts += 1
        request.session['otp_attempts'] = attempts

        # If maximum attempts reached
        if attempts >= 3:

            request.session.pop('registration_otp', None)
            request.session.pop('registration_user_id', None)
            request.session.pop('otp_expiry', None)
            request.session.pop('otp_attempts', None)

            return render(
                request,
                'registration/verify_otp.html',
                {'error': 'Maximum attempts exceeded. Please register again.'}
            )

        remaining = 3 - attempts

        return render(
            request,
            'registration/verify_otp.html',
            {'error': f'Incorrect OTP. {remaining} attempts remaining.'}
        )

    # If OTP is correct, find the inactive user
    from django.contrib.auth import get_user_model

    User = get_user_model()

    user = User.objects.filter(
        id=user_id,
        is_active=False
    ).first()

    if user is None:

        return render(
            request,
            'registration/verify_otp.html',
            {'error': 'Registration not found. Please register again.'}
        )

    # Activate user account
    user.is_active = True
    user.save(update_fields=['is_active'])

    # Clear OTP session data
    request.session.pop('registration_user_id', None)
    request.session.pop('registration_otp', None)
    request.session.pop('otp_expiry', None)
    request.session.pop('otp_attempts', None)

    # Redirect to login
    return redirect('login')





def resend_otp(request):

    # Allow only POST requests
    if request.method != 'POST':
        return redirect('verify_otp')

    # Check whether a registration is pending
    user_id = request.session.get('registration_user_id')

    if not user_id:
        return redirect('register')

    # Get the user model
    from django.contrib.auth import get_user_model
    import time

    User = get_user_model()

    # Find the inactive user
    user = User.objects.filter(
        id=user_id,
        is_active=False
    ).first()

    if user is None:
        return redirect('register')

    # Check OTP resend limit
    now = time.time()

    resend_times = request.session.get('otp_resend_times', [])

    # Keep requests made within the last 10 minutes
    resend_times = [
        timestamp for timestamp in resend_times
        if now - timestamp < 600
    ]

    # Allow maximum 3 resend requests
    if len(resend_times) >= 3:

        request.session['otp_resend_times'] = resend_times

        return render(
            request,
            'registration/verify_otp.html',
            {
                'error': 'Resend limit reached. Please try again after 10 minutes.'
            }
        )

    # Record the current resend request
    resend_times.append(now)

    request.session['otp_resend_times'] = resend_times

    # Generate a new OTP
    otp = generate_otp()

    # Store new OTP details
    request.session['registration_otp'] = otp
    request.session['otp_expiry'] = get_otp_expiry()
    request.session['otp_attempts'] = 0

    # Send OTP through email
    send_mail(
        'CineTrack Email Verification',
        f'Your new verification OTP is {otp}. It expires in 5 minutes.',
        None,
        [user.email],
        fail_silently=False,
    )

    # Redirect to OTP verification page
    return redirect('verify_otp')

