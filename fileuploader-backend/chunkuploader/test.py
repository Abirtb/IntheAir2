from chunkuploader.models import UploadedFile
print(UploadedFile.objects.all())  # List all files to see if the target one is still there
