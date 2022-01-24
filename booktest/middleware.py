from django.http import HttpResponse


class BlockedIPSMiddleware(object):
    EXCLUDE_IPS = ['192.168.83.1']

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        '''before view mobilise'''
        if request.META['REMOTE_ADDR'] in BlockedIPSMiddleware.EXCLUDE_IPS: 
            return HttpResponse('<h1>Forbidden</h1>')


class TestMiddleware(object):

    def __init__(self) -> None:
        '''after server restart & receive first request'''
        print('----init----')

    def process_request(self, request):
        '''before url match'''
        print('----process request----')

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        print('----process view----')

    def process_response(self, request, response):
        '''before return to browser'''
        print('----process response----')
        return response


class ExceptionTestMiddleware(object):
    def process_exception(self, request, exception):
        print('---process exception---')
        print(exception)
    

class ExceptionTestMiddleware2(object):
    def process_exception(self, request, exception):
        print('---process exception2---')
        print(exception)
    