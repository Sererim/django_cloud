from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.shortcuts import render
from django.utils.timezone import datetime, timedelta
from .models import Client, Product, Order
from .forms import ClientForm
from PIL import Image
from io import BytesIO


def order_list(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['timeframe'] == '7':
                start_date = datetime.now() - timedelta(days=7)
            elif form.cleaned_data['timeframe'] == '30':
                start_date = datetime.now() - timedelta(days=30)
            elif form.cleaned_data['timeframe'] == '365':
                start_date = datetime.now() - timedelta(days=365)
            else:
                pass

            client = Client.objects.filter(firstname=form.cleaned_data['firstname'], surname=form.cleaned_data['surname']).first()
            orders = Order.objects.filter(client_id=client, date_of_order__gte=start_date)
            
            context = {
                'orders': orders,
                'client': client,
            }
            return render(request, 'myapp/order_list.html', context)

    return render(request, 'myapp/index.html')


# View for upload_image.htnl
def upload_image(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        try:
            img = Image.open(image_file)
            img_bytes = BytesIO()
            img.save(img_bytes, format='JPEG')
            img_bytes.seek(0)
            product.image.save(image_file.name, img_bytes)
            
            return redirect('product_details', product_id=product_id)
        except IOError:
            product.image = None
            product.save()
            msg = "Failed to process the uploaded image."
            return render(request, 'myapp/upload_image.html', {'product_id':product_id, 'error_message':msg})
        
    context = {'product_id':product_id}
    return render(request, 'myapp/upload_image.html', context)


# View for showign product.
def product_details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'myapp/product_details.html', context)
