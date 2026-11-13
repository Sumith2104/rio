import bcrypt
from student_success_platform.src.fluxbase_client import FluxbaseClient

client = FluxbaseClient()
check = client.execute_query("SELECT user_id, display_name FROM platform_users WHERE email = 'sailaja.thota@reva.edu.in'")
if not check.get('rows'):
    pwd_hash = bcrypt.hashpw(b'password123', bcrypt.gensalt(12)).decode('utf-8')
    insert_sql = f"""
        INSERT INTO platform_users (user_id, email, hashed_password, role, entity_id, display_name, department, is_active, created_at)
        VALUES ('USR_SAILAJA', 'sailaja.thota@reva.edu.in', '{pwd_hash}', 'faculty', 'FAC_SAILAJA_01', 'Dr Sailaja Thota', 'Department of AIML', true, NOW())
    """
    res = client.execute_query(insert_sql)
    print('Inserted Dr Sailaja Thota into platform_users:', res)
else:
    print('Dr Sailaja Thota already in platform_users:', check['rows'])
