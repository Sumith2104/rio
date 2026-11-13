"""
Autonomous Syllabus & Lecture Slides Vector Indexer (PACD-RAG)
==============================================================
Author: Sumith U (SRN: R24EA807) | 7th Sem B.Tech CSE (AI & ML), Section B, REVA University
Project: AI-Powered Smart Campus Intelligence & Student Success Platform

Ingests syllabus documents and slide decks into ChromaDB vector collections,
extracts prerequisite dependencies, and populates the learning materials repository.
"""

import os
import sys
import json
import re
from typing import Dict, Any, List, Optional

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from vector_db_manager import VectorDBManager
from fluxbase_client import FluxbaseClient
from auto_prerequisite_service import AutoPrerequisiteExtractor

class SyllabusIndexerTool:
    def __init__(self, vector_db: Optional[VectorDBManager] = None, db_client: Optional[FluxbaseClient] = None):
        self.vector_db = vector_db or VectorDBManager()
        self.db = db_client or FluxbaseClient()
        self.auto_prereq = AutoPrerequisiteExtractor()

    def chunk_document_text(self, text: str, chunk_size: int = 500, overlap: int = 80) -> List[Dict[str, Any]]:
        """Splits raw text or slide transcripts into overlapping semantic chunks."""
        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 30]
        chunks = []
        
        current_chunk = ""
        chunk_idx = 1
        
        for p in paragraphs:
            if len(current_chunk) + len(p) < chunk_size:
                current_chunk += " " + p
            else:
                if current_chunk:
                    chunks.append({"chunk_id": f"CHUNK_{chunk_idx:03d}", "content": current_chunk.strip()})
                    chunk_idx += 1
                current_chunk = p
        
        if current_chunk:
            chunks.append({"chunk_id": f"CHUNK_{chunk_idx:03d}", "content": current_chunk.strip()})
            
        return chunks

    def index_syllabus_or_slides(
        self,
        course_id: str,
        faculty_id: str,
        raw_text: str,
        filename: str = "curriculum_slides.pptx"
    ) -> Dict[str, Any]:
        """
        Chunks content, indexes into ChromaDB vector store, extracts prerequisite DAG,
        and saves references to PostgreSQL learning_materials.
        """
        # 1. Chunking
        chunks = self.chunk_document_text(raw_text)
        if not chunks:
            chunks = [{"chunk_id": "CHUNK_001", "content": raw_text[:600]}]

        # 2. Extract curriculum prerequisite DAG
        dag_analysis = self.auto_prereq.process_syllabus_text(raw_text)

        # 3. Ingest into ChromaDB course_learning_materials
        texts = [c["content"] for c in chunks]
        metadatas = [
            {
                "course_id": course_id,
                "source_file": filename,
                "faculty_id": faculty_id,
                "chunk_id": c["chunk_id"]
            }
            for c in chunks
        ]
        ids = [f"{course_id}_{os.path.splitext(filename)[0]}_{c['chunk_id']}" for c in chunks]

        # Use ChromaDB client
        try:
            coll = self.vector_db.get_collection("course_learning_materials")
            coll.upsert(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            chroma_success = True
        except Exception as e:
            chroma_success = False

        # 4. Save metadata to learning_materials in PostgreSQL
        title = os.path.splitext(filename)[0].replace("_", " ").title()
        safe_title = title.replace("'", "''")
        clean_text_excerpt = raw_text[:800].replace("'", "''").strip()
        if not clean_text_excerpt:
            clean_text_excerpt = f"Faculty lecture materials for {title}."

        unit_name = "Curriculum Unit"
        fn_low = filename.lower()
        if "cnn" in fn_low:
            unit_name = "Unit 1: Convolutional Neural Networks"
        elif "lstm" in fn_low or "rnn" in fn_low:
            unit_name = "Unit 2: Sequence Modeling & Recurrent Networks"
        elif "transformer" in fn_low or "attention" in fn_low:
            unit_name = "Unit 3: Transformer Networks & Attention Mechanisms"
        elif "adam" in fn_low or "optimization" in fn_low:
            unit_name = "Unit 4: Deep Network Optimization & Regularization"
        elif "gan" in fn_low:
            unit_name = "Unit 5: Generative Models & Adversarial Training"

        # Check if already present to avoid duplicate records
        existing = self.db.execute_query(f"SELECT material_id FROM learning_materials WHERE file_name = '{filename}';").get("rows", [])
        if not existing:
            self.db.execute_query(f"""
                INSERT INTO learning_materials (course_id, title, material_type, unit_name, content_text, file_name, uploaded_by_faculty_id)
                VALUES (
                    '{course_id}',
                    '{safe_title}',
                    'lecture_slides',
                    '{unit_name}',
                    '{clean_text_excerpt}',
                    '{filename}',
                    '{faculty_id}'
                );
            """)

        return {
            "status": "INDEXED_AND_VECTORIZED",
            "course_id": course_id,
            "filename": filename,
            "total_chunks_created": len(chunks),
            "chroma_ingested": chroma_success,
            "prerequisite_concepts_discovered": dag_analysis.get("graph_summary", {}).get("node_count", 0),
            "dag_valid": dag_analysis.get("graph_summary", {}).get("is_dag_valid", True),
            "discovered_concepts": dag_analysis.get("graph_summary", {}).get("concepts", [])[:6],
            "summary": f"Successfully indexed {len(chunks)} chunks into ChromaDB for {course_id}."
        }

if __name__ == "__main__":
    indexer = SyllabusIndexerTool()
    print("SyllabusIndexerTool initialized successfully.")

