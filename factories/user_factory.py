from factories import fake


def build_user_payload(**overrides) -> dict:
    payload = {
        "name": fake.name(),
        "email": fake.unique.email(),
        "gender": fake.random_element(elements=("male", "female")),
        "status": fake.random_element(elements=("active", "inactive")),
    }
    payload.update(overrides)
    return payload
