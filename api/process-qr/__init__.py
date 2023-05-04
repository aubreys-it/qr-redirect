import logging
import json

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
            
    headers = dict(req.headers)

    logging.info(json.dumps(headers, indent=2))

    return func.HttpResponse(
        headers,
        status_code=200
    )
