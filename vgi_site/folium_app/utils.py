def handle_uploaded_file(f):
    with open("SIRI.xml", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
