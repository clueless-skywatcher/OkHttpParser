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
	'''
	Main parsing class for Android log files
	Usage:
	>>> from okhttpparser import OkHttpParser
	>>> okhttp = OkHttpParser('file.txt', lines = 2000)
	>>> okhttp.parse() --> returns a list of pairs of requests and their
	corresponding responses
	'''
	def __init__(self, logfile, lines = 1400):
		self.loglines = []
		with open(logfile, 'r') as f:
			for line in f.readlines()[:lines]:
				# This part here assumes that the HTTP request-response lines
				# are contained only in lines where "D/OkHttp" is present
				if 'D/OkHttp' in line:
					self.loglines.append(line.split('D/OkHttp: ')[1].rstrip())

	def parse(self):
		request_response_bounds = []
		req_res_start = False
		x, y = -1, -1
		for i in range(len(self.loglines)):
			# This part assumes that each request starts with a line that contains
			# "-->" at the beginning
			# Solution: We might want to check where "GET" or "POST" is mentioned
			# without an "END" in the line
			if self.loglines[i].startswith("-->") and not req_res_start:
				x = i
				req_res_start = True
			# Instead of using "-->", searching for an "END" in the line would mean
			# that the request/response is over
			if self.loglines[i].startswith("<-- END") and req_res_start:
				y = i
				req_res_start = False
				request_response_bounds.append([x, y])

		req_res_pair_bounds = []

		for rr in request_response_bounds:
			for i in range(rr[0], rr[1] + 1):
				if self.loglines[i].startswith("--> END"):
					req_res_pair_bounds.append([(rr[0], i), (i + 1, rr[1])])
					break

		req_res_pairs = []

		for req, res in req_res_pair_bounds:
			# Here is where things might go wrong. It has been assumed that
			# when splitting the line by space, the 2nd element would give the
			# HTTP method, and the 3rd would give the HTTP endpoint for the API
			# call
			# Solution: Use a regex to detect the HTTP endpoint, use a "GET/POST"
			# finder to find the HTTP method used
			req_method = self.loglines[req[0]].split(" ")[1]
			req_endpoint = self.loglines[req[0]].split(" ")[2]

			request = OkHttpRequestObject(req_endpoint, req_method)
			req_header = {}
			req_payload = {}
			for i in range(req[0] + 1, req[1]):
				if re.match(r'[@_!#$%^&*()<>?/\|}{~]*\w+(?:-\w+)*:', self.loglines[i]):
					header_key = self.loglines[i].split(": ", 1)[0]
					header_val = self.loglines[i].split(": ", 1)[1]
					req_header[header_key] = header_val
				# Assumption has been made that the payload might start with "{"
				# If payload starts with "{" then it has been assumed that the line
				# is a JSON object, or otherwise a plain payload. This may break for
				# multipart data or images
				# Solution: Using a lookahead parser for detecting multipart data/images.
				if self.loglines[i].startswith("{"):
					req_payload = json.loads(self.loglines[i])
				elif not self.loglines[i].startswith("--"):
					req_payload = self.loglines[i]
			request.payload = req_payload
			request.header = req_header

			# Just like the request parsing, here we are also assuming that the 2nd string
			# of the split is the status code of a response, the 3rd is the name of the
			# status code, and the 4th is the endpoint.
			# Solution: Write a regex for detecting the endpoint, a regex for finding the
			# status code, and there may be a regex for detecting the name of the status code
			# (if it exists)

			# Also this may break for image responses, and we are still assuming that strings
			# beginning with braces are JSON payloads, otherwise they are just strings.
			# Obviously this would not work properly for images, which are in some sort of
			# garbled text called "Mojibake" due to incompatible encoding.
			# Solution: Use proper decoding techniques to decode images.
			res_status_code = self.loglines[res[0]].split(" ")[1]
			res_status_code_name = self.loglines[res[0]].split(" ")[2]
			res_endpoint = self.loglines[res[0]].split(" ")[3]
			response = OkHttpResponseObject(res_endpoint, res_status_code, res_status_code_name)
			res_header = {}
			res_payload = {}
			for i in range(res[0] + 1, res[1]):
				if re.match(r'[@_!#$%^&*()<>?/\|}{~]*\w+(?:-\w+)*:', self.loglines[i]):
					header_key = self.loglines[i].split(": ", 1)[0]
					header_val = self.loglines[i].split(": ", 1)[1]
					res_header[header_key] = header_val
				if self.loglines[i].startswith("{"):
					res_payload = json.loads(self.loglines[i])
				elif not self.loglines[i].startswith("--"):
					res_payload = self.loglines[i]
			response.payload = res_payload
			response.header = res_header

			req_res_pairs.append((request, response))
		return req_res_pairs

# if __name__ == '__main__':
# 	okhttp = OkHttpParser('../input (1).txt')
# 	for line in okhttp.loglines:
# 		print(line)
# 	for req, res in okhttp.parse():
# 		print("-------------------------------------------")
# 		print("Request:")
# 		print(f'Method: {req.method}')
# 		print(f'Endpoint: {req.endpoint}')
# 		print(f'Header: {json.dumps(req.header, indent = 4)}')
# 		print(f'Payload: {json.dumps(req.payload, indent = 4)}')
# 		print()
# 		print("Response:")
# 		print(f'Endpoint: {res.endpoint}')
# 		print(f'Status Code: {res.status_code}')
# 		print(f'Status Code Name: {res.status_code_name}')
# 		print(f'Header: {json.dumps(res.header, indent = 4)}')
# 		print(f'Payload: {json.dumps(res.payload, indent = 4)}')
