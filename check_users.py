from student_success_platform.src.fluxbase_client import FluxbaseClient
import bcrypt

fb = FluxbaseClient()
res = fb.execute_query("SELECT user_id, email, hashed_password, role, entity_id, display_name FROM platform_users")
for r in res.get("rows", []):
    print(r.get("user_id"), "|", r.get("email"), "|", r.get("role"), "|", r.get("entity_id"), "|", r.get("display_name"))
    matched = None
    for pw in ["password123", "Pass@123", "admin123", "student123", "faculty123", "Sumith@123", "reva@123", "123456", "password"]:
        try:
            if bcrypt.checkpw(pw.encode(), r["hashed_password"].encode()):
                matched = pw
                break
        except Exception:
            pass
    print("   password:", matched or "UNKNOWN")

