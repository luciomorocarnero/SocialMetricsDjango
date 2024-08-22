from django.db import models
import uuid

# Create your models here.
class ServiceRequest(models.Model):
    SERVICES = (
        ('Twitter', 'Twitter'),
        ('Youtube','Youtube'),
        ('Instagram', 'Instagram'),
        ('Facebook', 'Facebook')
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    service = models.CharField(max_length=20, choices=SERVICES)
    params = models.JSONField(encoder=models.JSONField.encoder, decoder=models.JSONField.decoder)
    data = models.JSONField(encoder=models.JSONField.encoder, decoder=models.JSONField.decoder)
    
    def __str__(self):
        return f"Request {self.id} for {self.service} at {self.created_at.isoformat()}"

    @classmethod
    def last_request(cls, service: str):
        return cls.objects.filter(service=service).order_by('-created_at').first()
    
    @classmethod
    def exist_response(cls):
        pass