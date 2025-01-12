from formaloo import constants, client


class GamificationCalculationJob:
    def __init__(self):
        self.client = client.Client()

    def create(self):
        body = self.get_body()

        response = self.client.post(
            constants.V_1_0_CREATE_GAMIFICATION_CALCULATION_JOB,
            body=body
        )

        return response.status_code, response.json()

    def get_body(self):
        body = {
        }
        return body