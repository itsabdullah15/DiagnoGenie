import pdfplumber
import json
import os
from typing import List, Dict, Optional
from dataclasses import dataclass
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


@dataclass
class MedicationInfo:
    """Data class for medication information"""
    name: str
    frequency: str
    dosage: str = ""
    purpose: str = ""


class PrescriptionAnalyzer:
    """Simple prescription medicine analyzer"""
    
    def __init__(self, groq_api_key: str = None, model_name: str = "llama-3.3-70b-versatile"):
        self.groq_api_key = groq_api_key or os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY must be provided or set as environment variable")
        
        self.llm = ChatGroq(model=model_name, api_key=self.groq_api_key)
        self._setup_prompts()
    
    def _setup_prompts(self):
        """Setup prompts"""
        self.extract_medication_prompt = PromptTemplate(
            input_variables=["prescription_text"],
            template="""
Extract medication details from this prescription text.
Return ONLY valid JSON in this format:
{{
  "medications": [
    {{
      "name": "medication name",
      "dosage": "dosage amount",
      "frequency": "frequency"
    }}
  ]
}}

Text: {prescription_text}
"""
        )
        
        self.purpose_prompt = PromptTemplate(
            input_variables=["medication_name"],
            template="""
Briefly explain what '{medication_name}' is used for. Keep it simple and under 3 sentences.
"""
        )
    
    def extract_pdf_text(self, pdf_path: str) -> Optional[str]:
        """Extract text from PDF"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text_content = []
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        text_content.append(page_text.strip())
                return "\n\n".join(text_content) if text_content else None
        except Exception as e:
            print(f"PDF extraction error: {e}")
            return None
    
    def extract_medications(self, prescription_text: str) -> List[Dict[str, str]]:
        """Extract medications from text"""
        try:
            chain = LLMChain(llm=self.llm, prompt=self.extract_medication_prompt)
            response = chain.run(prescription_text=prescription_text)
            
            # Clean response
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:-3]
            elif response.startswith("```"):
                response = response[3:-3]
            
            parsed_data = json.loads(response)
            return parsed_data.get("medications", [])
            
        except Exception as e:
            print(f"Extraction error: {e}")
            return []
    
    def get_medication_purpose(self, medication_name: str) -> str:
        """Get medication purpose"""
        try:
            # chain = self.purpose_prompt | self.llm
            chain = LLMChain(llm=self.llm, prompt=self.purpose_prompt)
            return chain.run(medication_name=medication_name).strip()
        except Exception as e:
            return f"Purpose unavailable for {medication_name}"
    
    def analyze_prescription(self, pdf_path: str) -> List[MedicationInfo]:
        """Analyze prescription and return results"""
        # Extract text
        prescription_text = self.extract_pdf_text(pdf_path)
        if not prescription_text:
            return []
        
        # Extract medications
        medications_data = self.extract_medications(prescription_text)
        if not medications_data:
            return []
        
        # Analyze each medication
        analyzed_medications = []
        for med_data in medications_data:
            med_name = med_data.get("name", "")
            if not med_name:
                continue
            
            purpose = self.get_medication_purpose(med_name)
            
            medication_info = MedicationInfo(
                name=med_name,
                frequency=med_data.get("frequency", ""),
                dosage=med_data.get("dosage", ""),
                purpose=purpose
            )
            
            analyzed_medications.append(medication_info)
        
        return analyzed_medications
    
    def print_summary(self, medications: List[MedicationInfo]):
        """Print simple summary"""
        if not medications:
            print("No medications found.")
            return
        
        print(f"\nFound {len(medications)} medications:")
        print("-" * 40)
        
        for i, med in enumerate(medications, 1):
            print(f"{i}. {med.name}")
            if med.dosage:
                print(f"   Dosage: {med.dosage}")
            if med.frequency:
                print(f"   Frequency: {med.frequency}")
            print(f"   Purpose: {med.purpose}")
            print()


# def main():
#     """Main function"""
#     try:
#         analyzer = PrescriptionAnalyzer()
        
#         # Change this path to your PDF file
#         pdf_path = r"C:\Users\abdullah.shahid\Downloads\medical_prescription.pdf"
        
#         medications = analyzer.analyze_prescription(pdf_path)
#         analyzer.print_summary(medications)
        
#     except Exception as e:
#         print(f"Error: {e}")


# if __name__ == "__main__":
#     main()