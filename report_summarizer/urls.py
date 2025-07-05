from django.urls import path
from .views import SummarizeReportAPIView, medical_report_summary_generator

urlpatterns = [
    path('summarize-report/', SummarizeReportAPIView.as_view(), name='summarize-report'),
    
    path('medical_report_summary/', medical_report_summary_generator, name='medical_report_summary_generator-page'),
    
]
