def make_request(stdin=None, environ=None,
                   response=None, clean=1, stdout=None):
    from ZPublisher.HTTPRequest import HTTPRequest
    from ZPublisher.HTTPResponse import HTTPResponse
    from zope.publisher.browser import setDefaultSkin
    from cStringIO import StringIO

    if stdin is None:
        stdin = StringIO()

    if stdout is None:
        stdout = StringIO()

    if environ is None:
        environ = {}

    if 'SERVER_NAME' not in environ:
        environ['SERVER_NAME'] = 'http://localhost'

    if 'SERVER_PORT' not in environ:
        environ['SERVER_PORT'] = '8080'

    if response is None:
        response = HTTPResponse(stdout=stdout)

    req = HTTPRequest(stdin, environ, response, clean)
    setDefaultSkin(req)
    return req

