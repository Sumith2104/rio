"""
=============================================================================
TOP-LEVEL HYBRID PREREQUISITE-AWARE RAG ENGINE (PACD-RAG)
AI-Powered Agentic Smart Campus Intelligence & Student Success Platform
Author: Sumith U (SRN: R24EA807) & Shreehari (SRN: R23EA116)
Faculty Guide: Dr Sailaja Thota, REVA University
=============================================================================
Implements production-grade Hybrid RAG:
  1. High-Performance Okapi BM25 Sparse Keyword Retreival
  2. ChromaDB Dense Semantic Vector Retrieval (Cosine Space)
  3. Reciprocal Rank Fusion (RRF, k=60)
  4. Ontology-Conditioned Query Expansion via Open Knowledge Format (OKF) DAG
  5. Pedagogical Re-ranking with Bloom's Taxonomy Cognitive Scaffolding
=============================================================================
"""

import os
import sys
import math
import re
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter

# Ensure src in path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from vector_db_manager import VectorDBManager
from prerequisite_graph import PrerequisiteKnowledgeGraph

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class OkapiBM25:
    """High-performance in-memory Okapi BM25 ranker for academic curriculum and slide text."""

    def __init__(self, corpus_records: List[Dict[str, Any]], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.records = corpus_records
        self.nd = len(corpus_records)
        self.stopwords = {
            "the", "and", "is", "in", "to", "of", "a", "an", "with", "for", "on", "as",
            "at", "by", "this", "that", "it", "from", "are", "be", "was", "will", "or"
        }
        
        # Tokenize corpus
        self.tokenized_corpus = [self._tokenize(r["content"]) for r in corpus_records]
        self.doc_len = [len(doc) for doc in self.tokenized_corpus]
        self.avgdl = sum(self.doc_len) / max(1, self.nd)

        # Document frequencies
        self.doc_freqs = []
        df = Counter()
        for doc in self.tokenized_corpus:
            terms = Counter(doc)
            self.doc_freqs.append(terms)
            for t in terms:
                df[t] += 1

        # Inverse Document Frequency (IDF)
        self.idf = {}
        for term, freq in df.items():
            self.idf[term] = math.log((self.nd - freq + 0.5) / (freq + 0.5) + 1.0)

    def _tokenize(self, text: str) -> List[str]:
        """Normalize and tokenize text, preserving math symbols and hyphenated terms."""
        clean = text.lower()
        tokens = re.findall(r'[a-zA-Z0-9_\-\\^]+', clean)
        return [t for t in tokens if len(t) > 1 and t not in self.stopwords]

    def search(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """Rank documents by BM25 relevance score."""
        q_tokens = self._tokenize(query)
        scores = [0.0] * self.nd

        for term in q_tokens:
            if term not in self.idf:
                continue
            idf_val = self.idf[term]
            for i, doc_terms in enumerate(self.doc_freqs):
                tf = doc_terms.get(term, 0)
                if tf == 0:
                    continue
                denom = tf + self.k1 * (1.0 - self.b + self.b * (self.doc_len[i] / max(1.0, self.avgdl)))
                scores[i] += idf_val * (tf * (self.k1 + 1.0)) / denom

        ranked_indices = sorted(range(self.nd), key=lambda i: scores[i], reverse=True)
        results = []
        for idx in ranked_indices[:top_k]:
            if scores[idx] > 0.001:
                results.append((self.records[idx], scores[idx]))
        return results


class HybridPrerequisiteRAG:
    """
    Unified Hybrid RAG Engine integrating OKF Ontological Graphs, BM25, and ChromaDB.
    """

    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.graph_json = os.path.join(base_dir, "data", "concept_prerequisites.json")
        self.pkg = PrerequisiteKnowledgeGraph(self.graph_json)
        self.vdb = VectorDBManager(host="localhost", port=8001)
        self.collection_name = "course_learning_materials"

        # Load local corpus cache for BM25
        corpus_cache_file = os.path.join(base_dir, "data", "curriculum_corpus.json")
        if os.path.exists(corpus_cache_file):
            with open(corpus_cache_file, "r", encoding="utf-8") as f:
                self.corpus_records = json.load(f)
        else:
            self.corpus_records = []
            logger.warning("curriculum_corpus.json not found; BM25 initialized with empty corpus.")

        self.bm25 = OkapiBM25(self.corpus_records) if self.corpus_records else None

    def reciprocal_rank_fusion(
        self,
        dense_results: List[Dict[str, Any]],
        sparse_results: List[Tuple[Dict[str, Any], float]],
        rrf_k: int = 60,
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Merge ranked dense vector results and sparse BM25 results using Reciprocal Rank Fusion:
            RRF_Score(d) = 1 / (k + rank_dense) + 1 / (k + rank_sparse)
        """
        rrf_scores = {}
        doc_store = {}

        # 1. Score dense rankings
        for rank, item in enumerate(dense_results, start=1):
            doc_id = item.get("id") or item.get("concept_id") or str(rank)
            doc_store[doc_id] = item
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (rrf_k + rank))

        # 2. Score sparse rankings
        for rank, (rec, bm_score) in enumerate(sparse_results, start=1):
            doc_id = rec.get("doc_id") or rec.get("concept_id")
            if doc_id not in doc_store:
                doc_store[doc_id] = {
                    "id": doc_id,
                    "concept_id": rec.get("concept_id"),
                    "title": rec.get("title"),
                    "unit": rec.get("unit"),
                    "slide_ref": rec.get("slide_ref"),
                    "bloom_taxonomy": rec.get("bloom_taxonomy"),
                    "content": rec.get("content"),
                    "primary_formula": rec.get("primary_formula")
                }
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (rrf_k + rank))

        # 3. Sort by fused RRF score
        sorted_docs = sorted(rrf_scores.keys(), key=lambda d: rrf_scores[d], reverse=True)
        fused = []
        for d in sorted_docs[:top_n]:
            item = dict(doc_store[d])
            item["rrf_score"] = round(rrf_scores[d], 6)
            fused.append(item)

        return fused

    def retrieve_hybrid_context(
        self,
        course_id: str,
        target_concept_id: str,
        query_text: str,
        include_prerequisites: bool = True,
        top_k: int = 4
    ) -> Dict[str, Any]:
        """
        Execute Ontology-Conditioned Hybrid RAG:
          1. Detect upstream prerequisite ancestors from OKF DAG.
          2. Retrieve sparse BM25 results + dense vector ChromaDB results for target query.
          3. Retrieve prerequisite foundational slides.
          4. Fuse with RRF and scaffold hierarchically.
        """
        # Step 1: Upstream prerequisite identification
        prereq_ancestors = []
        prereq_steps = []
        target_meta = {}

        if target_concept_id and target_concept_id in self.pkg.concept_catalog:
            target_meta = self.pkg.concept_catalog[target_concept_id]
            prereq_ancestors = list(self.pkg.get_all_prerequisites(target_concept_id))
            if prereq_ancestors:
                # Topologically sorted learning sequence of prerequisites
                sorted_prereqs = self.pkg.get_learning_sequence(prereq_ancestors)
                for p_id in sorted_prereqs:
                    prereq_steps.append(self.pkg.concept_catalog[p_id])

        # Step 2: Dense Vector Retrieval for target query
        dense_hits = []
        try:
            chroma_res = self.vdb.query_similar(
                collection_name=self.collection_name,
                query_text=f"{target_concept_id} {query_text}",
                n_results=top_k * 2,
                where_filter={"course_id": course_id}
            )
            for idx in range(len(chroma_res.get("ids", []))):
                doc_id = chroma_res["ids"][idx]
                meta = chroma_res["metadatas"][idx] if chroma_res["metadatas"] else {}
                text = chroma_res["documents"][idx] if chroma_res["documents"] else ""
                dist = chroma_res["distances"][idx] if chroma_res["distances"] else 1.0
                dense_hits.append({
                    "id": doc_id,
                    "concept_id": meta.get("concept_id", target_concept_id),
                    "title": meta.get("title", ""),
                    "unit": meta.get("unit", ""),
                    "slide_ref": meta.get("slide_ref", ""),
                    "bloom_taxonomy": meta.get("bloom_taxonomy", "Understand"),
                    "content": text,
                    "distance": dist
                })
        except Exception as e:
            logger.warning(f"Dense vector retrieval encountered warning: {e}")

        # Step 3: Sparse BM25 Retrieval for target query
        sparse_hits = []
        if self.bm25:
            sparse_hits = self.bm25.search(f"{target_concept_id} {query_text}", top_k=top_k * 2)

        # Step 4: Reciprocal Rank Fusion for Target Chunks
        target_fused = self.reciprocal_rank_fusion(dense_hits, sparse_hits, rrf_k=60, top_n=top_k)

        # Step 5: Prerequisite Foundational Scaffolding
        prereq_citations = []
        if include_prerequisites and prereq_steps:
            for p in prereq_steps[-3:]:  # Most immediate 3 upstream prerequisites
                pid = p["id"]
                p_query = f"{pid} {p['name']} foundational mathematical formulation"
                p_sparse = self.bm25.search(p_query, top_k=1) if self.bm25 else []
                if p_sparse:
                    p_rec = p_sparse[0][0]
                    prereq_citations.append({
                        "priority": "FOUNDATIONAL_PREREQUISITE",
                        "concept_id": pid,
                        "title": p_rec.get("title"),
                        "unit": p_rec.get("unit"),
                        "slide_ref": p_rec.get("slide_ref"),
                        "bloom_taxonomy": p_rec.get("bloom_taxonomy"),
                        "primary_formula": p_rec.get("primary_formula"),
                        "excerpt": p_rec.get("content")[:1200]
                    })

        return {
            "course_id": course_id,
            "target_concept": {
                "id": target_concept_id,
                "name": target_meta.get("name", target_concept_id),
                "unit": target_meta.get("unit", ""),
                "bloom_taxonomy": target_meta.get("bloom_taxonomy", "Apply"),
                "primary_formula": target_meta.get("primary_formula", ""),
                "slide_ref": target_meta.get("syllabus_slide_ref", "")
            },
            "prerequisite_ancestors": [p["name"] for p in prereq_steps],
            "foundational_prerequisite_citations": prereq_citations,
            "target_retrieved_citations": [
                {
                    "concept_id": hit.get("concept_id"),
                    "title": hit.get("title"),
                    "unit": hit.get("unit"),
                    "slide_ref": hit.get("slide_ref"),
                    "bloom_taxonomy": hit.get("bloom_taxonomy"),
                    "rrf_score": hit.get("rrf_score"),
                    "excerpt": hit.get("content")[:1200]
                }
                for hit in target_fused
            ],
            "raw_fused_chunks": target_fused
        }


# Quick CLI test
if __name__ == "__main__":
    hrag = HybridPrerequisiteRAG()
    res = hrag.retrieve_hybrid_context(
        course_id="AIML-401",
        target_concept_id="DL_BACKPROP",
        query_text="Explain gradient calculation across layers with multivariable chain rule.",
        top_k=2
    )
    print("\n" + "=" * 75)
    print("  HYBRID PREREQUISITE-AWARE RAG RETRIEVAL VERIFICATION")
    print("=" * 75)
    print(f"Target Concept: {res['target_concept']['name']} ({res['target_concept']['id']})")
    print(f"Syllabus Slide: {res['target_concept']['slide_ref']}")
    print(f"Primary Formula: {res['target_concept']['primary_formula']}")
    print(f"Traced Prerequisite Ancestors: {res['prerequisite_ancestors']}")
    print(f"\nFoundational Prerequisite Citations ({len(res['foundational_prerequisite_citations'])}):")
    for cit in res["foundational_prerequisite_citations"]:
        print(f"  * [{cit['concept_id']}] {cit['title']} (Slide: {cit['slide_ref']}) | Formula: {cit['primary_formula']}")
    print(f"\nTarget Retrieved Citations ({len(res['target_retrieved_citations'])}):")
    for hit in res["target_retrieved_citations"]:
        print(f"  * [{hit['concept_id']}] {hit['title']} (Slide: {hit['slide_ref']}) | RRF Score: {hit['rrf_score']}")
    print("=" * 75 + "\n")
