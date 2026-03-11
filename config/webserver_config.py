from airflow.www.security import AirflowSecurityManager
from flask_appbuilder.security.manager import AUTH_DB

# Use database-backed auth
AUTH_TYPE = AUTH_DB

# This allows all users to access the UI as Admin without logging in.
# Only use this for local development!
AUTH_ROLE_PUBLIC = 'Admin'
