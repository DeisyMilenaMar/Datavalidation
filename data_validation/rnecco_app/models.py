from django.db import models
from django.utils import timezone


class ApiClient(models.Model):
    name = models.TextField()
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='creation timestamp',
        db_index=True,
        help_text='Moment when user information is initially obtained'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='update timestamp', 
        db_index=True, 
        help_text='Moment when user information is updated'
    )
     

    class Meta:
        verbose_name = "API Client"
        verbose_name_plural = "API Clients"

    def __str__(self):
        return f"{self.name}  ({self.is_active})"



class ApiKey(models.Model):
    key = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey(ApiClient, on_delete=models.CASCADE, related_name='api_keys')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='creation timestamp',
        db_index=True,
        help_text='Moment when user information is initially obtained'

    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='update timestamp', 
        db_index=True, 
        help_text='Moment when user information is updated'
    )
    
    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"

    def __str__(self):
        return f"{self.key} ({self.client.name})"
    


class IdentityInformation(models.Model):
    identification_number = models.CharField(max_length=20)
    issue_date = models.DateField()
    issue_place = models.CharField(max_length=100)
    name = models.TextField()
    status = models.CharField(max_length=70)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='creation timestamp', 
        db_index=True, 
        help_text='Initial moment when user information is initially obtained'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='update timestamp', 
        db_index=True, 
        help_text='Moment when user information is updated'
    )
    api_key = models.ForeignKey(ApiKey, on_delete=models.CASCADE, related_name='identity_information')

    class Meta:
        verbose_name = "Identity Information"
        verbose_name_plural = "Identity Information"
        unique_together = ['identification_number', 'api_key']

    def __str__(self):
        return f"{self.name} ({self.identification_number})"


class RequestLog(models.Model):
    api_key = models.ForeignKey(ApiKey, on_delete=models.CASCADE, related_name= 'request_logs')
    request_body = models.JSONField(blank=True, default=dict, help_text='Request')
    response_body = models.JSONField(blank=True, default=dict, help_text='Response')
    status_code = models.IntegerField(help_text='Status code')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='creation timestamp', 
        db_index=True, 
        help_text='Created'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='update timestamp', 
        db_index=True, 
        help_text='Moment when user information is updated'
    )

    class Meta:
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"

    def __str__(self):
        return f"Request {self.id} ({self.api_key.key})"
