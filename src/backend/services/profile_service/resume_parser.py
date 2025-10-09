import pdfplumber
import re
from typing import Dict, List, Optional, Any
from io import BytesIO


class ResumeParser:
    """Parse PDF resumes and extract structured information"""

    def __init__(self):
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
        self.url_pattern = re.compile(r'https?://(?:www\.)?linkedin\.com/in/[\w-]+/?')

    def parse_pdf(self, file_content: bytes) -> Dict[str, Any]:
        """Parse PDF resume and extract information"""
        # Extract raw text from PDF
        raw_text = self._extract_text_from_pdf(file_content)

        # Extract structured information
        extracted_data = {
            "raw_text": raw_text,
            "name": self._extract_name(raw_text),
            "email": self._extract_email(raw_text),
            "phone": self._extract_phone(raw_text),
            "linkedin_url": self._extract_linkedin_url(raw_text),
            "skills": self._extract_skills(raw_text),
            "education": self._extract_education(raw_text),
            "experience": self._extract_experience(raw_text),
            "summary": self._extract_summary(raw_text),
        }

        return extracted_data

    def _extract_text_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with pdfplumber.open(BytesIO(file_content)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")

        return text.strip()

    def _extract_name(self, text: str) -> Optional[str]:
        """Extract name from resume (usually first line)"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            # Assume first line is the name if it's not too long and doesn't contain common keywords
            first_line = lines[0]
            if len(first_line.split()) <= 4 and not any(keyword in first_line.lower() for keyword in ['resume', 'cv', 'curriculum']):
                return first_line
        return None

    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email address"""
        matches = self.email_pattern.findall(text)
        return matches[0] if matches else None

    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number"""
        matches = self.phone_pattern.findall(text)
        return matches[0] if matches else None

    def _extract_linkedin_url(self, text: str) -> Optional[str]:
        """Extract LinkedIn URL"""
        matches = self.url_pattern.findall(text)
        return matches[0] if matches else None

    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume"""
        skills = []

        # Common skill keywords to look for
        skill_keywords = [
            'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
            'node.js', 'express', 'django', 'flask', 'spring', 'sql', 'postgresql',
            'mysql', 'mongodb', 'redis', 'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'git', 'ci/cd', 'agile', 'scrum', 'machine learning', 'deep learning',
            'data analysis', 'pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit-learn',
            'html', 'css', 'sass', 'tailwind', 'bootstrap', 'rest api', 'graphql',
            'microservices', 'system design', 'algorithms', 'data structures'
        ]

        text_lower = text.lower()

        # Find skills section
        skills_section_match = re.search(r'skills?\s*:?\s*\n(.*?)(?:\n\n|\n[A-Z])', text, re.IGNORECASE | re.DOTALL)
        skills_text = skills_section_match.group(1) if skills_section_match else text_lower

        # Extract matching skills
        for keyword in skill_keywords:
            if keyword.lower() in skills_text:
                skills.append(keyword.title())

        return list(set(skills))  # Remove duplicates

    def _extract_education(self, text: str) -> List[Dict[str, Any]]:
        """Extract education information"""
        education = []

        # Find education section
        education_section_match = re.search(
            r'education\s*:?\s*\n(.*?)(?:\n\n[A-Z]|$)',
            text,
            re.IGNORECASE | re.DOTALL
        )

        if education_section_match:
            edu_text = education_section_match.group(1)

            # Extract degree patterns
            degree_patterns = [
                r"(Bachelor'?s?|B\.?S\.?|B\.?A\.?|Master'?s?|M\.?S\.?|M\.?A\.?|MBA|Ph\.?D\.?|Doctorate)",
                r"(Computer Science|Engineering|Business|Mathematics|Physics|Chemistry|Biology)"
            ]

            # Look for university names (capitalized words, potentially with "University" or "Institute")
            university_pattern = re.compile(r'([A-Z][a-z]+(?: [A-Z][a-z]+)*\s+(?:University|Institute|College))', re.MULTILINE)
            universities = university_pattern.findall(edu_text)

            # Extract years (4-digit numbers)
            year_pattern = re.compile(r'\b(19|20)\d{2}\b')
            years = year_pattern.findall(edu_text)

            if universities:
                education.append({
                    "institution": universities[0] if universities else None,
                    "degree": "Bachelor's",  # Default assumption
                    "field_of_study": "Computer Science",  # Default assumption
                    "year": int(years[-1]) if years else None,
                    "gpa": None
                })

        return education

    def _extract_experience(self, text: str) -> List[Dict[str, Any]]:
        """Extract work experience"""
        experience = []

        # Find experience section
        experience_section_match = re.search(
            r'(?:experience|employment|work history)\s*:?\s*\n(.*?)(?:\n\neducation|\n\nskills|$)',
            text,
            re.IGNORECASE | re.DOTALL
        )

        if experience_section_match:
            exp_text = experience_section_match.group(1)

            # Split by common job entry patterns
            job_entries = re.split(r'\n(?=[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s*[,\-])', exp_text)

            for entry in job_entries[:3]:  # Limit to 3 most recent positions
                # Extract years
                year_pattern = re.compile(r'\b(19|20)\d{2}\b')
                years = year_pattern.findall(entry)

                # Extract company and position (simplified)
                lines = [line.strip() for line in entry.split('\n') if line.strip()]

                if lines:
                    experience.append({
                        "position": lines[0] if lines else None,
                        "company": lines[1] if len(lines) > 1 else None,
                        "start_date": years[0] if years else None,
                        "end_date": years[-1] if len(years) > 1 else "Present",
                        "description": ' '.join(lines[2:]) if len(lines) > 2 else None
                    })

        return experience

    def _extract_summary(self, text: str) -> Optional[str]:
        """Extract professional summary"""
        # Look for summary section
        summary_patterns = [
            r'(?:summary|profile|objective)\s*:?\s*\n(.*?)(?:\n\n|\n[A-Z])',
        ]

        for pattern in summary_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                summary = match.group(1).strip()
                # Limit to first 500 characters
                return summary[:500] if len(summary) > 500 else summary

        return None
