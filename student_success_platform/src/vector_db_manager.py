"""
=============================================================================
VECTOR DATABASE MANAGER (CHROMADB DOCKER INTEGRATION)
AI-Powered Agentic Smart Campus Intelligence & Student Success Platform
Author: Sumith U (SRN: R24EA807), 7th Sem B.Tech CSE (AI & ML), REVA University
=============================================================================
This module provides a unified interface to ChromaDB running locally via Docker
(http://localhost:8001). It creates and manages persistent vector collections for:
  1. Syllabus & Curriculum Specifications (course outcomes, modules)
  2. Lecture Notes & Slides (for Part 5 Prerequisite-Aware RAG retrieval)
  3. Question Bank & Isomorphic Drills (for PACD-RAG cognitive diagnosis)
=============================================================================
"""

import os
import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class VectorDBManager:
    """
    Manages local ChromaDB vector collections for syllabus, notes, and question banks.
    Supports Docker HTTP Client with graceful persistent local disk fallback.
    """

    # Collection Identifiers
    COLLECTION_SYLLABUS = "syllabus_collection"
    COLLECTION_NOTES = "lecture_notes_collection"
    COLLECTION_QUESTION_BANK = "question_bank_collection"

    _DOCKER_AVAILABLE: Optional[bool] = None

    def __init__(self, host: str = "localhost", port: int = 8001, local_fallback_dir: Optional[str] = None):
        """
        Initialize connection to ChromaDB.
        
        Args:
            host: ChromaDB Docker container host (default: localhost).
            port: Mapped host port (default: 8001).
            local_fallback_dir: Local path for disk persistence if Docker is unreachable.
        """
        self.host = host
        self.port = port
        self.client = None
        self.is_remote = False

        if local_fallback_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            local_fallback_dir = os.path.join(base_dir, "data", "chroma_local")

        self.local_dir = local_fallback_dir
        self._connect()

    def _connect(self) -> None:
        """Establish connection to Docker ChromaDB with fast persistent local disk fallback."""
        if VectorDBManager._DOCKER_AVAILABLE is not False:
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.3)
                result = sock.connect_ex((self.host, self.port))
                sock.close()
                if result == 0:
                    client = chromadb.HttpClient(
                        host=self.host,
                        port=self.port,
                        settings=Settings(anonymized_telemetry=False)
                    )
                    client.heartbeat()
                    self.client = client
                    self.is_remote = True
                    VectorDBManager._DOCKER_AVAILABLE = True
                    logger.info(f"Connected to local Docker ChromaDB instance at http://{self.host}:{self.port}")
                    return
                else:
                    VectorDBManager._DOCKER_AVAILABLE = False
            except Exception:
                VectorDBManager._DOCKER_AVAILABLE = False

        os.makedirs(self.local_dir, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=self.local_dir,
            settings=Settings(anonymized_telemetry=False)
        )
        self.is_remote = False

    def get_or_create_collection(self, collection_name: str, description: str = ""):
        """Retrieve existing collection or create a new one with cosine distance metric."""
        return self.client.get_or_create_collection(
            name=collection_name,
            metadata={
                "description": description,
                "hnsw:space": "cosine"
            }
        )

    def add_documents(
        self,
        collection_name: str,
        documents: List[str],
        metadatas: List[Dict[str, Any]],
        ids: List[str]
    ) -> None:
        """Add text documents and their metadata to a vector collection."""
        collection = self.get_or_create_collection(collection_name)
        collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Upserted {len(ids)} document(s) into '{collection_name}' (Total: {collection.count()})")

    def query_similar(
        self,
        collection_name: str,
        query_text: str,
        n_results: int = 3,
        where_filter: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Query a vector collection for the most semantically relevant text chunks.
        
        Args:
            collection_name: Target collection (syllabus, notes, question_bank).
            query_text: Search prompt or student question.
            n_results: Number of top results to return.
            where_filter: Optional metadata filtering (e.g., {'concept_id': 'DL_BACKPROP'}).
        """
        collection = self.get_or_create_collection(collection_name)
        kwargs: Dict[str, Any] = {
            "query_texts": [query_text],
            "n_results": min(n_results, max(1, collection.count()))
        }
        if where_filter:
            kwargs["where"] = where_filter

        results = collection.query(**kwargs)
        return {
            "query": query_text,
            "collection": collection_name,
            "ids": results["ids"][0] if results["ids"] else [],
            "documents": results["documents"][0] if results["documents"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else [],
            "distances": results["distances"][0] if results["distances"] else []
        }

    # =========================================================================
    # SEEDING REAL ACADEMIC CORPUS
    # =========================================================================

    def seed_academic_corpus(self) -> Dict[str, int]:
        """
        Seed initial academic records for Syllabus, Lecture Notes, and Question Bank
        aligned with the REVA University AIML-401 curriculum.
        """
        # 1. Syllabus Corpus
        syllabus_docs = [
            "Unit 1: Mathematical Foundations. Multivariable calculus, partial derivatives, and the chain rule for composite function differentiation. Matrix algebra and vector dot products.",
            "Unit 2: Classical Machine Learning. Convex cost functions, gradient descent optimization algorithms, logistic regression binary boundaries, and tree ensembles (Random Forest, XGBoost).",
            "Unit 3: Deep Neural Networks. Artificial neuron perceptron, non-linear activations (ReLU, Sigmoid), multi-layer dense feedforward transformations, and backpropagation gradient flow.",
            "Unit 4: Model Explainability and Trustworthy AI. Cooperative game theory, Shapley values, TreeSHAP feature attributions, and local waterfall explanations for black-box models."
        ]
        syllabus_meta = [
            {"unit": "Unit 1", "level": "Foundational", "type": "syllabus"},
            {"unit": "Unit 2", "level": "Intermediate", "type": "syllabus"},
            {"unit": "Unit 3", "level": "Advanced", "type": "syllabus"},
            {"unit": "Unit 4", "level": "Advanced", "type": "syllabus"}
        ]
        syllabus_ids = ["SYLL_U1", "SYLL_U2", "SYLL_U3", "SYLL_U4"]
        self.add_documents(self.COLLECTION_SYLLABUS, syllabus_docs, syllabus_meta, syllabus_ids)

        # 2. Lecture Notes Corpus (For Part 5 RAG Retrieval)
        notes_docs = [
            "Partial Derivatives Lecture Note: A partial derivative of a multivariable function f(x, y) with respect to x measures the instantaneous rate of change of f as x varies while holding y constant. In neural networks, weights are updated by computing dLoss/dw.",
            "Chain Rule Lecture Note: When computing the derivative of composite function z = f(y) where y = g(x), dz/dx = (dz/dy) * (dy/dx). In deep architectures with multiple hidden layers, error gradients are propagated layer-by-layer backwards using the multivariable chain rule.",
            "Backpropagation Lecture Note: Backpropagation is an efficient algorithmic application of the calculus chain rule. It calculates the gradient of the loss function with respect to every parameter in the network, flowing backward from output layer to input layer.",
            "Neural Network Training Lecture Note: End-to-end training loops consist of four repeated phases: 1) Forward pass generating predictions y_hat, 2) Loss calculation via Cross-Entropy or MSE, 3) Backward pass computing parameter gradients via Backprop, and 4) Optimizer weight update via Gradient Descent (w = w - eta * grad).",
            "Loss Functions Lecture Note: Cross-Entropy Loss measures the performance of a classification model whose output is a probability value between 0 and 1. L = -sum(y_i * log(p_i)). Minimizing cross-entropy aligns with maximum likelihood estimation.",
            "Gradient Descent Lecture Note: Gradient descent steps parameters in the opposite direction of the gradient: theta = theta - alpha * grad(J(theta)). Learning rate alpha determines step size; too large causes divergence, too small causes slow convergence."
        ]
        notes_meta = [
            {"concept_id": "MATH_DERIV", "topic": "Partial Derivatives", "unit": "Unit 1", "type": "lecture_slide"},
            {"concept_id": "MATH_CHAIN_RULE", "topic": "Chain Rule", "unit": "Unit 1", "type": "lecture_slide"},
            {"concept_id": "DL_BACKPROP", "topic": "Backpropagation", "unit": "Unit 3", "type": "lecture_slide"},
            {"concept_id": "DL_NN_TRAIN", "topic": "Neural Network Training", "unit": "Unit 3", "type": "lecture_slide"},
            {"concept_id": "ML_LOSS_FUNC", "topic": "Loss Functions", "unit": "Unit 2", "type": "lecture_slide"},
            {"concept_id": "ML_GRAD_DESC", "topic": "Gradient Descent", "unit": "Unit 2", "type": "lecture_slide"}
        ]
        notes_ids = ["NOTE_DERIV_01", "NOTE_CHAIN_01", "NOTE_BACKPROP_01", "NOTE_NNTRAIN_01", "NOTE_LOSS_01", "NOTE_GRAD_01"]
        self.add_documents(self.COLLECTION_NOTES, notes_docs, notes_meta, notes_ids)

        # 3. Question Bank Corpus (For PACD-RAG Adaptive Drills)
        qb_docs = [
            "Why is the calculus chain rule strictly required in backpropagation? Correct answer: To calculate partial derivatives of loss with respect to early hidden layer weights across composite transformations.",
            "What happens if the learning rate alpha in gradient descent is set excessively large? Correct answer: The optimizer oscillates erratically, overshoots the minimum, and may diverge to infinity.",
            "What is the mathematical definition of a partial derivative in multivariable calculus? Correct answer: The derivative with respect to one variable while treating all other variables as constant.",
            "In what direction does the gradient vector point relative to the loss surface? Correct answer: It points in the direction of greatest instantaneous rate of increase; gradient descent steps in the negative direction.",
            "Which loss function is optimal for training a binary logistic regression model? Correct answer: Binary Cross-Entropy (Log-Loss), which is strictly convex with respect to model weights."
        ]
        qb_meta = [
            {"concept_id": "MATH_CHAIN_RULE", "blooms": "Understand", "difficulty": 0.6, "type": "quiz_mcq"},
            {"concept_id": "ML_GRAD_DESC", "blooms": "Analyze", "difficulty": 0.5, "type": "quiz_mcq"},
            {"concept_id": "MATH_DERIV", "blooms": "Remember", "difficulty": 0.3, "type": "quiz_mcq"},
            {"concept_id": "ML_GRAD_DESC", "blooms": "Understand", "difficulty": 0.4, "type": "quiz_mcq"},
            {"concept_id": "ML_LOSS_FUNC", "blooms": "Apply", "difficulty": 0.5, "type": "quiz_mcq"}
        ]
        qb_ids = ["Q_CHAIN_01", "Q_GRAD_01", "Q_DERIV_01", "Q_GRAD_02", "Q_LOSS_01"]
        self.add_documents(self.COLLECTION_QUESTION_BANK, qb_docs, qb_meta, qb_ids)

        counts = {
            "syllabus_count": self.get_or_create_collection(self.COLLECTION_SYLLABUS).count(),
            "notes_count": self.get_or_create_collection(self.COLLECTION_NOTES).count(),
            "question_bank_count": self.get_or_create_collection(self.COLLECTION_QUESTION_BANK).count()
        }
        logger.info(f"Seeding completed successfully: {counts}")
        return counts


# Standalone CLI execution demonstration
if __name__ == "__main__":
    print("\n" + "=" * 75)
    print("  LOCAL CHROMADB VECTOR DATABASE VERIFICATION (DOCKER INTEGRATION)")
    print("=" * 75)

    vdb = VectorDBManager(host="localhost", port=8001)
    print(f"1. Connection Mode: {'Docker Remote HTTP (Port 8001)' if vdb.is_remote else 'Local Persistent Fallback'}")

    print("\n2. Seeding Academic Corpus (Syllabus, Notes, Question Bank)...")
    stats = vdb.seed_academic_corpus()
    for coll, count in stats.items():
        print(f"   * {coll}: {count} records indexed")

    print("\n3. Testing Semantic Vector Search:")
    query = "How do we compute gradients backward through layers in neural networks?"
    print(f"   Query: \"{query}\"")
    results = vdb.query_similar(VectorDBManager.COLLECTION_NOTES, query, n_results=2)

    print("\n   Top Semantic Matches from Lecture Notes Collection:")
    for i, (doc, meta, dist) in enumerate(zip(results["documents"], results["metadatas"], results["distances"]), 1):
        similarity = round(1.0 - dist, 4)
        print(f"\n   Match {i} (Similarity: {similarity}, Topic: {meta.get('topic')}, Concept: {meta.get('concept_id')}):")
        print(f"   \"{doc}\"")

    print("\n" + "=" * 75)
    print("  VECTOR DATABASE INITIALIZED AND FULLY OPERATIONAL.")
    print("=" * 75 + "\n")

