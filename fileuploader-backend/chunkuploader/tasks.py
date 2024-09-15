from celery import shared_task
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import UploadedFile, FileChunk

@shared_task
def combine_file_chunks(uploaded_file_id):
    print("begin")
    uploaded_file = UploadedFile.objects.get(id=uploaded_file_id)
    chunks_query = uploaded_file.chunks.all().order_by('chunk_number')
    complete_file_data = b''.join(chunk.data for chunk in chunks_query)
    print("aaaaa")

    # Save the combined file to the default storage
    file_path = default_storage.save(f'media/{uploaded_file.file_name}', ContentFile(complete_file_data))
    uploaded_file.total_size = default_storage.size(file_path)
    uploaded_file.save(update_fields=['total_size'])

    print(f"File {uploaded_file.file_name} combined and saved at {file_path}. Total size: {uploaded_file.total_size}")
