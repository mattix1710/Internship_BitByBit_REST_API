from rest_framework.response import Response
from rest_framework.decorators import api_view

# example
@api_view(['GET'])
def getData(request):
    person = {'name':'Jan', 'age':30}
    return Response(person)