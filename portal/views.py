from django.shortcuts import render
from django.views.generic import TemplateView, FormView

# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

# views.py
from django.shortcuts import render
from django.views import View
from .forms import BillCreationForm
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
            post['location'] = location
        form = BillCreationForm(post)
        if form.is_valid():
            # Save the bill, get the printer from the location, and print it
            bill = form.save()
            printer = bill.location.printer
            text = f'Bill: {bill.temp_name}\n'
            for product in Product.objects.filter(location=bill.location):
                text += f'{product.name}: {product.price_per_unit}\n'
            if printer:
                printer.print_text(text)
                
            
            
            
            alert_kind = 'success'
            alert_message = 'Bill created successfully'
        else:
            alert_kind = 'danger'
            alert_message = f'Bill creation failed: {form.errors}'
            
    else:
        try:
            location = Location.objects.get(name=location_name)
            print(f'Location found: {location}')
        except Location.DoesNotExist:
            location = None
            print(f'Location not found in GET: {location_name}' )
        alert_kind, alert_message = None, None
        form = BillCreationForm(initial={'location': location})
    if location:
        locations = [location]
    else:
        locations = Location.objects.all()
    return render(request, 'bill_creation.html', {'form': form, 'locations': locations, 'alert_message': alert_message, 'alert_kind': alert_kind, 'location_name': location_name})