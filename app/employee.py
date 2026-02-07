import random
import string

def generate_employee_id():
    return "EMP-" + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=6)
    )
