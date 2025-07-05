import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import Dict, Optional
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import logging
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
logging.getLogger("langchain").setLevel(logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.CRITICAL)

load_dotenv() 

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MedicalSummary(BaseModel):
    """Pydantic model for structured medical summary output."""
    overall_condition: str = Field(description="Summary of patient's overall condition")
    test_results: str = Field(description="Key test results or findings")
    diagnosis: str = Field(description="Diagnosis or clinical impression")
    follow_up: str = Field(description="Recommended follow-up or treatment plan")

class MedicalReportSummarizer:
    """Class to handle medical report summarization using LangChain and Groq."""
    
    def __init__(self, model_name: str = "llama-3.3-70b-versatile", api_key: Optional[str] = None):
        """
        Initialize the summarizer with a specific model and API key.
        
        Args:
            model_name (str): Name of the Groq model to use
            api_key (str, optional): Groq API key. Defaults to environment variable if None
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        
        self.prompt_template = self._create_prompt_template()
        self.llm = self._initialize_llm(model_name)
        self.chain = self._initialize_chain()

    def _create_prompt_template(self) -> PromptTemplate:
        """Create and return the prompt template for summarization."""
        template = """
        You are an experienced medical assistant tasked with summarizing medical reports.
        Analyze the following patient report and provide a structured summary.

        Requirements:
        - Use clear, concise, and professional medical language
        - Avoid reproducing protected health information (PHI)
        - Highlight critical findings and recommendations
        - Structure the response in four sections:
          1. Overall Condition: General health status of the patient
          2. Test Results: Key laboratory or imaging findings
          3. Diagnosis: Primary diagnosis or clinical impression
          4. Follow-up: Recommended treatments or follow-up actions

        Medical Report:
        {report_text}

        Summary (use the specified structure):
        """
        return PromptTemplate(
            input_variables=["report_text"],
            template=template
        )

    def _initialize_llm(self, model_name: str) -> ChatGroq:
        """Initialize the Groq LLM with the specified model."""
        try:
            return ChatGroq(
                model_name=model_name,
                api_key=self.api_key,
                temperature=0.3,  # Lower temperature for more factual output
                max_tokens=1000   # Reasonable limit for summary length
            )
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {str(e)}")
            raise

    def _initialize_chain(self) -> LLMChain:
        """Initialize the LangChain LLMChain."""
        try:
            return LLMChain(llm=self.llm, prompt=self.prompt_template)
        except Exception as e:
            logger.error(f"Failed to initialize chain: {str(e)}")
            raise

    def summarize(self, report_text: str) -> MedicalSummary:
        """
        Summarize the medical report and return structured output.
        
        Args:
            report_text (str): The medical report text to summarize
            
        Returns:
            MedicalSummary: Structured summary object
            
        Raises:
            ValueError: If report_text is empty or invalid
            Exception: For other processing errors
        """
        if not report_text or not isinstance(report_text, str):
            raise ValueError("Report text must be a non-empty string")

        try:
            # Run the chain to get raw summary
            raw_summary = self.chain.run(report_text=report_text)
            
            # Parse the raw summary into structured format
            return self._parse_summary(raw_summary)
            
        except Exception as e:
            logger.error(f"Error processing medical report: {str(e)}")
            raise

    def _parse_summary(self, raw_summary: str) -> MedicalSummary:
        """
        Parse raw summary text into structured MedicalSummary object.
        
        Args:
            raw_summary (str): Raw summary text from LLM
            
        Returns:
            MedicalSummary: Structured summary object
        """
        try:
            # Split the summary into sections based on expected headers
            sections = {
                "Overall Condition": "",
                "Test Results": "",
                "Diagnosis": "",
                "Follow-up": ""
            }
            
            current_section = None
            for line in raw_summary.split("\n"):
                line = line.strip()
                if not line:
                    continue
                if any(section in line for section in sections.keys()):
                    current_section = next(section for section in sections.keys() if section in line)
                elif current_section:
                    sections[current_section] += line + " "

            # Create structured output
            return MedicalSummary(
                overall_condition=sections["Overall Condition"].strip(),
                test_results=sections["Test Results"].strip(),
                diagnosis=sections["Diagnosis"].strip(),
                follow_up=sections["Follow-up"].strip()
            )
        except Exception as e:
            logger.error(f"Error parsing summary: {str(e)}")
            raise

def summarize_medical_text(report_text: str, model_name: str = "llama-3.3-70b-versatile") -> Dict:
    """
    Summarize medical report using LangChain + Groq.

    Args:
        report_text (str): The medical report text to summarize
        model_name (str): Name of the Groq model to use
    
    Returns:
        Dict: Structured summary as a dictionary
    """
    summarizer = MedicalReportSummarizer(model_name=model_name)
    summary = summarizer.summarize(report_text)
    return summary.dict()

# if __name__ == "__main__":
#     sample_report = """
#     Patient presented with persistent cough and fever for 7 days. 
#     Chest X-ray shows bilateral infiltrates. 
#     Lab results: WBC 15,000/uL, CRP elevated at 50 mg/L. 
#     Sputum culture pending. 
#     Clinical impression suggests community-acquired pneumonia. 
#     Started on empiric antibiotics (azithromycin). 
#     Recommended follow-up in 3 days or sooner if symptoms worsen.
#     """
    
#     try:
#         summary = summarize_medical_text(sample_report)
#         print("Medical Report Summary:")
#         print(f"Overall Condition: {summary['overall_condition']}")
#         print(f"Test Results: {summary['test_results']}")
#         print(f"Diagnosis: {summary['diagnosis']}")
#         print(f"Follow-up: {summary['follow_up']}")
#     except Exception as e:
#         print(f"Error: {str(e)}")