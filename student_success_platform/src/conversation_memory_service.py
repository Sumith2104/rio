"""
Multi-Turn Conversational Memory & Tutoring Session Service (PACD-RAG)
=====================================================================
Author: Sumith U (SRN: R24EA807) | 7th Sem B.Tech CSE (AI & ML), Section B, REVA University
Project: AI-Powered Smart Campus Intelligence & Student Success Platform

Maintains stateful multi-turn dialogue memory across student tutoring queries.
Enriches follow-up questions with previous conversation history, tracks learning
state, and logs student misconceptions across turns.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import uuid

class ConversationMemoryService:
    def __init__(self, max_history_turns: int = 6):
        self.max_history_turns = max_history_turns
        # In-memory session store (can sync with PostgreSQL/Fluxbase)
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def get_or_create_session(self, student_srn: str, course_id: str, session_id: Optional[str] = None) -> str:
        """Retrieves an existing session or initializes a new contextual dialogue session."""
        if not session_id or session_id not in self.sessions:
            session_id = session_id or f"SES_{student_srn}_{course_id}_{uuid.uuid4().hex[:8]}"
            self.sessions[session_id] = {
                "session_id": session_id,
                "student_srn": student_srn,
                "course_id": course_id,
                "created_at": datetime.now().isoformat(),
                "last_active": datetime.now().isoformat(),
                "turns": [],
                "active_topics": [],
                "misconceptions_identified": [],
                "turn_count": 0
            }
        return session_id

    def add_interaction(
        self,
        session_id: str,
        user_query: str,
        assistant_response: str,
        retrieved_contexts: Optional[List[str]] = None,
        faithfulness_score: Optional[float] = None
    ) -> Dict[str, Any]:
        """Appends a user-assistant dialogue turn to conversational memory."""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found.")

        sess = self.sessions[session_id]
        sess["turn_count"] += 1
        sess["last_active"] = datetime.now().isoformat()

        turn_entry = {
            "turn_number": sess["turn_count"],
            "timestamp": datetime.now().isoformat(),
            "user_query": user_query,
            "assistant_response": assistant_response,
            "retrieved_contexts_count": len(retrieved_contexts or []),
            "faithfulness_score": faithfulness_score
        }
        sess["turns"].append(turn_entry)

        # Enforce rolling buffer window
        if len(sess["turns"]) > self.max_history_turns:
            sess["turns"] = sess["turns"][-self.max_history_turns:]

        return {
            "session_id": session_id,
            "turn_number": sess["turn_count"],
            "buffered_turns_count": len(sess["turns"]),
            "status": "RECORDED"
        }

    def enrich_query_with_history(self, session_id: str, current_query: str) -> str:
        """
        Resolves pronouns and context from recent conversation turns to form
        a semantically complete retrieval query for vector search.
        """
        if session_id not in self.sessions:
            return current_query

        sess = self.sessions[session_id]
        recent_turns = sess["turns"][-2:]
        if not recent_turns:
            return current_query

        # Construct context summary for LLM / vector retrieval
        history_snippets = []
        for t in recent_turns:
            history_snippets.append(f"Student asked: {t['user_query']}")
            # Extract first sentence of previous assistant answer
            first_sent = t['assistant_response'].split('.')[0]
            if first_sent:
                history_snippets.append(f"AI explained: {first_sent.strip()}")

        context_prefix = " | ".join(history_snippets)
        enriched_prompt = f"[Context: {context_prefix}] Follow-up Question: {current_query}"
        return enriched_prompt

    def get_session_history(self, session_id: str) -> Dict[str, Any]:
        """Returns the complete structured conversation memory for the session."""
        if session_id not in self.sessions:
            return {"error": "Session not found", "session_id": session_id}
        return self.sessions[session_id]

if __name__ == "__main__":
    mem = ConversationMemoryService()
    s_id = mem.get_or_create_session("R24EA807", "AIML-401")
    
    # Turn 1
    mem.add_interaction(
        session_id=s_id,
        user_query="Can you explain Backpropagation in Deep Learning?",
        assistant_response="Backpropagation is an algorithm to compute gradients of the loss function using the chain rule.",
        faithfulness_score=0.88
    )
    
    # Turn 2 - Follow up with pronoun 'it'
    enriched = mem.enrich_query_with_history(s_id, "How does it use the chain rule?")
    print("Enriched retrieval query:")
    print(enriched)
    print("\nSession state:")
    print(json.dumps(mem.get_session_history(s_id), indent=2))

