import time

from fidelio import settings
from fidelio_core import *

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from fidelio_app.models import *


def index(request):
    if request.method == 'POST':

        if 'index_upload' or 'navbar_upload' in request.POST:

            file = request.FILES['files']
            file_name = request.FILES['files'].name
            do_we_have_file, md5 = handle_uploaded_file(file, file_name)

            if not do_we_have_file:


                fidelio = Fidelio(file_name, settings.MEDIA_ROOT)
                fidelio.start()

                while True:
                    if fidelio.finished:

                        sound = Sound(file_name=file_name, samplerate=fidelio.samplerate, md5=md5, gif=fidelio.gif_path)
                        sound.save()
                        images = fidelio.get_images()

                        for x in images:
                            image = FidelioImage(file_path=x)
                            image.save()
                            sound.images.add(image)

                        return redirect('/fi/' + md5)

                    time.sleep(0.01)
            else:

                return redirect('/fi/' + md5)

    background = Sound.objects.order_by('?').first()

    if background is None:

        return render_to_response('index.html',
                                  {'background': 'assets/img/slides/yolo.gif'},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('index.html',
                                  {'background': background.gif},
                                  context_instance=RequestContext(request))


def handle_uploaded_file(f, filename):
    destination = open(settings.MEDIA_ROOT + filename, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    md5 = create_md5(settings.MEDIA_ROOT + filename)

    try:
        sound = Sound.objects.get(md5__exact=md5)
        os.remove(settings.MEDIA_ROOT + filename)
        return True, md5
    except Sound.DoesNotExist:
        return False, md5


def create_md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def created(request, md5):
    sound = Sound.objects.get(md5__exact=md5)
    return render_to_response('created.html',
                              {'sound': sound},
                              context_instance=RequestContext(request))
