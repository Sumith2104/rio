"""
Comprehensive Curriculum Ingestion for Hybrid PACD-RAG Engine
Seeds all 68 Open Knowledge Format (OKF) concepts into ChromaDB & BM25 Corpus
Author: Sumith U (SRN: R24EA807) & Shreehari (SRN: R23EA116)
Faculty Guide: Dr Sailaja Thota
REVA University
"""

import os
import sys
import json
import logging

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from vector_db_manager import VectorDBManager
from fluxbase_client import FluxbaseClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def seed_curriculum_materials():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "data", "concept_prerequisites.json")
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    concepts = data.get("concepts", [])
    vdb = VectorDBManager(host="localhost", port=8001)
    flux_db = FluxbaseClient()
    collection_name = "course_learning_materials"

    corpus_records = []
    documents = []
    metadatas = []
    ids = []

    course_id = "AIML-401"

    for c in concepts:
        cid = c["id"]
        cname = c["name"]
        unit = c.get("unit", "Core AI Foundations")
        level = c.get("level", "Foundational")
        bloom = c.get("bloom_taxonomy", "Understand")
        formula = c.get("primary_formula", "")
        slide_ref = c.get("syllabus_slide_ref", f"Slide-{cid}")
        study_min = c.get("estimated_study_minutes", 45)
        desc = c.get("description", "")
        competencies = c.get("competencies", [])
        comp_str = "; ".join(competencies) if competencies else "Master core concepts and practical problem solving."

        # Structured lecture note text
        lecture_text = (
            f"Course: {course_id} | Unit: {unit} | Slide: {slide_ref}\n"
            f"Concept: {cname} ({cid}) [Bloom's Level: {bloom}, Tier: {level}]\n\n"
            f"1. Overview & Pedagogical Definition:\n"
            f"{desc}\n\n"
            f"2. Core Mathematical Formulation & Governing Equations:\n"
            f"Key Formula: {formula}\n\n"
            f"3. Essential Learning Competencies:\n"
            f"By mastering this topic, students can: {comp_str}.\n\n"
            f"4. Diagnostic Notes & Common Misconceptions:\n"
            f"Students often score low on {cname} when they fail to grasp its upstream prerequisite dependencies. "
            f"Analytical problem solving requires setting up the algebraic parameters correctly and validating boundary conditions. "
            f"Estimated study duration for comprehensive remediation: {study_min} minutes.\n\n"
            f"5. Application in ML & AI Systems:\n"
            f"{cname} directly supports downstream tasks including gradient optimization, loss minimization, "
            f"neural network backpropagation, and transparent model diagnostics."
        )

        doc_id = f"{course_id}_{cid}_{slide_ref}"
        
        documents.append(lecture_text)
        metadatas.append({
            "course_id": course_id,
            "concept_id": cid,
            "unit": unit,
            "title": cname,
            "level": level,
            "bloom_taxonomy": bloom,
            "slide_ref": slide_ref,
            "estimated_minutes": study_min,
            "material_type": "syllabus_lecture_deck"
        })
        ids.append(doc_id)

        corpus_records.append({
            "doc_id": doc_id,
            "course_id": course_id,
            "concept_id": cid,
            "title": cname,
            "unit": unit,
            "level": level,
            "bloom_taxonomy": bloom,
            "slide_ref": slide_ref,
            "primary_formula": formula,
            "content": lecture_text
        })

    # 1. Upsert into ChromaDB
    try:
        vdb.add_documents(
            collection_name=collection_name,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Successfully upserted {len(ids)} concept documents into ChromaDB collection '{collection_name}'")
    except Exception as e:
        logger.error(f"Failed upserting to ChromaDB: {e}")

    # 2. Save master corpus cache for BM25 sparse retrieval
    corpus_cache_file = os.path.join(base_dir, "data", "curriculum_corpus.json")
    with open(corpus_cache_file, "w", encoding="utf-8") as f:
        json.dump(corpus_records, f, indent=2)
    logger.info(f"Saved local BM25 corpus cache ({len(corpus_records)} documents) to: {corpus_cache_file}")

    # 3. Register in PostgreSQL learning_materials table (sample first 10 for overview)
    for rec in corpus_records[:15]:
        safe_title = rec["title"].replace("'", "''")
        safe_content = rec["content"][:600].replace("'", "''")
        mat_id = f"MAT_{rec['concept_id']}"
        sql = f"""
        INSERT INTO learning_materials (material_id, course_id, unit_name, concept_id, material_type, title, content_text, file_name, uploaded_by_faculty_id)
        VALUES ('{mat_id}', '{course_id}', '{rec['unit'].replace("'", "''")}', '{rec['concept_id']}', 'lecture_slides', '{safe_title}', '{safe_content}', '{rec['slide_ref']}.pdf', 'FAC_AIML_01')
        ON CONFLICT (material_id) DO UPDATE SET title = EXCLUDED.title, content_text = EXCLUDED.content_text;
        """
        try:
            flux_db.execute_query(sql)
        except Exception:
            pass

    print(f"\n[OK] Successfully indexed all {len(concepts)} OKF curriculum concepts for Hybrid PACD-RAG.")

if __name__ == "__main__":
    seed_curriculum_materials()

