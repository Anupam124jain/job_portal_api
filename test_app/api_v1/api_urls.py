"""
    Apis end point urls
"""
from django.urls import path
from test_app.api_v1 import api

urlpatterns = [
    path('jobs/', api.JobsList.as_view()),
    path('jobs/<str:title_id>', api.JobsDetails.as_view()),
    path('jobs/<str:title_id>/top_skills', api.SkillsListing.as_view())
]
