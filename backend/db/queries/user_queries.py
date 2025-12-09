LOGIN_QUERY = "SELECT idusers, email, password FROM users WHERE email = %s"
REGISTER_QUERY = "INSERT INTO users (email, password) VALUES (%s, %s)"