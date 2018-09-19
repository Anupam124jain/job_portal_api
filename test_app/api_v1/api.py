""" Jobs create, listing apis"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

from test_app.models import JobSeeker
from test_app.api_v1.serializers import JobsListSerializer, JobsDetailsSerializer

from common.data_model import get_top_skills, check_title_id
from common.messages import INTERNAL_SERVER_ERROR, INVALID_REQUEST


class JobsList(APIView):

    """ Apis for create jobs and show jobs listing """

    serializer_class = JobsListSerializer

    @classmethod
    def get(cls, request):   # pylint: disable=unused-argument
        """ To get the jobs listing """
        try:
            jobs = JobSeeker.objects.all()
            serializer = JobsListSerializer(jobs, many=True)
            return Response(serializer.data)
        except (AttributeError, KeyError, TypeError):
            content = {'message': INTERNAL_SERVER_ERROR}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def post(cls, request):
        """ To create a new jobs"""
        try:
            serializer = JobsListSerializer(data=request.data)
            if serializer.is_valid():
                title = serializer.validated_data['title']
                response_title = requests.get(
                    'http://api.dataatwork.org/v1/jobs/autocomplete?begins_with=%s' % title
                )
                title_json = response_title.json()
                serializer.validated_data['title_id'] = title_json[0]['uuid']
                title_id = serializer.validated_data['title_id']
                respons_skills = requests.get(
                    'http://api.dataatwork.org/v1/jobs/%s/related_skills' % title_id
                )
                response_skills = respons_skills.json()
                serializer.validated_data[
                    'normalized_title'
                ] = title_json[0]['normalized_job_title']
                serializer.validated_data['skills'] = response_skills['skills'][:10]
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (AttributeError, KeyError, TypeError):
            content = {'message': INTERNAL_SERVER_ERROR}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JobsDetails(APIView):

    """ Jobs details list according to job title_id """

    serializer_class = JobsDetailsSerializer

    @classmethod
    def get(cls, request, title_id):  # pylint: disable=unused-argument
        """To get a one jobs detail  """
        try:
            if check_title_id(title_id):
                jobs_title = JobSeeker.objects.filter(
                    title_id=title_id
                )
                serializer = JobsDetailsSerializer(jobs_title, many=True)
                return Response(serializer.data)

            return Response(
                {'message': INVALID_REQUEST},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        except (AttributeError, KeyError, TypeError):
            content = {'message': INTERNAL_SERVER_ERROR}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SkillsListing(APIView):

    """  List of top 10 highest skills """
    serializer_class = JobsListSerializer

    @classmethod
    def get(cls, request, title_id):   # pylint: disable=unused-argument
        """ To get a list of top 10 highest skills """
        try:
            if check_title_id(title_id):
                jobs_title = JobSeeker.objects.filter(title_id=title_id)
                print(jobs_title)
                serializer = JobsDetailsSerializer(jobs_title, many=True)
                serializer.data[0]['skills'] = get_top_skills(title_id)
                return Response(serializer.data)

            return Response(
                {'message': INVALID_REQUEST},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        except (AttributeError, KeyError, TypeError):
            content = {'message': INTERNAL_SERVER_ERROR}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
