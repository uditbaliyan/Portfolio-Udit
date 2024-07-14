import qrcode
from django.shortcuts import render
from django.conf import settings
import os

def generate_qr(request):
    if request.method == 'POST':
        # Get the data from the form
        data = request.POST.get('qr_data')
        
        # Sanitize the input data to create a valid file name
        filename = "img.png"
        
        # Generate the QR code
        qr_img = qrcode.make(data)
        
        # Define the directory where you want to save the image
        directory = os.path.join(settings.MEDIA_ROOT, 'images')
        
        # Create the directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        
        # Construct the full file path dynamically
        file_path = os.path.join(directory, filename)
        
        # Save the QR code image
        qr_img.save(file_path)
        
        # Pass the QR code image filename to the template
        return render(request, 'qr_generator.html', {'qr_img': f'media/images/{filename}'})

    # If it's a GET request or the form is not submitted
    return render(request, 'qr_generator.html')
