from django.shortcuts import render
from django.views.generic import TemplateView, FormView


# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

# views.py
from django.shortcuts import render
from django.views import View
from .models import Location, Product, Bill, Printer

def PortalView(request, location_name=None, kiosk=False):
    # location validation
    if not Location.objects.filter(name=location_name).exists():
        location_name = None
    return render(request, 'portal.html', {'location_name': location_name, 'kiosk':kiosk})

def BillCreationView(request, location_name=None):
    if request.method == 'POST':
        print(f'POST: {request.POST}')
        # if there isnt a valid location, try to get it from the location_name
        post = request.POST.copy()  # Make a mutable copy
        if not post.get('location'):
            try:
                location = Location.objects.get(name=location_name)
                print(f'Location found: {location}')
            except Location.DoesNotExist:
                location = None
                print(f'Location not found in POST: {location_name}' )
            post['location'] = location.id
                
            
            
            
            alert_kind = 'success'
            alert_message = 'Bill created successfully'
        else:
            alert_kind = 'danger'
            alert_message = f'Bill creation failed'
            
    else:
        try:
            location = Location.objects.get(name=location_name)
            print(f'Location found: {location}')
        except Location.DoesNotExist:
            location = None
            print(f'Location not found in GET: {location_name}' )
        alert_kind, alert_message = None, None
    if location:
        locations = [location]
    else:
        locations = Location.objects.all()
    return render(request, 'bill_creation.html', {'locations': locations, 'alert_message': alert_message, 'alert_kind': alert_kind, 'location_name': location_name})

def get_bill_item(request):
    if request.method == 'GET':
        print(f'GET: {request.GET}')
        if request.GET.get('location'):
            products = Product.objects.filter(location__id=request.GET.get('location'))
        else:
            print('No location in GET')
            return render(request, 'bill_item.html', {'products': None, 'location': request.GET.get('location')})
        return render(request, 'bill_item.html', {'products': products, 'location': request.GET.get('location')})