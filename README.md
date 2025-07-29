DiagnoGenie

DiagnoGenie is a comprehensive project designed to assist in medical document processing, focusing on summarizing prescriptions and medical reports. It aims to streamline the understanding and management of medical information.FeaturesPrescription Summarization: Automatically extracts and summarizes key information from prescription texts, such as medication names, dosages, and frequencies.Report Summarization: Provides capabilities to summarize medical reports, making it easier to grasp essential details quickly.User Accounts: Manages user authentication and profiles.Templates: Likely includes various templates for document processing or report generation.Generative AI CoreDiagnoGenie leverages the power of Large Language Models (LLMs) to perform its core summarization tasks. Specifically:Intelligent Summarization: LLMs are utilized to process raw prescription and medical report texts, identifying and extracting critical information to generate concise and accurate summaries. The current implementation uses the Mistral model via the Groq API for these summarization capabilities.Contextual Understanding: The models are designed to understand the medical context of the documents, ensuring that the summaries are not just extractive but also semantically meaningful and relevant.Scalable Processing: The architecture is built to handle various document lengths and complexities, providing efficient summarization capabilities.InstallationTo set up DiagnoGenie locally, follow these steps:Clone the repository:git clone https://github.com/your-username/DiagnoGenie.git
cd DiagnoGenie

Set up a virtual environment (recommended):python -m venv venv
source venv/bin/activate  # On Windows: `venv\Scripts\activate`

Install dependencies:pip install -r requirements.txt # (Assuming a requirements.txt file exists)

Database Migrations:python manage.py migrate

Run the development server:python manage.py runserver

(Note: Specific dependencies and detailed setup instructions might be required based on the project's exact requirements, e.g., API keys for LLMs.)UsageOnce the application is running, you can:Access the web interface to manage accounts.Upload prescription texts or medical reports for summarization.View summarized outputs.Project StructureThe project is organized into the following main directories and files:DiagnoGenie/
├── accounts/                     # Manages user authentication and profiles
│   └── ...
├── prescription_summarizer/      # Handles the summarization of prescription texts
│   ├── _init_.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── report_summarizer/            # Handles the summarization of medical reports
│   ├── _init_.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── templates/                    # Contains HTML templates for the web interface
│   └── ...
├── utils/                        # Utility functions and helpers
│   ├── summarize.py
│   └── extract_pdf.py
├── .gitignore                    # Specifies intentionally untracked files to ignore
├── LICENSE                       # Project licensing information
├── README.md                     # This README file
└── manage.py                     # Django's command-line utility for administrative tasks

LicenseThis project is licensed under the LICENSE file.
