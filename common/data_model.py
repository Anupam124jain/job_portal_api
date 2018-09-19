""" Create common python function which is use in rest apis """

from operator import add
import requests
from test_app.models import JobSeeker

#get scores according to open skills api levels and importance

def get_score(title_id):
    """
        desc: This function is use to find out the scores of skills.
        :param: title_id:str
        :return: top_ten_scores

    """
    respons_skills = requests.get('http://api.dataatwork.org/v1/jobs/%s/related_skills' % title_id)
    json_result = respons_skills.json()
    top_ten_scores = json_result['skills'][ :10]
    levels = []
    importance = []
    for i  in range(10):
        levels.append(top_ten_scores[i]['level'])
        importance.append(top_ten_scores[i]['importance'])
        result = list(map(add, levels, importance))
        avarage = result[i]/2
        top_ten_scores[i]['scores'] = avarage

    return top_ten_scores

#get top ten skills according to score

def get_top_skills(title_id):
    """
        desc: This function is use to find out top ten skills according to scores
        :param title_id: str
        :return: top ten skills

    """
    skills_scores = get_score(title_id)
    top_score_skills = sorted(skills_scores, key=lambda score: float(score['scores']), reverse=True)
    return top_score_skills


#check title_id

def check_title_id(title_id):
    """
        desc: This function is use to check job title id and its length
        :param: title_id: str
        :return: Boolean values

    """
    jobs = JobSeeker.objects.all()
    for job in jobs:
        if len(title_id) == 32 and title_id == job.title_id or title_id != job.title_id:
            return True
        return False
