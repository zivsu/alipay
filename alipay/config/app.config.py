    #!/usr/bin/env python
# coding: utf-8

urls = 'app'

db = {
    "driver": "mysql",
    "username": "root",
    "password": "",
    "host": "localhost",
    "port": 3306,
    "database": "alipay_local"
}

cookie_secret = "636f531befd9491382a233a92936589d"
xsrf_cookies = False
debug = True
autoreload = True

port = 8080

ENV_LOCAL = "local"
ENV_QA = "qa"
ENV_PROD = "prod"

PROXY_HOST = ""

# ali pay
ali_app_id = ""
ali_seller_id = ""
ali_sign_type = "RSA2"
ali_gateway = "https://openapi.alipaydev.com/gateway.do"

import os
_current_folder_path = os.path.dirname(os.path.abspath(__file__))
private_key_path = _current_folder_path + "/app_private_key.crt"
public_key_path = _current_folder_path + "/app_public_key.crt"
ali_public_key_path = _current_folder_path + "/ali_public_key.crt"