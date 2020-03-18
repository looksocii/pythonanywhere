from django.shortcuts import render

# Create your views here.

def index(request):
    num = list()
    for i in range(1, 32):
        num.append(i)
    return render(request, 'select_zip/index.html', {'days': num})