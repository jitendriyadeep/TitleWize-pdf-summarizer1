from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

class LegalTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#6c757d')
    practice_area = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class DocumentCategory(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#6c757d')

    def __str__(self):
        return self.name

class PDFDocument(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(
        upload_to='pdfs/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    reviewed = models.BooleanField(default=False)
    review_date = models.DateField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(DocumentCategory, on_delete=models.SET_NULL, null=True, blank=True)
    client_name = models.CharField(max_length=255, blank=True)
    matter_number = models.CharField(max_length=50, blank=True)
    extracted_text = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(LegalTag, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    last_accessed = models.DateTimeField(auto_now=True)
    access_count = models.PositiveIntegerField(default=0)
    summary_length = models.CharField(
        max_length=10,
        choices=[('short', 'Short'), ('medium', 'Medium'), ('long', 'Long')],
        default='medium'
    )

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

class LegalUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = [
        ('PARTNER', 'Partner'),
        ('ASSOCIATE', 'Associate'),
        ('PARALEGAL', 'Paralegal'),
        ('CLIENT', 'Client')
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    practice_area = models.CharField(max_length=100, blank=True)
    bar_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class UserDocumentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_history')
    document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20, choices=[
        ('UPLOAD', 'Uploaded'),
        ('VIEW', 'Viewed'),
        ('EDIT', 'Edited')
    ])

    class Meta:
        ordering = ['-accessed_at']
        unique_together = ['user', 'document', 'action']
        verbose_name = 'Document History'
        verbose_name_plural = 'Document Histories'

    def __str__(self):
        return f"{self.user.username} {self.get_action_display()} {self.document.title}"