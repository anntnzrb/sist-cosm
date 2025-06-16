"""
Common mixins for views following SPARC modularity principles.
Provides reusable functionality across different apps.
"""
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


class MessageMixin:
    """Mixin to provide standardized messaging."""
    
    success_message = "Operación realizada exitosamente."
    error_message = "Ha ocurrido un error. Por favor, intente nuevamente."
    
    def form_valid(self, form):
        """Add success message on valid form submission."""
        messages.success(self.request, self.get_success_message())
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Add error message on invalid form submission."""
        messages.error(self.request, self.get_error_message())
        return super().form_invalid(form)
    
    def get_success_message(self):
        """Get success message for the view."""
        return self.success_message
    
    def get_error_message(self):
        """Get error message for the view."""
        return self.error_message


class PaginationMixin:
    """Mixin to provide pagination functionality."""
    
    paginate_by = 12
    
    def paginate_queryset(self, queryset):
        """Paginate the queryset with error handling."""
        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page', 1)
        
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        
        return page_obj
    
    def get_context_data(self, **kwargs):
        """Add pagination context."""
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'object_list'):
            context['page_obj'] = self.paginate_queryset(self.object_list)
        return context


class SearchMixin:
    """Mixin to provide search functionality."""
    
    search_fields = []
    
    def get_queryset(self):
        """Filter queryset based on search query."""
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        
        if query and self.search_fields:
            search_filter = Q()
            for field in self.search_fields:
                search_filter |= Q(**{f"{field}__icontains": query})
            queryset = queryset.filter(search_filter)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add search context."""
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class AjaxResponseMixin:
    """Mixin to handle AJAX requests."""
    
    def dispatch(self, request, *args, **kwargs):
        """Handle AJAX and regular requests."""
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return self.ajax_response(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)
    
    def ajax_response(self, request, *args, **kwargs):
        """Handle AJAX request and return JSON response."""
        try:
            response_data = self.get_ajax_data(request, *args, **kwargs)
            return JsonResponse(response_data)
        except Exception as e:
            logger.error(f"AJAX error: {str(e)}")
            return JsonResponse({'error': 'Error processing request'}, status=500)
    
    def get_ajax_data(self, request, *args, **kwargs):
        """Override in subclasses to provide AJAX data."""
        return {'status': 'success'}


class SecurityMixin:
    """Mixin to add security headers and validation."""
    
    def dispatch(self, request, *args, **kwargs):
        """Add security headers to response."""
        response = super().dispatch(request, *args, **kwargs)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        
        return response
    
    def form_valid(self, form):
        """Add security validation to form processing."""
        # Log form submission for audit trail
        logger.info(f"Form submission by user: {self.request.user} for {self.__class__.__name__}")
        return super().form_valid(form)


class CosmeticsCRUDMixin(MessageMixin, PaginationMixin, SearchMixin, SecurityMixin):
    """Combined mixin for cosmetics store CRUD operations."""
    
    def get_context_data(self, **kwargs):
        """Add common context for cosmetics store."""
        context = super().get_context_data(**kwargs)
        context['app_name'] = getattr(self, 'app_name', '')
        context['page_title'] = getattr(self, 'page_title', '')
        context['create_url'] = getattr(self, 'create_url', '#')
        return context


class PerformanceMixin:
    """Mixin to optimize database queries."""
    
    select_related_fields = []
    prefetch_related_fields = []
    
    def get_queryset(self):
        """Optimize queryset with select_related and prefetch_related."""
        queryset = super().get_queryset()
        
        if self.select_related_fields:
            queryset = queryset.select_related(*self.select_related_fields)
        
        if self.prefetch_related_fields:
            queryset = queryset.prefetch_related(*self.prefetch_related_fields)
        
        return queryset