import datetime
def application(environ,start_response):
    status='200 OK'
    time_now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    serv = environ['SERVER_ADDR']
    sern = environ['SERVER_NAME']
    serp = environ['SERVER_PORT']
    clit = environ['REMOTE_ADDR']
    clitp = environ['REMOTE_PORT']
    output='''<html>
<head>
</head>
<body>
<hr>date:%s
<br><font color=#0000FF>server=%s#%s </font>
<br><font color=#0000FF>server=%s#%s </font>
<br><font color=#ff0000>client=%s#%s </font>
<hr>
</body>
<html>
    '''%(time_now,sern,serp,serv,serp,clit,clitp)
    #output = str(environ)

    response_headers=[('Content-type','text/html'),('Content-Length',str(len(output)))]
    start_response(status,response_headers)
    
    return [output]
