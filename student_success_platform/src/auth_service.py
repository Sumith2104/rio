"""
=============================================================================
AUTHENTICATION & AUDIT LOGGING SERVICE
AI-Powered Agentic Smart Campus Intelligence & Student Success Platform
Author: Sumith U (SRN: R24EA807), 7th Sem B.Tech CSE (AI & ML), REVA University
=============================================================================
Provides:
  1. Role-based Authentication (student, faculty, admin) with bcrypt password verification.
  2. Stateless JWT access token issuance and signature verification.
  3. Relational Audit Logging into Fluxbase Cloud PostgreSQL (`audit_logs`, `data_change_log`, `ai_call_log`).
  4. Vector Audit Logging into ChromaDB (`system_audit_logs`) for fast semantic trace queries.
=============================================================================
"""

import os
import sys
import time
import uuid
import json
import secrets
import subprocess
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional

import bcrypt
import jwt

# Include current directory in path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from fluxbase_client import FluxbaseClient
from vector_db_manager import VectorDBManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Security configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "reva-smart-campus-jwt-secret-key-2026-sumith-u-r24ea807")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24


class AuthService:
    """Enterprise-grade Auth and Auditing manager."""

    def __init__(self):
        self.flux_db = FluxbaseClient()
        self.vdb = VectorDBManager(host="localhost", port=8001)
        self.audit_collection = "system_audit_logs"
        self._active_otps: Dict[str, Dict[str, Any]] = {}

    # -------------------------------------------------------------------------
    # Password Utilities
    # -------------------------------------------------------------------------
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a plain text password using bcrypt."""
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify plain password against stored bcrypt hash."""
        try:
            return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False

    # -------------------------------------------------------------------------
    # JWT Token Operations
    # -------------------------------------------------------------------------
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Issue signed JWT access token containing user identity and role claims."""
        to_encode = data.copy()
        now = datetime.now(timezone.utc)
        expire = now + (expires_delta or timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS))
        to_encode.update({
            "iat": int(now.timestamp()),
            "exp": int(expire.timestamp()),
            "iss": "reva-smart-campus-platform",
            "jti": str(uuid.uuid4())
        })
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        if isinstance(encoded_jwt, bytes):
            return encoded_jwt.decode("utf-8")
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> Dict[str, Any]:
        """Decode and validate a JWT access token."""
        try:
            if isinstance(token, bytes):
                token = token.decode("utf-8")
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token signature has expired. Please log in again.")
        except Exception as e:
            raise ValueError(f"Invalid token: {e}")

    # -------------------------------------------------------------------------
    # User Authentication
    # -------------------------------------------------------------------------
    def authenticate_user(
        self,
        identifier: str,
        password: str,
        role: Optional[str] = None,
        ip_address: str = "127.0.0.1"
    ) -> Dict[str, Any]:
        """
        Authenticate user by email, user_id, or entity_id (SRN/Faculty ID).
        Verifies credentials against platform_users and logs the attempt to audit_logs.
        """
        clean_id = identifier.strip().replace("'", "''")
        # Support friendly aliases
        alias_map = {
            "student.profile@reva.edu.in": "sumith.u@reva.edu.in",
            "student.ontrack@reva.edu.in": "sumith.u@reva.edu.in",
            "student.lowrisk@reva.edu.in": "sumith.u@reva.edu.in",
            "student.atrisk@reva.edu.in": "vikram.p@reva.edu.in",
            "student.highrisk@reva.edu.in": "vikram.p@reva.edu.in",
            "faculty.lead@reva.edu.in": "ramesh.kumar@reva.edu.in",
            "faculty.advisor@reva.edu.in": "ramesh.kumar@reva.edu.in",
            "faculty.mentor@reva.edu.in": "ananya.s@reva.edu.in"
        }
        if clean_id.lower() in alias_map:
            clean_id = alias_map[clean_id.lower()]

        extra_condition = ""
        if clean_id.upper().startswith("STU-"):
            num = clean_id.upper().replace("STU-", "")
            extra_condition = f" OR LOWER(user_id) = 'usr_{num.lower()}' OR LOWER(entity_id) = 'r24ea{num.lower()}'"
        elif clean_id.upper().startswith("FAC"):
            clean_fac = clean_id.upper().replace("FAC-", "").replace("FAC_", "").replace("FAC", "")
            if clean_fac:
                extra_condition = f" OR LOWER(entity_id) LIKE '%{clean_fac.lower()}%' OR LOWER(user_id) LIKE '%{clean_fac.lower()}%'"

        role_clause = f" AND role = '{role}'" if role else ""
        sql = f"""
        /* auth_nonce={time.time_ns()} */
        SELECT user_id, email, hashed_password, role, entity_id, display_name, department, is_active
        FROM platform_users
        WHERE (LOWER(email) = LOWER('{clean_id}') 
           OR LOWER(user_id) = LOWER('{clean_id}') 
           OR LOWER(entity_id) = LOWER('{clean_id}'){extra_condition}){role_clause};
        """
        res = self.flux_db.execute_query(sql)
        rows = res.get("rows", [])

        if not rows:
            self.log_audit_event(
                actor_id=identifier,
                actor_role="anonymous",
                action="USER_LOGIN_FAILED",
                resource="auth",
                resource_id=identifier,
                ip_address=ip_address,
                status="FAILED",
                detail={"error": "User account does not exist"}
            )
            return {"authenticated": False, "message": "Invalid email/username or password."}

        user = rows[0]
        if not user.get("is_active", True):
            return {"authenticated": False, "message": "Account has been deactivated. Contact IT helpdesk."}

        # Verify password
        if not self.verify_password(password, user["hashed_password"]):
            self.log_audit_event(
                actor_id=user["user_id"],
                actor_role=user["role"],
                action="USER_LOGIN_FAILED",
                resource="auth",
                resource_id=user["entity_id"],
                ip_address=ip_address,
                status="FAILED",
                detail={"error": "Incorrect password provided"}
            )
            return {"authenticated": False, "message": "Invalid email/username or password."}

        # Create JWT token
        token_claims = {
            "sub": user["user_id"],
            "user_id": user["user_id"],
            "role": user["role"],
            "entity_id": user["entity_id"],
            "email": user["email"],
            "display_name": user["display_name"],
            "department": user.get("department", "School of Computing & IT")
        }
        access_token = self.create_access_token(token_claims)

        # Log successful login to both DB and ChromaDB
        self.log_audit_event(
            actor_id=user["user_id"],
            actor_role=user["role"],
            action="USER_LOGIN_SUCCESS",
            resource="auth",
            resource_id=user["entity_id"],
            ip_address=ip_address,
            status="SUCCESS",
            detail={"display_name": user["display_name"], "department": user.get("department")}
        )

        return {
            "authenticated": True,
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "user_id": user["user_id"],
                "email": user["email"],
                "role": user["role"],
                "entity_id": user["entity_id"],
                "display_name": user["display_name"],
                "department": user.get("department")
            }
        }

    # -------------------------------------------------------------------------
    # SMTP Nodemailer OTP Authentication (Dual-Role: Student & Faculty)
    # -------------------------------------------------------------------------
    def find_user(self, identifier: str, role: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Look up user record by email, user_id, or entity_id (SRN/Faculty ID)."""
        clean_id = identifier.strip().replace("'", "''")
        alias_map = {
            "sumith.u@reva.edu.in": "sumithu.dev@gmail.com",
            "student.profile@reva.edu.in": "sumithu.dev@gmail.com",
            "student.ontrack@reva.edu.in": "sumithu.dev@gmail.com",
            "student.lowrisk@reva.edu.in": "sumithu.dev@gmail.com",
            "student.atrisk@reva.edu.in": "vikram.p@reva.edu.in",
            "student.highrisk@reva.edu.in": "vikram.p@reva.edu.in",
            "faculty.lead@reva.edu.in": "ramesh.kumar@reva.edu.in",
            "faculty.advisor@reva.edu.in": "ramesh.kumar@reva.edu.in",
            "faculty.mentor@reva.edu.in": "ananya.s@reva.edu.in"
        }
        if clean_id.lower() in alias_map:
            clean_id = alias_map[clean_id.lower()]

        extra_condition = ""
        if clean_id.upper().startswith("STU-"):
            num = clean_id.upper().replace("STU-", "")
            extra_condition = f" OR LOWER(user_id) = 'usr_{num.lower()}' OR LOWER(entity_id) = 'r24ea{num.lower()}'"
        elif clean_id.upper().startswith("FAC"):
            clean_fac = clean_id.upper().replace("FAC-", "").replace("FAC_", "").replace("FAC", "")
            if clean_fac:
                extra_condition = f" OR LOWER(entity_id) LIKE '%{clean_fac.lower()}%' OR LOWER(user_id) LIKE '%{clean_fac.lower()}%'"

        role_filter = ""
        if role and role.strip():
            role_filter = f" AND LOWER(role) = '{role.strip().lower()}'"

        sql = f"""
        /* auth_nonce={time.time_ns()} */
        SELECT user_id, email, hashed_password, role, entity_id, display_name, department, is_active
        FROM platform_users
        WHERE (LOWER(email) = LOWER('{clean_id}') 
           OR LOWER(user_id) = LOWER('{clean_id}') 
           OR LOWER(entity_id) = LOWER('{clean_id}'){extra_condition}){role_filter};
        """
        res = self.flux_db.execute_query(sql)
        rows = res.get("rows", [])
        if rows:
            return rows[0]

        if role_filter:
            fallback_sql = f"""
            /* auth_nonce={time.time_ns()} */
            SELECT user_id, email, hashed_password, role, entity_id, display_name, department, is_active
            FROM platform_users
            WHERE LOWER(email) = LOWER('{clean_id}') 
               OR LOWER(user_id) = LOWER('{clean_id}') 
               OR LOWER(entity_id) = LOWER('{clean_id}'){extra_condition};
            """
            fallback_res = self.flux_db.execute_query(fallback_sql)
            fallback_rows = fallback_res.get("rows", [])
            return fallback_rows[0] if fallback_rows else None

        return None

    def request_otp(
        self,
        identifier: str,
        role: Optional[str] = None,
        ip_address: str = "127.0.0.1"
    ) -> Dict[str, Any]:
        """
        Dispatches a 6-digit OTP code to the user's email via SMTP Protocol using Nodemailer.
        Supports both 'student' and 'faculty' user roles.
        """
        user = self.find_user(identifier, role=role)
        if not user:
            self.log_audit_event(
                actor_id=identifier,
                actor_role="anonymous",
                action="OTP_REQUEST_FAILED",
                resource="auth",
                resource_id=identifier,
                ip_address=ip_address,
                status="FAILED",
                detail={"error": "User identifier not recognized"}
            )
            return {
                "success": False,
                "message": f"Account '{identifier}' was not found. Please verify your SRN, Faculty ID, or University email."
            }

        if not user.get("is_active", True):
            return {"success": False, "message": "Account has been deactivated. Please contact campus IT helpdesk."}

        # Role consistency check (if role is specified)
        if role and role.strip().lower() != user["role"].lower():
            return {
                "success": False,
                "message": f"Role mismatch: This account is registered as a {user['role'].upper()}, not {role.upper()}."
            }

        # Generate cryptographic 6-digit code
        otp = f"{secrets.randbelow(900000) + 100000}"
        expires_at = time.time() + 600  # 10 minutes

        otp_data = {
            "otp": otp,
            "expires_at": expires_at,
            "user": user,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "attempts": 0
        }

        # Register active OTP
        self._active_otps[user["email"].lower()] = otp_data
        if user.get("entity_id"):
            self._active_otps[user["entity_id"].lower()] = otp_data
        if user.get("user_id"):
            self._active_otps[user["user_id"].lower()] = otp_data

        # Execute Node.js Nodemailer SMTP Dispatcher
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        mailer_script = os.path.join(root_dir, "smtp_mailer.js")

        preview_url = None
        transport_type = "smtp-nodemailer"
        try:
            cmd = [
                "node",
                mailer_script,
                "--to", user["email"],
                "--otp", otp,
                "--role", user["role"],
                "--name", user["display_name"],
                "--entityId", user.get("entity_id", "")
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if proc.returncode == 0 and proc.stdout:
                mail_res = json.loads(proc.stdout)
                preview_url = mail_res.get("previewUrl")
                transport_type = mail_res.get("transport", "smtp-nodemailer")
            else:
                logger.warning(f"Nodemailer returned warning: {proc.stderr}")
        except Exception as e:
            logger.error(f"Error calling smtp_mailer.js: {e}")

        # Record Institutional Audit Event
        self.log_audit_event(
            actor_id=user["user_id"],
            actor_role=user["role"],
            action="OTP_DISPATCHED",
            resource="auth",
            resource_id=user["entity_id"],
            ip_address=ip_address,
            status="SUCCESS",
            detail={
                "transport": transport_type,
                "recipient_email": user["email"],
                "role": user["role"],
                "preview_url": preview_url
            }
        )

        email_parts = user["email"].split("@")
        masked_email = user["email"]
        if len(email_parts) == 2 and len(email_parts[0]) > 2:
            u = email_parts[0]
            masked_email = f"{u[0]}***{u[-1]}@{email_parts[1]}"

        return {
            "success": True,
            "message": f"Verification code dispatched via Nodemailer SMTP to {masked_email}",
            "email": user["email"],
            "masked_email": masked_email,
            "entity_id": user["entity_id"],
            "display_name": user["display_name"],
            "role": user["role"],
            "department": user.get("department", "School of Computing & IT"),
            "expires_in": 600,
            "preview_url": preview_url,
            "dev_otp": otp  # Included for instant UI testing feedback
        }

    def verify_otp(
        self,
        identifier: str,
        otp: str,
        ip_address: str = "127.0.0.1"
    ) -> Dict[str, Any]:
        """
        Verifies 6-digit OTP code sent via Nodemailer SMTP.
        On success, issues signed JWT access token and logs audit trail.
        """
        clean_key = identifier.strip().lower()
        user = self.find_user(clean_key)
        otp_data = None
        if user:
            otp_data = (
                self._active_otps.get(user["email"].lower()) or
                self._active_otps.get((user.get("entity_id") or "").lower()) or
                self._active_otps.get((user.get("user_id") or "").lower())
            )
        if not otp_data:
            otp_data = self._active_otps.get(clean_key)

        if not otp_data:
            self.log_audit_event(
                actor_id=identifier,
                actor_role="anonymous",
                action="USER_LOGIN_FAILED",
                resource="auth",
                resource_id=identifier,
                ip_address=ip_address,
                status="FAILED",
                detail={"error": "No OTP requested or session expired"}
            )
            return {
                "authenticated": False,
                "message": "No active verification code found. Please click 'Send Verification Code' first."
            }

        # Check expiration (10 min)
        if time.time() > otp_data["expires_at"]:
            return {
                "authenticated": False,
                "message": "Verification code has expired. Please request a new code."
            }

        # Check code match
        if otp.strip() != otp_data["otp"].strip():
            otp_data["attempts"] = otp_data.get("attempts", 0) + 1
            self.log_audit_event(
                actor_id=otp_data["user"]["user_id"],
                actor_role=otp_data["user"]["role"],
                action="USER_LOGIN_FAILED",
                resource="auth",
                resource_id=otp_data["user"]["entity_id"],
                ip_address=ip_address,
                status="FAILED",
                detail={"error": "Incorrect OTP code", "attempts": otp_data["attempts"]}
            )
            return {
                "authenticated": False,
                "message": "Invalid verification code. Please check your email or test preview link."
            }

        # Authenticated successfully!
        user = otp_data["user"]

        # Evict OTP
        self._active_otps.pop(user["email"].lower(), None)
        if user.get("entity_id"):
            self._active_otps.pop(user["entity_id"].lower(), None)
        if user.get("user_id"):
            self._active_otps.pop(user["user_id"].lower(), None)

        # Issue JWT Access Token
        token_claims = {
            "sub": user["user_id"],
            "user_id": user["user_id"],
            "role": user["role"],
            "entity_id": user["entity_id"],
            "email": user["email"],
            "display_name": user["display_name"],
            "department": user.get("department", "School of Computing & IT")
        }
        access_token = self.create_access_token(token_claims)

        # Log institutional audit event
        self.log_audit_event(
            actor_id=user["user_id"],
            actor_role=user["role"],
            action="USER_LOGIN_SUCCESS",
            resource="auth",
            resource_id=user["entity_id"],
            ip_address=ip_address,
            status="SUCCESS",
            detail={
                "method": "SMTP_NODEMAILER_OTP",
                "display_name": user["display_name"],
                "role": user["role"]
            }
        )

        return {
            "authenticated": True,
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "user_id": user["user_id"],
                "email": user["email"],
                "role": user["role"],
                "entity_id": user["entity_id"],
                "display_name": user["display_name"],
                "department": user.get("department")
            }
        }

    # -------------------------------------------------------------------------
    # Audit Logging System (DB & ChromaDB Vector Store)
    # -------------------------------------------------------------------------
    def log_audit_event(
        self,
        actor_id: str,
        actor_role: str,
        action: str,
        resource: str,
        resource_id: Optional[str] = None,
        ip_address: str = "127.0.0.1",
        status: str = "SUCCESS",
        detail: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Record a security or institutional audit log in:
        1. Fluxbase PostgreSQL (audit_logs table)
        2. ChromaDB Vector Store (system_audit_logs collection) for semantic trace searches.
        """
        clean_actor = (actor_id or "ANONYMOUS").replace("'", "''")
        clean_role = (actor_role or "guest").replace("'", "''")
        clean_action = (action or "EVENT").replace("'", "''")
        clean_resource = (resource or "system").replace("'", "''")
        clean_resource_id = (resource_id or "").replace("'", "''")
        detail_json = json.dumps(detail or {}).replace("'", "''")

        # 1. Store in Relational DB (audit_logs uses SERIAL primary key and DEFAULT created_at)
        sql = f"""
        INSERT INTO audit_logs (actor_id, actor_role, action, resource, resource_id, ip_address, status, detail)
        VALUES ('{clean_actor}', '{clean_role}', '{clean_action}', '{clean_resource}', '{clean_resource_id}', '{ip_address}', '{status}', '{detail_json}');
        """
        try:
            self.flux_db.execute_query(sql)
        except Exception as e:
            logger.warning(f"Could not write audit log to Fluxbase DB: {e}")

        # 2. Store in ChromaDB Vector Collection for Semantic Log Auditing
        try:
            log_id = f"AUD_{int(time.time()*1000)}_{uuid.uuid4().hex[:6]}"
            now_iso = datetime.now(timezone.utc).isoformat()
            log_narrative = (
                f"Audit Event: {clean_action} by [{clean_role}] '{clean_actor}' on {clean_resource} "
                f"(ID: {clean_resource_id}). Status: {status}. Detail: {json.dumps(detail or {})}"
            )
            self.vdb.add_documents(
                collection_name=self.audit_collection,
                documents=[log_narrative],
                metadatas=[{
                    "actor_id": clean_actor,
                    "actor_role": clean_role,
                    "action": clean_action,
                    "resource": clean_resource,
                    "status": status,
                    "timestamp": now_iso
                }],
                ids=[log_id]
            )
        except Exception as e:
            logger.warning(f"Could not index audit log in ChromaDB: {e}")

    def log_data_change(
        self,
        actor_id: str,
        table_name: str,
        record_id: str,
        action_type: str,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        change_reason: str = "Automated Academic Processing"
    ) -> None:
        """Record an immutable row edit / ingestion change log in Fluxbase data_change_log."""
        clean_actor = (actor_id or "SYSTEM").replace("'", "''")
        clean_tbl = (table_name or "").replace("'", "''")
        clean_rec = (record_id or "").replace("'", "''")
        clean_type = (action_type or "UPDATE").replace("'", "''")
        old_str = json.dumps(old_values or {}).replace("'", "''")
        new_str = json.dumps(new_values or {}).replace("'", "''")
        reason_clean = change_reason.replace("'", "''")

        sql = f"""
        INSERT INTO data_change_log (actor_id, table_name, record_id, action_type, old_values, new_values, change_reason)
        VALUES ('{clean_actor}', '{clean_tbl}', '{clean_rec}', '{clean_type}', '{old_str}', '{new_str}', '{reason_clean}');
        """
        try:
            self.flux_db.execute_query(sql)
        except Exception as e:
            logger.warning(f"Could not write data change log: {e}")

    def log_ai_call(
        self,
        actor_id: str,
        task_type: str,
        model_id: str,
        prompt_summary: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        latency_ms: int = 0,
        status: str = "SUCCESS"
    ) -> None:
        """Record model inference metrics in ai_call_log for governance and cost tracking."""
        clean_actor = (actor_id or "ANONYMOUS").replace("'", "''")
        clean_task = (task_type or "RAG").replace("'", "''")
        clean_model = (model_id or "AWS_BEDROCK_CLAUDE").replace("'", "''")
        clean_summary = prompt_summary.replace("'", "''")

        sql = f"""
        INSERT INTO ai_call_log (actor_id, task_type, model_id, prompt_summary, input_tokens, output_tokens, latency_ms, status)
        VALUES ('{clean_actor}', '{clean_task}', '{clean_model}', '{clean_summary}', {input_tokens}, {output_tokens}, {int(latency_ms)}, '{status}');
        """
        try:
            self.flux_db.execute_query(sql)
        except Exception as e:
            logger.warning(f"Could not write AI call log: {e}")

    def get_recent_audit_logs(self, limit: int = 25) -> list:
        """Retrieve latest institutional audit logs."""
        sql = f"""
        SELECT * FROM audit_logs 
        ORDER BY created_at DESC 
        LIMIT {limit};
        """
        res = self.flux_db.execute_query(sql)
        return res.get("rows", [])

    def get_recent_data_changes(self, limit: int = 25) -> list:
        """Retrieve latest data change records."""
        sql = f"""
        SELECT * FROM data_change_log 
        ORDER BY created_at DESC 
        LIMIT {limit};
        """
        res = self.flux_db.execute_query(sql)
        return res.get("rows", [])
