from django.shortcuts import render


# views


def index(request):

    return render(request, 'welcome.html')

def table(request):
    
    return render(request, 'table.html')

def model(request):
    
    return render(request, 'model.html')

def charts(request):
    # Pandas DataFrame Query
    return render(request, 'charts.html')
    
def report(request):
    # Pandas DataFrame Query
    return render(request, 'report.html')