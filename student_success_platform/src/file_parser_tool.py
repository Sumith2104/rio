"""
Multi-Format Document Parser & Academic Content Classifier (PACD-RAG)
=====================================================================
Author: Sumith U (SRN: R24EA807) | 7th Sem B.Tech CSE (AI & ML), Section B, REVA University
Project: AI-Powered Smart Campus Intelligence & Student Success Platform

Ingests and extracts structured data from:
- PDF (Syllabus, Question papers, Assignment briefs)
- Excel / CSV (Attendance registers, IA marks sheets, End-sem exam registers)
- PowerPoint (.pptx) (Lecture slide decks, Unit presentations)
- Text files
Autonomously classifies the academic intent and payloads for downstream agent tools.
"""

import os
import re
import json
from typing import Dict, Any, List, Optional
import pandas as pd
from pypdf import PdfReader
from pptx import Presentation

class FileParserTool:
    def __init__(self):
        pass

    def extract_text_from_pdf(self, file_path: str) -> Dict[str, Any]:
        """Extracts text and page-by-page content from PDF documents."""
        reader = PdfReader(file_path)
        pages_text = []
        full_text = []
        for idx, page in enumerate(reader.pages):
            txt = page.extract_text() or ""
            pages_text.append({"page": idx + 1, "text": txt})
            full_text.append(txt)
        
        combined = "\n".join(full_text)
        return {
            "file_type": "PDF",
            "page_count": len(reader.pages),
            "pages": pages_text,
            "raw_text": combined
        }

    def extract_data_from_excel_or_csv(self, file_path: str) -> Dict[str, Any]:
        """Parses tabular academic registers, marks sheets, and attendance."""
        ext = os.path.splitext(file_path)[1].lower()
        if ext in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)
        
        # Clean column names (lowercase, strip whitespace)
        df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
        
        # Convert to records
        records = df.to_dict(orient="records")
        return {
            "file_type": "SPREADSHEET",
            "columns": list(df.columns),
            "row_count": len(records),
            "records": records,
            "dataframe_summary": df.head(5).to_dict(orient="records")
        }

    def extract_content_from_pptx(self, file_path: str) -> Dict[str, Any]:
        """Extracts slide titles, bullet points, and speaker notes from PowerPoint presentations."""
        prs = Presentation(file_path)
        slides_data = []
        all_text = []

        for idx, slide in enumerate(prs.slides):
            slide_text = []
            title = ""
            for shape in slide.shapes:
                if shape.has_text_frame:
                    for paragraph in shape.text_frame.paragraphs:
                        txt = paragraph.text.strip()
                        if txt:
                            slide_text.append(txt)
            
            if slide_text:
                title = slide_text[0]
            
            combined_slide = "\n".join(slide_text)
            slides_data.append({
                "slide_number": idx + 1,
                "title": title,
                "content": combined_slide
            })
            all_text.append(f"--- Slide {idx+1}: {title} ---\n{combined_slide}")

        return {
            "file_type": "PPTX",
            "slide_count": len(prs.slides),
            "slides": slides_data,
            "raw_text": "\n\n".join(all_text)
        }

    def classify_academic_document(self, parsed_data: Dict[str, Any], filename: str) -> Dict[str, Any]:
        """
        Autonomously determines the nature of the document without human labeling.
        """
        fn = filename.lower()
        raw_text = parsed_data.get("raw_text", "").lower()
        columns = [c.lower() for c in parsed_data.get("columns", [])]
        
        # 1. Attendance Sheet Detection
        attendance_cues = ["attendance", "present", "absent", "attendance_pct", "att_pct", "attended", "classes_held"]
        if any(c in columns for c in attendance_cues) or ("attendance" in fn and "srn" in columns):
            return {
                "detected_type": "ATTENDANCE_SHEET",
                "confidence": 0.96,
                "target_tool": "academic_ingest_tool",
                "recommended_action": "INGEST_ATTENDANCE_RECORDS"
            }

        # 2. IA Marks Sheet Detection
        ia_cues = ["ia1", "ia2", "ia1_score", "ia2_score", "ia_marks", "internal_assessment", "q1", "q2", "q3"]
        if any(c in columns for c in ia_cues) or ("ia" in fn and any(c in columns for c in ["marks", "score"])):
            return {
                "detected_type": "IA_MARKS",
                "confidence": 0.95,
                "target_tool": "academic_ingest_tool",
                "recommended_action": "INGEST_IA_AND_TRIGGER_RISK_PIPELINE"
            }

        # 3. Assignment Marks Sheet Detection
        asg_marks_cues = ["assignment_score", "asg1", "asg2", "assignment_marks", "lab_assignment"]
        if any(c in columns for c in asg_marks_cues) or ("assignment" in fn and "marks" in fn):
            return {
                "detected_type": "ASSIGNMENT_MARKS",
                "confidence": 0.93,
                "target_tool": "academic_ingest_tool",
                "recommended_action": "RECORD_ASSIGNMENT_SCORES"
            }

        # 4. End Semester Exam Marks Detection
        exam_cues = ["exam_score", "end_sem", "see_marks", "final_exam", "grade", "sgpa"]
        if any(c in columns for c in exam_cues) or "exam" in fn or "grade" in fn:
            return {
                "detected_type": "EXAM_MARKS",
                "confidence": 0.92,
                "target_tool": "academic_ingest_tool",
                "recommended_action": "UPDATE_FINAL_GRADES_AND_SGPA"
            }

        # 5. Assignment Specification / Question Paper Detection (PDF/Word/Text)
        assignment_spec_cues = ["assignment", "problem statement", "due date", "submission deadline", "rubric", "instructions", "submit by", "max marks:"]
        matches = sum(1 for cue in assignment_spec_cues if cue in raw_text or cue in fn)
        if matches >= 2 or ("assignment" in fn and ("due" in raw_text or "problem" in raw_text or "question" in raw_text)):
            return {
                "detected_type": "ASSIGNMENT_SPECIFICATION",
                "confidence": 0.94,
                "target_tool": "assignment_manager_tool",
                "recommended_action": "CREATE_AND_ASSIGN_TO_STUDENTS"
            }

        # 6. Syllabus or Lecture Slides (PPTX / PDF / Text)
        if parsed_data.get("file_type") == "PPTX" or "syllabus" in fn or "module" in raw_text or "unit" in raw_text or "course outcome" in raw_text:
            return {
                "detected_type": "SYLLABUS_OR_SLIDES",
                "confidence": 0.95,
                "target_tool": "syllabus_indexer_tool",
                "recommended_action": "VECTORIZE_CHUNKS_AND_EXTRACT_PREREQUISITE_DAG"
            }

        # Default fallback
        return {
            "detected_type": "GENERAL_ACADEMIC_DOCUMENT",
            "confidence": 0.70,
            "target_tool": "syllabus_indexer_tool",
            "recommended_action": "INDEX_FOR_KNOWLEDGE_BASE"
        }

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Entrypoint for parsing any file format and classifying its payload."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        filename = os.path.basename(file_path)
        ext = os.path.splitext(filename)[1].lower()

        if ext == ".pdf":
            parsed = self.extract_text_from_pdf(file_path)
        elif ext in [".xlsx", ".xls", ".csv"]:
            parsed = self.extract_data_from_excel_or_csv(file_path)
        elif ext in [".pptx", ".ppt"]:
            parsed = self.extract_content_from_pptx(file_path)
        elif ext in [".txt", ".md"]:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            parsed = {"file_type": "TEXT", "raw_text": content}
        else:
            raise ValueError(f"Unsupported file format: {ext}")

        parsed["filename"] = filename
        parsed["file_size_kb"] = round(os.path.getsize(file_path) / 1024.0, 1)
        
        classification = self.classify_academic_document(parsed, filename)
        parsed["classification"] = classification

        return parsed

if __name__ == "__main__":
    parser = FileParserTool()
    print("FileParserTool initialized successfully.")

