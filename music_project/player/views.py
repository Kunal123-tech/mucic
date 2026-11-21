from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Song

def home(request):
    songs = Song.objects.all().order_by('-uploaded_at')
    return render(request, 'player/home.html', {'songs': songs})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'player/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'player/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        artist = request.POST.get('artist')
        audio_file = request.FILES.get('audio_file')
        if title and artist and audio_file:
            Song.objects.create(
                title=title,
                artist=artist,
                audio_file=audio_file,
                uploaded_by=request.user
            )
            return redirect('dashboard')

    user_songs = Song.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
    return render(request, 'player/dashboard.html', {'songs': user_songs})

@login_required
def delete_song(request, song_id):
    song = get_object_or_404(Song, id=song_id, uploaded_by=request.user)
    song.delete()
    return redirect('dashboard')

def music_player(request, song_id=None):
    all_songs = list(Song.objects.all().order_by('-uploaded_at'))
    
    if not all_songs:
        return render(request, 'player/music_player.html', {'song': None, 'all_songs': []})

    if song_id:
        current_song = get_object_or_404(Song, id=song_id)
    else:
        current_song = all_songs[0]

    # Calculate Previous and Next songs for navigation
    current_index = all_songs.index(current_song)
    prev_song = all_songs[current_index - 1] if current_index > 0 else all_songs[-1]
    next_song = all_songs[current_index + 1] if current_index < len(all_songs) - 1 else all_songs[0]

    context = {
        'song': current_song,
        'all_songs': all_songs,
        'prev_song': prev_song,
        'next_song': next_song,
    }
    return render(request, 'player/music_player.html', context)