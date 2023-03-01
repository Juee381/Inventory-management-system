import os

UPLOADED_IMAGES_DEST = os.path.join("static", "images")
API_TITLE = "Stores REST API"
API_VERSION = "v1"
OPENAPI_VERSION = "3.0.3"
OPENAPI_URL_PREFIX = "/"
# OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
# OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
# SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/inventory_management_sys?unix_socket=/opt/lampp/var/mysql/mysql.sock"
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "Root@123"
MYSQL_DB = "inventory_management_system_db"
