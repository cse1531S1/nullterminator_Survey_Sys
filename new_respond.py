from sql_uti import SqlUtil
from server import app

class Respond():
    """docstring for respond."""
    def __init__(self):
        super().__init__("respond")
    def insert_response(self, survey_id):
        
