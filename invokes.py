import requests

SUPPORTED_HTTP_METHODS = set([
    "GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"
])

def invoke_http(url, method='GET', json=None, **kwargs):
    """A simple wrapper for requests methods.
       url: the url of the http service;
       method: the http method;
       data: the JSON input when needed by the http method;
       return: the JSON reply content from the http service if the call succeeds;
            otherwise, return a JSON object with a "code" name-value pair.
    """
    code = 200
    result = {}

    try:
        if method.upper() in SUPPORTED_HTTP_METHODS:
            print("NEW TRY")
            r = requests.request(method, url, json = json, **kwargs)
            print("Request is populated")
            # r = requests.get(method, url, json = json, **kwargs)

            # r = {"code": 200, "offers": "None"}
        else:
            raise Exception("HTTP method {} unsupported.".format(method))
    except Exception as e:
        print("Requests is empty")
        code = 500
        result = {"code": code, "message": "invocation of service fails: " + url + ". " + str(e)}
    if code not in range(200,300):
        print("Code not in range 200, 300")
        return result

    ## Check http call result
    # r.status_code = code
    print("STATUS CODE:", r.status_code)

    if r.status_code != requests.codes.ok: # requests.codes.ok = 200
        code = r.status_code
        
    try:
        print("R.json:", r.json())
        print("R.content:", r.content)
        result = r.json() if len(r.content)>0 else "" 
        print("Results populated")
    except Exception as e:
        print("Results is empty")
        code = 500
        result = {"code": code, "message": "Invalid JSON output from service: " + url + ". " + str(e)}
    print("Printing results:", result)
    return result

# invoke_http(offer_URL, method='POST', json=offer)