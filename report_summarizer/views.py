import tempfile
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from .utils.extract_pdf import extract_data_from_medical_report
from .utils.summarize_pdf import summarize_medical_text
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render


logger = logging.getLogger(__name__)


@csrf_exempt
def medical_report_summary_generator(request):
    return render(request, 'medical_report_summary_generator.html')


class SummarizeReportAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist("files")
        if not files:
            return Response({"detail": "No files uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        summaries = []

        for file in files:
            logger.info(f"Processing file: {file.name}")
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    for chunk in file.chunks():
                        tmp.write(chunk)
                    tmp.flush()
                    tmp.seek(0)

                    raw_text = extract_data_from_medical_report(tmp.name, file.name)
                    logger.info(f"Text extraction successful for: {file.name}")

                    summary = summarize_medical_text(raw_text)
                    logger.info(f"Summarization successful for: {file.name}")

                summaries.append({
                    "filename": file.name,
                    "summary": summary,
                })

            except Exception as e:
                logger.exception(f"Failed to process: {file.name}")
                summaries.append({
                    "filename": file.name,
                    "summary": f"Error processing file: {str(e)}",
                })
        logger.info(summaries)
        return Response(summaries, status=status.HTTP_200_OK)
