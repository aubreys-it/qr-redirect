import logging
import pyodbc
import os

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    qrId = req.params.get('qrId')
    if not qrId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            qrId = req_body.get('qrId')
            
    headers = dict(req.headers)
    columns = "([qrId], "
    tableValues = "('" + qrId + "', "

    tableCols = [
        'host',
        'cache-control',
        'sec-ch-ua',
        'accept-language',
        'x-forwarded-for',
        'connection',
        'accept-encoding',
        'x-arr-ssl',
        'disguised-host',
        'ssc-ch-ua-platform',
        'x-waws-unencoded-url',
        'x-original-url',
        'sec-fetch-mode',
        'x-arr-log-id',
        'x-site-deployment-id',
        'x-appservice-proto',
        'sec-fetch-dest',
        'max-forwards',
        'sec-ch-ua-mobile',
        'x-forwarded-tlsversion',
        'sec-fetch-site',
        'x-forwarded-proto',
        'user-agent',
        'client-ip',
        'was-default-hostname',
        'accept',
        'logEventTime'
    ]

    for col in tableCols:
        if col in headers:
            columns += "[" + col + "], "
            tableValues += "'" + headers[col] + "', "

    columns = columns[:-2]
    tableValues = tableValues[:-2]
    columns += ")"
    tableValues += ")"

    sql = "INSERT INTO [qr].[log] " + columns + " VALUES " + tableValues + ";"

    logging.info(sql)

    conn = pyodbc.connect(os.environ['DMCP_CONNECT_STRING'])
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    sql = "SELECT * FROM [qr].[map] WHERE qrId='" + qrId + "';"
    cursor.execute(sql)
    row = cursor.fetchone()
    uri = row[1] 
    if not uri:
        uri = "https://www.burlesonbrands.com"

    cursor.close()
    conn.close()

    return func.HttpResponse(
        uri,
        headers={'Location': uri},
        status_code=302
    )
