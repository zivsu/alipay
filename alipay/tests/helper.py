import uuid

def gen_uid():
    return str(uuid.uuid4()).replace("-", "")
