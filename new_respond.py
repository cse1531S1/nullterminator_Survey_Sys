from sql_uti import SqlUtil
from user import UserData


class Respond(SqlUtil):
    """Controller for Respond, control the table for respond"""
    def __init__(self, arg):
        super().__init__("respond")

class RespondMcq(SqlUtil):
    """Control table for respond_mcq."""
    def __init__(self, arg):
        super().__init__("respond_mcq")

class RespondText(SqlUtil):
    """Table control for respond_text"""
    def __init__(self, arg):
        super().__init__("respond_text")
    


if __name__ == '__main__':
    # unitests
    pass
