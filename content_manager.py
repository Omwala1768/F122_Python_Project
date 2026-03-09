from syllabus_data import syllabus
from resources_data import resources

def get_topics(semester):
    return syllabus.get(semester, [])

from resources_data import resources


def get_resources(topic):

    if topic not in resources:
        return [], []

    data = resources[topic]

    websites = data.get("websites", [])
    youtube = data.get("youtube", [])

    return websites, youtube

