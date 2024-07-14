# views.py
# pip install qrcode

from django.shortcuts import render

from text_to_speech import save

# text = "Hello, World!"
# language = "en"  # Specify the language (IETF language tag)
# output_file = "hello_world.mp3"  # Specify the output file (only accepts .mp3)

# save(text, language, file=output_file)



import os

def generate_tts(request):
    if request.method == 'POST':
        # Get the data from the form
        text = request.POST.get('qr_data')
        
        # Sanitize the input data to create a valid file name
        language = "en"  # Specify the language (IETF language tag)
        
        output_file = f"media/audio/hello_world.mp3"  # Specify the output file (only accepts .mp3)
        save(text, language, file=output_file)

        
        # Pass the QR code image filename to the template
        return render(request, 'tts_generator.html', {'qr_img': output_file})

    # If it's a GET request or the form is not submitted
    return render(request, 'tts_generator.html')
