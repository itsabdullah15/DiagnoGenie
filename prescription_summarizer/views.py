from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from prescription_summarizer.utils.summarize import PrescriptionAnalyzer

class PrescriptionUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        pdf_file = request.FILES.get('file')
        if not pdf_file:
            return Response({"error": "No PDF file provided."}, status=status.HTTP_400_BAD_REQUEST)

        with open("temp_prescription.pdf", "wb+") as f:
            for chunk in pdf_file.chunks():
                f.write(chunk)

        analyzer = PrescriptionAnalyzer()
        try:
            medications = analyzer.analyze_prescription("temp_prescription.pdf")
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"medications": medications})
