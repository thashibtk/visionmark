import os
import django
from django.test import RequestFactory, Client
from django.urls import reverse
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visionmark.settings')
django.setup()

from myapp.views import about

def check_context():
    try:
        client = Client()
        url = reverse('about')
        print(f"URL for 'about': {url}")
        response = client.get(url)
        
        print(f"Response type: {type(response)}")
        if hasattr(response, 'context'):
            print(f"Response context type: {type(response.context)}")
            if response.context is None:
                print("Response context is None.")
                # Fallback: maybe verify by content?
                if b'servicedetails' in response.content:
                     print("SUCCESS (via content): 'servicedetails' link found.")
                else:
                     print("FAILURE: Link not found in content.")
                return

            if 'services' in response.context:
                print("SUCCESS: 'services' found in context.")
                # print(f"Count: {response.context['services'].count()}")
            else:
                 # response.context might be a list of dicts
                 print(f"Context content: {response.context}")
                 found = False
                 try:
                     for ctx in response.context:
                         if 'services' in ctx:
                             print("SUCCESS: 'services' found in nested context.")
                             found = True
                             break
                 except:
                     pass
                 
                 if not found:
                     print("FAILURE: 'services' NOT found in context.")
        else:
             print("Response has no context.")

    except Exception:
        with open('traceback.log', 'w') as f:
            traceback.print_exc(file=f)

if __name__ == "__main__":
    check_context()
