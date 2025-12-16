LOGIN_QUERY = """
SELECT idusers, email, password, name
FROM users 
WHERE email = %s
"""

REGISTER_QUERY = """
INSERT INTO users (email, password, name)
VALUES (%s, %s, %s)
"""

UPDATE_USER_QUERY = """
UPDATE users
SET 
    email = COALESCE(%s, email),
    password = COALESCE(%s, password),
    name = COALESCE(%s, name)
WHERE idusers = %s
"""
