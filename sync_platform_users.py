from student_success_platform.src.fluxbase_client import FluxbaseClient
import bcrypt

fb = FluxbaseClient()
pw_hash = bcrypt.hashpw(b"password123", bcrypt.gensalt(12)).decode("utf-8").replace("'", "''")

# 1. Sync students to platform_users
stu_res = fb.execute_query("SELECT srn, student_name, email FROM students")
for s in stu_res.get("rows", []):
    srn = s["srn"]
    name = (s["student_name"] or "").replace("'", "''")
    email = (s["email"] or "").replace("'", "''")
    num = srn.replace("R24EA", "").replace("STU-", "")
    uid = f"USR_{num}"
    
    # Upsert or check
    q = f"""
    INSERT INTO platform_users (user_id, email, hashed_password, role, entity_id, display_name, department, is_active)
    VALUES ('{uid}', '{email}', '{pw_hash}', 'student', '{srn}', '{name}', 'School of Computing & IT', TRUE)
    ON CONFLICT (user_id) DO UPDATE SET email = '{email}', display_name = '{name}', entity_id = '{srn}';
    """
    res = fb.execute_query(q)
    print(f"Synced student {srn} ({email}): {res.get('success')}")

# 2. Sync faculty to platform_users
fac_res = fb.execute_query("SELECT faculty_id, name, email FROM faculty")
for f in fac_res.get("rows", []):
    fid = f["faculty_id"]
    name = (f["name"] or "").replace("'", "''")
    email = (f["email"] or "").replace("'", "''")
    uid = f"USR_{fid.replace('-', '_')}"
    q = f"""
    INSERT INTO platform_users (user_id, email, hashed_password, role, entity_id, display_name, department, is_active)
    VALUES ('{uid}', '{email}', '{pw_hash}', 'faculty', '{fid}', '{name}', 'School of Computing & IT', TRUE)
    ON CONFLICT (user_id) DO UPDATE SET email = '{email}', display_name = '{name}', entity_id = '{fid}';
    """
    res = fb.execute_query(q)
    print(f"Synced faculty {fid} ({email}): {res.get('success')}")

# 3. Ensure Sumith U has both student and faculty entries with sumithu.dev@gmail.com
fb.execute_query(f"""
INSERT INTO platform_users (user_id, email, hashed_password, role, entity_id, display_name, department, is_active)
VALUES ('USR_807', 'sumithu.dev@gmail.com', '{pw_hash}', 'student', 'R24EA807', 'Sumith U', 'School of Computing & IT', TRUE)
ON CONFLICT (user_id) DO UPDATE SET email = 'sumithu.dev@gmail.com', display_name = 'Sumith U', entity_id = 'R24EA807', hashed_password = '{pw_hash}';
""")

fb.execute_query(f"""
INSERT INTO platform_users (user_id, email, hashed_password, role, entity_id, display_name, department, is_active)
VALUES ('USR_FAC_SUMITH', 'sumithu.dev@gmail.com', '{pw_hash}', 'faculty', 'FAC_AIML_00', 'Sumith U (Faculty Lead)', 'School of Computing & IT', TRUE)
ON CONFLICT (user_id) DO UPDATE SET email = 'sumithu.dev@gmail.com', display_name = 'Sumith U (Faculty Lead)', entity_id = 'FAC_AIML_00', hashed_password = '{pw_hash}';
""")
print("All users synchronized in platform_users!")

