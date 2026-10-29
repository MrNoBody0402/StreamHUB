import requests

TMDB_READ_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0OTliNDA0N2ZmMWQwNDViOTIyM2I5Y2U3MGUzODU0OSIsIm5iZiI6MTc5MjE2NTA2NC42OTkwMDAxLCJzdWIiOiI2YWQyNDRjODFhMWI1OTlmOWNjNjMwYWIiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.vh43kyFptJyGO88URqMRSiiL7QsDiIc6EqE1QfSY4UY"
BASE_URL = "https://api.themoviedb.org/3"

HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_READ_TOKEN}"
}

GENRES = {
    'action': 28,
    'adventure': 12,
    'animation': 16,
    'comedy': 35,
    'crime': 80,
    'drama': 18,
    'fantasy': 14,
    'horror': 27,
    'mystery': 9648,
    'romance': 10749,
    'scifi': 878,
    'thriller': 53,
}

def get_media_list(media_type="movie", category="popular", page=1, genre_id=None):
    if genre_id:
        url = f"{BASE_URL}/discover/{media_type}?with_genres={genre_id}&page={page}&sort_by=popularity.desc"
    elif category == "trending":
        url = f"{BASE_URL}/trending/{media_type}/week?page={page}"
    else:
        url = f"{BASE_URL}/{media_type}/{category}?page={page}"
        
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get('results', [])
    except Exception as e:
        print(f"Error fetching {category} {media_type}: {e}")
    return []

def get_media_details(media_type, tmdb_id):
    url = f"{BASE_URL}/{media_type}/{tmdb_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching details for {media_type} {tmdb_id}: {e}")
    return None

def get_media_credits(media_type, tmdb_id):
    """Fetch cast list for a movie or TV show."""
    url = f"{BASE_URL}/{media_type}/{tmdb_id}/credits"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get('cast', [])[:12]
    except Exception as e:
        print(f"Error fetching credits for {media_type} {tmdb_id}: {e}")
    return []

def get_person_details(person_id):
    """Fetch details and filmography for a specific actor."""
    person_url = f"{BASE_URL}/person/{person_id}"
    credits_url = f"{BASE_URL}/person/{person_id}/combined_credits"
    
    person_data = None
    filmography = []
    
    try:
        p_res = requests.get(person_url, headers=HEADERS)
        if p_res.status_code == 200:
            person_data = p_res.json()
            
        c_res = requests.get(credits_url, headers=HEADERS)
        if c_res.status_code == 200:
            results = c_res.json().get('cast', [])
            filmography = sorted(results, key=lambda x: x.get('popularity', 0), reverse=True)
    except Exception as e:
        print(f"Error fetching person data for {person_id}: {e}")
        
    return person_data, filmography

def search_media(query):
    url = f"{BASE_URL}/search/multi?query={query}"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            results = response.json().get('results', [])
            return [item for item in results if item.get('media_type') in ['movie', 'tv']]
    except Exception as e:
        print(f"Error searching media: {e}")
    return []