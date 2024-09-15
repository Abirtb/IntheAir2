from django.http import JsonResponse
from rest_framework.views import APIView
from .models import UploadedFile, FileChunk
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import logging

from .tasks import combine_file_chunks  # Import the Celery task

logger = logging.getLogger(__name__)

class FileChunkUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file_id = request.POST.get('file_id')
        chunk_number = int(request.POST.get('chunk_number'))
        is_last = request.POST.get('is_last', 'false').lower() == 'true'
        chunk_data = request.FILES['chunk'].read()

        # Retrieve or create the UploadedFile instance
        uploaded_file, created = UploadedFile.objects.get_or_create(
            id=file_id,
            defaults={
                'file_name': request.POST.get('file_name'),
                'total_chunks': int(request.POST.get('total_chunks'))
            }
        )

        # Increment the number of chunks received and save the model
        uploaded_file.chunks_received += 1
        uploaded_file.save(update_fields=['chunks_received'])

        # Create a new chunk instance
        FileChunk.objects.create(
            uploaded_file=uploaded_file,
            chunk_number=chunk_number,
            data=chunk_data,
            is_last=is_last
        )

        # Check if all chunks have been received
        if is_last or uploaded_file.chunks_received == uploaded_file.total_chunks:
            # Queue the Celery task to combine the file
            combine_file_chunks(uploaded_file.id)
            print(UploadedFile.objects.all())

        return JsonResponse({'status': 'success', 'file_id': uploaded_file.id})

class FileListView(APIView):
    def get(self, request, *args, **kwargs):
        files = UploadedFile.objects.all()
        return JsonResponse({'files': list(files.values('id', 'file_name', 'total_size', 'upload_date'))}, safe=False)

    def delete(self, request, *args, **kwargs):
        file_id = request.GET.get('file_id')
        try:
            
            file = UploadedFile.objects.get(id=file_id)
            file.chunks.all().delete()
            file.delete()
            return JsonResponse({'status': 'success', 'message': 'File deleted successfully'})
        except UploadedFile.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'File not found'}, status=404)
