from django.test import TestCase
from unittest.mock import patch


class WatchPageTests(TestCase):
    @patch('catalog.views.get_media_recommendations')
    @patch('catalog.views.get_media_credits')
    @patch('catalog.views.get_media_details')
    def test_watch_page_shows_cast_under_player_and_related_titles(
        self, get_details, get_credits, get_recommendations
    ):
        get_details.return_value = {
            'id': 123,
            'title': 'Featured Movie',
            'overview': 'A test synopsis.',
            'poster_path': '/featured.jpg',
            'vote_average': 8.0,
        }
        get_credits.return_value = [
            {
                'id': 456,
                'name': 'Test Actor',
                'character': 'Lead',
                'profile_path': None,
            }
        ]
        get_recommendations.return_value = {
            'results': [
                {
                    'id': 789,
                    'title': 'Related Movie',
                    'poster_path': '/related.jpg',
                    'vote_average': 7.5,
                }
            ],
            'total_pages': 1,
        }

        response = self.client.get('/watch/movie/123/')

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn('Cast & Characters', content)
        self.assertIn('Test Actor', content)
        self.assertIn('Related Movie', content)
        self.assertLess(content.index('video-player'), content.index('cast-heading'))
        self.assertIn('"media_type": "movie"', content)
        self.assertIn('"title": "Featured Movie"', content)


class RecommendationsApiTests(TestCase):
    @patch('catalog.views.get_media_recommendations')
    def test_returns_paginated_recommendations_for_media_type(self, get_recommendations):
        get_recommendations.return_value = {
            'results': [
                {
                    'id': 789,
                    'title': 'Related Movie',
                    'poster_path': '/related.jpg',
                    'vote_average': 7.5,
                    'release_date': '2024-01-01',
                }
            ],
            'total_pages': 3,
        }

        response = self.client.get('/api/recommendations/movie/123/?page=2')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'results': [
                {
                    'id': 789,
                    'title': 'Related Movie',
                    'media_type': 'movie',
                    'poster_path': '/related.jpg',
                    'vote_average': 7.5,
                    'release_date': '2024-01-01',
                }
            ],
            'has_more': True,
        })
        get_recommendations.assert_called_once_with('movie', 123, 2)

    def test_rejects_invalid_page_number(self):
        response = self.client.get('/api/recommendations/tv/123/?page=invalid')

        self.assertEqual(response.status_code, 400)
