from django.shortcuts import render
from django.http import JsonResponse
from .services import (
    get_media_list, get_media_details, get_media_credits, 
    get_media_recommendations, get_person_details, search_media, GENRES
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
    recommendation_data = get_media_recommendations(media_type, tmdb_id)
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
            {'name': 'Server 2 (2Embed)', 'url': f"https://www.2embed.cc/embed/{tmdb_id}"},
            {'name': 'Server 3 (VidSrc.me)', 'url': f"https://vidsrc.me/embed/movie/{tmdb_id}"},
        ]
    else:
        servers = [
            {'name': 'Server 1 (VidLink)', 'url': f"https://vidlink.pro/tv/{tmdb_id}/{season}/{episode}"},
            {'name': 'Server 2 (2Embed)', 'url': f"https://www.2embed.cc/embedtv/{tmdb_id}&s={season}&e={episode}"},
            {'name': 'Server 3 (VidSrc.me)', 'url': f"https://vidsrc.me/embed/tv/{tmdb_id}/{season}/{episode}"},
        ]

    context = {
        'details': details,
        'cast': cast,
        'recommendations': recommendation_data['results'] if recommendation_data else [],
        'recommendations_has_more': recommendation_data['total_pages'] > 1 if recommendation_data else False,
        'recommendations_error': recommendation_data is None,
        'continue_watching_item': {
            'id': tmdb_id,
            'title': (details.get('title') or details.get('name') or 'Untitled') if details else 'Untitled',
            'poster_path': details.get('poster_path') if details else None,
            'media_type': media_type,
            'vote_average': details.get('vote_average') if details else None,
            'season': season,
            'episode': episode,
        },
        'servers': servers,
        'media_type': media_type,
        'tmdb_id': tmdb_id,
        'season': season,
        'episode': episode,
        'episodes_list': episodes_list,
    }
    return render(request, 'catalog/watch.html', context)

def media_recommendations_api(request, media_type, tmdb_id):
    if media_type not in {'movie', 'tv'}:
        return JsonResponse({'error': 'Unsupported media type.'}, status=404)

    try:
        page = int(request.GET.get('page', 2))
    except ValueError:
        return JsonResponse({'error': 'Page must be a number.'}, status=400)

    if not 2 <= page <= 500:
        return JsonResponse({'error': 'Page must be between 2 and 500.'}, status=400)

    recommendation_data = get_media_recommendations(media_type, tmdb_id, page)
    if recommendation_data is None:
        return JsonResponse({'error': 'Could not load recommendations.'}, status=502)

    results = [
        {
            'id': item.get('id'),
            'title': item.get('title') or item.get('name') or 'Untitled',
            'media_type': media_type,
            'poster_path': item.get('poster_path'),
            'vote_average': item.get('vote_average'),
            'release_date': item.get('release_date') or item.get('first_air_date') or '',
        }
        for item in recommendation_data['results']
    ]
    return JsonResponse({
        'results': results,
        'has_more': page < recommendation_data['total_pages'],
    })

def actor_detail(request, person_id):
    person, filmography = get_person_details(person_id)
    
    # Process filmography to ensure media_type and title fields exist
    processed_filmography = []
    if filmography:
        for item in filmography:
            # Fallback determination for media_type
            m_type = item.get('media_type')
            if not m_type:
                m_type = 'tv' if 'first_air_date' in item or 'name' in item else 'movie'
            
            display_title = item.get('title') or item.get('name') or 'Untitled'
            
            processed_filmography.append({
                'id': item.get('id'),
                'title': display_title,
                'media_type': m_type,
                'poster_path': item.get('poster_path'),
                'vote_average': round(item.get('vote_average', 0), 1) if item.get('vote_average') else None,
                'character': item.get('character', ''),
            })
    
    # Initial load of 12 works
    initial_works = processed_filmography[:12]
    
    context = {
        'person': person,
        'filmography': initial_works,
        'total_works': len(processed_filmography),
    }
    return render(request, 'catalog/actor.html', context)

def actor_works_api(request, person_id):
    """API endpoint to fetch chunked actor filmography for infinite scrolling."""
    page = int(request.GET.get('page', 1))
    page_size = 12
    
    _, filmography = get_person_details(person_id)
    
    processed_filmography = []
    if filmography:
        for item in filmography:
            m_type = item.get('media_type')
            if not m_type:
                m_type = 'tv' if 'first_air_date' in item or 'name' in item else 'movie'
            
            display_title = item.get('title') or item.get('name') or 'Untitled'
            
            processed_filmography.append({
                'id': item.get('id'),
                'title': display_title,
                'media_type': m_type,
                'poster_path': item.get('poster_path'),
                'vote_average': round(item.get('vote_average', 0), 1) if item.get('vote_average') else None,
                'character': item.get('character', ''),
            })
            
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    chunk = processed_filmography[start_idx:end_idx]
    has_more = end_idx < len(processed_filmography)
    
    return JsonResponse({
        'works': chunk,
        'has_more': has_more
    })

def watchlist(request):
    return render(request, 'catalog/watchlist.html')

def search_suggestions(request):
    query = request.GET.get('q', '').strip()
    if not query or len(query) < 2:
        return JsonResponse({'results': []})

    raw_results = search_media(query)
    cleaned_results = []

    for item in raw_results[:7]:
        media_type = item.get('media_type', 'movie')
        title = item.get('title') or item.get('name') or 'Untitled'
        release_date = item.get('release_date') or item.get('first_air_date') or ''
        year = release_date[:4] if release_date else ''
        
        cleaned_results.append({
            'id': item.get('id'),
            'title': title,
            'media_type': media_type,
            'poster_path': item.get('poster_path'),
            'year': year,
            'vote_average': round(item.get('vote_average', 0), 1),
        })

    return JsonResponse({'results': cleaned_results})