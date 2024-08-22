from django.db import models
import datetime
import uuid
from zoneinfo import ZoneInfo 

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
    params = models.JSONField()
    data = models.JSONField()
    
    def __str__(self):
        return f"Request {self.id} for {self.service} at {self.created_at.isoformat()}"

    @classmethod
    def last_request(
        cls, 
        service: str,
        params: dict
        ):
        return cls.objects.filter(service=service).filter(params=params).order_by('-created_at').first()
    
    @classmethod
    def exist_request(
        cls, 
        service: str, 
        params: dict, 
        time: datetime.timedelta = datetime.timedelta(days=1)
        ):
        last_request = cls.last_request(service,params)
        if last_request is None:
            return False
        last_request_date = last_request.created_at
        now = datetime.datetime.now(datetime.timezone.utc)
        date_delta = now - time
        return last_request_date > date_delta
    
    