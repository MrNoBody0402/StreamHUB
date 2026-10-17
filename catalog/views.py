from django.shortcuts import render
from .services import (
    get_media_list, get_media_details, get_media_credits, 
    get_person_details, search_media, GENRES
)

def home(request):
    query = request.GET.get('q', '').strip()
    selected_genre = request.GET.get('genre', '').lower()
    type_filter = request.GET.get('type', 'all').lower()  # 'all', 'movie', or 'tv'
    page = int(request.GET.get('page', 1))
    
    genre_id = GENRES.get(selected_genre)

    # Search mode
    if query:
        search_results = search_media(query)
        if type_filter != 'all':
            search_results = [item for item in search_results if item.get('media_type') == type_filter]
            
        context = {
            'query': query,
            'search_results': search_results,
            'type_filter': type_filter,
        }
    # Genre filter mode
    elif selected_genre and genre_id:
        movies = []
        shows = []
        
        if type_filter in ['all', 'movie']:
            movies = get_media_list(media_type="movie", page=page, genre_id=genre_id)
        if type_filter in ['all', 'tv']:
            shows = get_media_list(media_type="tv", page=page, genre_id=genre_id)

        context = {
            'selected_genre': selected_genre,
            'type_filter': type_filter,
            'movies': movies,
            'shows': shows,
            'current_page': page,
            'next_page': page + 1,
        }
    # Default Home view
    else:
        trending_movies = []
        popular_movies = []
        trending_shows = []
        popular_shows = []
        hero_item = None

        if type_filter in ['all', 'movie']:
            trending_movies = get_media_list(media_type="movie", category="trending", page=page)
            popular_movies = get_media_list(media_type="movie", category="popular", page=page)
            
        if type_filter in ['all', 'tv']:
            trending_shows = get_media_list(media_type="tv", category="trending", page=page)
            popular_shows = get_media_list(media_type="tv", category="popular", page=page)

        # Set hero banner item
        if trending_movies:
            hero_item = trending_movies[0]
            hero_type = 'movie'
        elif trending_shows:
            hero_item = trending_shows[0]
            hero_type = 'tv'
        else:
            hero_type = 'movie'

        context = {
            'hero_item': hero_item,
            'hero_type': hero_type,
            'type_filter': type_filter,
            'trending_movies': trending_movies[1:] if (hero_item and hero_type == 'movie') else trending_movies,
            'popular_movies': popular_movies,
            'trending_shows': trending_shows[1:] if (hero_item and hero_type == 'tv') else trending_shows,
            'popular_shows': popular_shows,
            'current_page': page,
            'next_page': page + 1,
        }
        
    return render(request, 'catalog/home.html', context)

def watch(request, media_type, tmdb_id):
    details = get_media_details(media_type, tmdb_id)
    cast = get_media_credits(media_type, tmdb_id)
    season = int(request.GET.get('season', 1))
    episode = int(request.GET.get('episode', 1))

    episodes_list = []
    if media_type == 'tv' and details:
        seasons_data = details.get('seasons', [])
        current_season_info = next((s for s in seasons_data if s.get('season_number') == season), None)
        ep_count = current_season_info.get('episode_count', 10) if current_season_info else 10
        episodes_list = list(range(1, ep_count + 1))

    if media_type == 'movie':
        servers = [
            {'name': 'Server 1 (VidLink)', 'url': f"https://vidlink.pro/movie/{tmdb_id}"},
            {'name': 'Server 2 (SmashyStream)', 'url': f"https://player.smashy.stream/movie/{tmdb_id}"},
            {'name': 'Server 3 (AutoEmbed)', 'url': f"https://player.autoembed.cc/embed/movie/{tmdb_id}"},
            {'name': 'Server 4 (2Embed)', 'url': f"https://www.2embed.cc/embed/{tmdb_id}"},
            {'name': 'Server 5 (VidSrc VIP)', 'url': f"https://vidsrc.vip/embed/movie/{tmdb_id}"},
        ]
    else:
        servers = [
            {'name': 'Server 1 (VidLink)', 'url': f"https://vidlink.pro/tv/{tmdb_id}/{season}/{episode}"},
            {'name': 'Server 2 (SmashyStream)', 'url': f"https://player.smashy.stream/tv/{tmdb_id}?s={season}&e={episode}"},
            {'name': 'Server 3 (AutoEmbed)', 'url': f"https://player.autoembed.cc/embed/tv/{tmdb_id}/{season}/{episode}"},
            {'name': 'Server 4 (2Embed)', 'url': f"https://www.2embed.cc/embedtv/{tmdb_id}&s={season}&e={episode}"},
            {'name': 'Server 5 (VidSrc VIP)', 'url': f"https://vidsrc.vip/embed/tv/{tmdb_id}/{season}/{episode}"},
        ]

    context = {
        'details': details,
        'cast': cast,
        'servers': servers,
        'media_type': media_type,
        'season': season,
        'episode': episode,
        'episodes_list': episodes_list,
    }
    return render(request, 'catalog/watch.html', context)

def actor_detail(request, person_id):
    person, filmography = get_person_details(person_id)
    context = {
        'person': person,
        'filmography': filmography,
    }
    return render(request, 'catalog/actor.html', context)

def watchlist(request):
    return render(request, 'catalog/watchlist.html')