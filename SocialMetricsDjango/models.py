from django.db import models, transaction
import datetime
import uuid
from zoneinfo import ZoneInfo

# Create your models here.
class ServiceRequest(models.Model):
    """Django Model for db of the requests"""
    
    SERVICES = (
        ('Twitter', 'Twitter'),
        ('Youtube','Youtube'),
        ('Instagram', 'Instagram'),
        ('Facebook', 'Facebook'),
        ('Tiktok', 'Tiktok')
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    service = models.CharField(max_length=20, choices=SERVICES)
    params = models.JSONField()
    data = models.JSONField()
    
    def __str__(self):
        return f"Request for {self.service} at {self.created_at.astimezone().strftime(format=r'%Y-%m-%d %H:%M:%S')}"

    @classmethod
    def _last_request(
        cls,
        service: str,
        params: dict,
        date_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
    ):
        """
        Search last response after selected date
        
        :param service: service of the object like 'Twitter' or 'Youtube'
        :param params: params of the object like {"userName": "name"}
        :param datetime: must be in utc like 'datetime.datetime(tzinfo=datetime.timezone.utc)'
        :return: None if not match and object if it's found
        """
        queryset = cls.objects.all().order_by('-created_at')
        for query in queryset:
            if query.service == service and query.params == params and query.created_at > date_time:
                return query
            if query.created_at.date() < date_time.date():
                break 
        return None
    
    def last_request(
        self,
        date_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
    ):
        """
        Search last response after selected date of the object
        
        :params datetime: must be in utc like 'datetime.datetime(tzinfo=datetime.timezone.utc)'
        :return: None if not match and object if it's found
        """
        return ServiceRequest._last_request(service=self.service, params=self.params, date_time=date_time)
