import question

class survey:

	def __init__(self, s_id, questions):
		self.s_id = s_id	
		self.questions = questions	
		#Survey ID will dictate a file which will be read from
		#questions contains a list of questions will be read from the surveys csv		


#Class representing a partitcular courses survey structure
class course:

	def __init__(self, course_id, q_list):
		self.course_id = course_id
		self.q_list = q_list
		
	def show_survey(self,course_id):
		#from routes.py file already...
		
	def publish_survey(self):
		#Publish a link to the survey, show the link on the screen	
	
	
	
	
	
#Class representing a response from a respondent
class response:
	#						      Question       1,2,3,4,5
	#response is a list of answers e.g. -> [s_id A,B,C,C,D]
	def __init__(self, s_id, response):	
		self.response = response	
		self.s_id = s_id
		
	#returns a list containing values for the new response list	
	def get_response(self):
	
		new_resp = #...get the response from the survey page after pressing submit	
		return new_resp
		 			
	#Writes the response of a survey to a data csv file	
	#response as a list of answers, with each index representing a question id
	def write_response(self, s_id, response):
		name = s_id + ".data.csv"
		response = get_response()
		with open(name, "a") as f:
		writer = csv.writer(f)
		writer.writerows(response)	
		
		
	

