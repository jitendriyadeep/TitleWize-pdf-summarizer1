from django.shortcuts import render, redirect
from django.contrib import messages
from .models import PDFDocument
from .utils import extract_text_from_pdf, generate_summary
from .models import LegalUserProfile
import os
from django.conf import settings
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .decorators import partner_required
from django.utils import timezone
# from docx import Document
from django.http import HttpResponse
# from xhtml2pdf import pisa
from io import BytesIO
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import UserDocumentHistory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, get_user_model
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm

User = get_user_model()

def custom_password_reset(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            request.session['reset_username'] = username  # Store username in session
            return redirect('password_reset_confirm')
        except User.DoesNotExist:
            messages.error(request, 'Username not found. Please try again.')
    
    return render(request, 'registration/password_reset.html')

def custom_password_reset_confirm(request):
    username = request.session.get('reset_username')
    if not username:
        return redirect('password_reset')
    
    user = User.objects.get(username=username)
    
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            del request.session['reset_username']  # Clear the session
            messages.success(request, 'Your password has been updated successfully!')
            return redirect('login')
    else:
        form = SetPasswordForm(user)
    
    return render(request, 'registration/password_reset_confirm.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create a LegalUserProfile for the new user
            LegalUserProfile.objects.create(
                user=user,
                role='CLIENT',  # Default role for new users
                practice_area=''  # Empty by default
            )
            
            login(request, user)  # Log the user in immediately
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('upload_pdf')
        else:
            # Add form errors to messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

class UserDocumentHistoryView(LoginRequiredMixin, ListView):
    model = UserDocumentHistory
    template_name = 'pdfprocessor/document_history.html'
    paginate_by = 10
    context_object_name = 'page_obj'  # Add this line
    
    def get_queryset(self):
        return UserDocumentHistory.objects.filter(user=self.request.user).select_related('document')

@login_required
def upload_pdf(request):
    if request.method == 'POST':
        title = request.POST.get('title', 'Untitled Document')
        pdf_file = request.FILES.get('pdf_file')
        summary_length = request.POST.get('summary_length', 'medium')
        
        if not pdf_file:
            messages.error(request, 'Please select a PDF file to upload.')
            return redirect('upload_pdf')
        
        if not pdf_file.name.endswith('.pdf'):
            messages.error(request, 'File must be a PDF.')
            return redirect('upload_pdf')
        
        # Create PDFDocument instance with current user
        pdf_doc = PDFDocument(
            title=title,
            file=pdf_file,
            summary_length=summary_length,
            uploaded_by=request.user  # This is required
        )
        pdf_doc.save()
        
        # Extract text from PDF
        pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_doc.file.name)
        extracted_text = extract_text_from_pdf(pdf_path)
        pdf_doc.extracted_text = extracted_text
        pdf_doc.save()
        
        # Generate summary
        summary = generate_summary(extracted_text, summary_length)
        if summary:
            pdf_doc.summary = summary
            pdf_doc.save()
            return redirect('view_summary', pk=pdf_doc.pk)
        else:
            messages.error(request, 'Failed to generate summary. Please try again.')
            return redirect('upload_pdf')
    
    return render(request, 'pdfprocessor/upload.html')

def view_summary(request, pk):
    pdf_doc = get_object_or_404(PDFDocument, pk=pk)

    # Update access tracking
    pdf_doc.access_count += 1
    pdf_doc.save()
    
    # Mark HTML as safe for rendering
    formatted_summary = mark_safe(pdf_doc.summary) if pdf_doc.summary else None

    # Update or create history entry (without creating duplicates)
    UserDocumentHistory.objects.update_or_create(
        user=request.user,
        document=pdf_doc,
        action='VIEW',
        defaults={'accessed_at': timezone.now()}
    )
    
    context = {
        'pdf_doc': pdf_doc,
        'formatted_summary': formatted_summary,
        'party_count': pdf_doc.summary.count("PAN:") if pdf_doc.summary else 0,
        'financial_count': pdf_doc.summary.count("₹") if pdf_doc.summary else 0,
        'doc_ref_count': pdf_doc.summary.count("Document No") if pdf_doc.summary else 0
    }
    return render(request, 'pdfprocessor/summary.html', context)
# views.py


@login_required
def dashboard(request):
    # Law firm statistics
    stats = {
        'total_docs': PDFDocument.objects.count(),
        'pending_review': PDFDocument.objects.filter(reviewed=False).count(),
        'top_categories': PDFDocument.objects.values('category__name')
                               .annotate(total=Count('category'))
                               .order_by('-total')[:5]
    }
    
    recent_docs = PDFDocument.objects.order_by('-uploaded_at')[:10]
    
    return render(request, 'pdfprocessor/dashboard.html', {
        'stats': stats,
        'recent_docs': recent_docs
    })
def legal_search(request):
    query = request.GET.get('q', '')
    
    results = PDFDocument.objects.filter(
        Q(client_name__icontains=query) |
        Q(matter_number__iexact=query) |
        Q(extracted_text__icontains=query) |
        Q(summary__icontains=query) |
        Q(file__icontains=query)
    ).distinct()
    
    return render(request, 'pdfprocessor/search_results.html', {
        'results': results,
        'query': query
    })
# views.py


@partner_required
def delete_document(request, pk):
    document = get_object_or_404(PDFDocument, pk=pk)
    document.delete()
    messages.success(request, 'Document deleted successfully')
    return redirect('dashboard')

# views.py


# def export_docx(request, pk):
#     doc = get_object_or_404(PDFDocument, pk=pk)
    
#     document = Document()
#     document.add_heading(f'Legal Summary - {doc.title}', 0)
    
#     # Add metadata table
#     table = document.add_table(rows=4, cols=2)
#     table.cell(0,0).text = 'Client'
#     table.cell(0,1).text = doc.client_name
#     table.cell(1,0).text = 'Matter Number'
#     table.cell(1,1).text = doc.matter_number
#     # ... add more metadata
    
#     document.add_heading('Summary', level=1)
#     document.add_paragraph(doc.summary)
    
#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
#     response['Content-Disposition'] = f'attachment; filename="{doc.title}_summary.docx"'
#     document.save(response)
#     return response

# def export_pdf(request, pk):
#     doc = get_object_or_404(PDFDocument, pk=pk)
#     html = render_to_string('pdfprocessor/export_pdf.html', {'doc': doc})
    
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
#     if not pdf.err:
#         response = HttpResponse(result.getvalue(), content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="{doc.title}_summary.pdf"'
#         return response
    
#     return HttpResponse('Error generating PDF', status=500)
# views.py
# @legal_staff_required
# def manage_tags(request, pk):
#     document = get_object_or_404(PDFDocument, pk=pk)
    
#     if request.method == 'POST':
#         tag_id = request.POST.get('tag_id')
#         action = request.POST.get('action')
        
#         if action == 'add':
#             document.tags.add(tag_id)
#         elif action == 'remove':
#             document.tags.remove(tag_id)
            
#         return JsonResponse({'status': 'success'})
    
#     all_tags = LegalTag.objects.all()
#     return render(request, 'pdfprocessor/manage_tags.html', {
#         'document': document,
#         'all_tags': all_tags
#     })