import requests

from formaloo import constants, client


class ActivityBatch:

    def __init__(self, activities=[]):
        self.client = client.Client()
        self.activities = activities

    def add_activity(self, activity):
        self.activities.append(activity)

    def create(self):
        body = self.get_body()

        response = self.client.post(
            constants.V_1_0_ACTIVITY_BATCH_ENDPOINT,
            body=body
        )

        return response

    def get_body(self):
        body = []

        for activity in self.activities:
            body.append(
                activity.get_body()
            )

        return body