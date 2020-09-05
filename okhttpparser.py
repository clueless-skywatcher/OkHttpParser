import re
import json

class OkHttpRequestObject:
	def __init__(self, endpoint, method, header = None, payload = None):
		self.method = method
		self.header = header
		self.payload = payload
		self.endpoint = endpoint

class OkHttpResponseObject:
	def __init__(self, endpoint, status_code, status_code_name, header = None, payload = None):
		self.endpoint = endpoint
		self.header = header
		self.payload = payload
		self.status_code = status_code
		self.status_code_name = status_code_name

class OkHttpParser:
	def __init__(self, logfile, lines = 1000):
		self.loglines = []
		with open(logfile, 'r') as f:
			for line in f.readlines()[:lines]:
				if 'D/OkHttp' in line:
					self.loglines.append(line.split('D/OkHttp: ')[1].rstrip())

	def parse_requests(self):
		header = dict()
		payload = dict()

		requests = []

		request_start = False

		for line in self.loglines:
			if line.startswith("-->"):
				if not line.startswith("--> END"):
					request_start = True
					method = line.split(" ")[1]
					endpoint = line.split(" ")[2]
					request = OkHttpRequestObject(endpoint, method)
				else:
					request.header = header
					request.payload = payload
					request_start = False
					requests.append(request)
					header = dict()
					payload = dict()

			if re.match(r"\w+(?:-\w+)+", line) and request_start:
				header_key = line.split(": ", 1)[0]
				header_val = line.split(": ", 1)[1]
				header[header_key] = header_val

			if line.startswith("{") and request_start:
				payload = json.loads(line)
			elif not (line.startswith("--") or line.startswith("<--")) and request_start:
				payload = line

		return requests

	def parse_responses(self):
		header = dict()
		payload = dict()

		responses = []

		response_start = False

		for line in self.loglines:
			if line.startswith("<--"):
				if not line.startswith("<-- END"):
					response_start = True
					status_code = line.split(" ")[1]
					status_code_name = line.split(" ")[2]
					endpoint = line.split(" ")[3]
					response = OkHttpResponseObject(endpoint, status_code, status_code_name)
				else:
					response.header = header
					response.payload = payload
					response_start = False
					responses.append(response)
					header = dict()
					payload = dict()

			if re.match(r"\w+(?:-\w+)*:", line) and response_start:
				header_key = line.split(": ", 1)[0]
				header_val = line.split(": ", 1)[1]
				header[header_key] = header_val

			if line.startswith("{") and response_start:
				payload = json.loads(line)
			elif not (line.startswith("--") or line.startswith("-->")) and response_start:
				payload = line

		return responses

if __name__ == '__main__':
	okhttp = OkHttpParser('assignment.txt', lines = 1300)
	for line in okhttp.loglines:
		print(line)

	# print("----------------------------------------")
	# for request in okhttp.parse_requests():
	# 	print(f"Method: {request.method}")
	# 	print(f"Endpoint: {request.endpoint}")
	# 	print(f"Header: {json.dumps(request.header, indent = 4)}")
	# 	print(f"Payload: {json.dumps(request.payload, indent = 4)}")
	# 	print()
	# print("----------------------------------------")
	# for response in okhttp.parse_responses():
	# 	print(f"Status Code: {response.status_code}")
	# 	print(f"Status Code Name: {response.status_code_name}")
	# 	print(f"Header: {json.dumps(response.header, indent = 4)}")
	# 	print(f"Payload: {json.dumps(response.payload, indent = 4)}")
	# 	print()
