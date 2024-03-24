from django.shortcuts import render
from fruit_shop.utils import send_code_via_phone,generate_verification_code
from django.http import JsonResponse,HttpResponse

# Create your views here.
def index(request):
    return render(request,'pages/index.html')

def about(request):
    return render(request,'pages/about.html')

def contact(request):
    return render(request,'pages/contact-us.html')


def test(request):
    if request.method == 'POST' and request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        input_value = request.POST.get('inputField')
        print(input_value)
        return JsonResponse({'result': input_value})
    return render(request,'bin/ajax-test.html')

def save_data(request):
    if request.method == 'POST' and request.is_ajax():
        # Assuming your data is sent as JSON
        data = request.POST.get('your_data_key')

        # Save data to the database
        print(data)

        return JsonResponse({'message': 'Data saved successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'})