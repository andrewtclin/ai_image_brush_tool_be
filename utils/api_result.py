import json


# --------------------------------------------------------------------------------------

# HTTP Status Code
status = {
	200: 'OK',
	400: 'Bad Request',
	401: 'Unauthorized',
	403: 'Forbidden',
	404: 'Not Found',
	405: 'Method Not Allowed',
	500: 'Internal Server Error'
}

# http code description (default)
default_description = {
	200: 'Success',
	400: 'Please check paras or query valid.',
	401: 'Please read the document to check API.',
	403: 'Please read the document to check API.',
	404: 'Please read the document to check API.',
	405: 'Please read the document to check API.',
	500: 'Please contact api server manager.'
}

def status_result(status_code, data = {}, description = ''):
	description = default_description.get(status_code) if description == '' else description
	response = json.dumps({
		"code": status_code,
		"status": status.get(status_code),
		"result": data,
		"description": description
	}, default=lambda o: '<not serializable>')
	return response, status_code, {'Content-Type': 'application/json'}