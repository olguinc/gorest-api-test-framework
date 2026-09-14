from factories import fake


def build_comment_payload(**overrides) -> dict:
    payload = {
        "name": fake.name(),
        "email": fake.unique.email(),
        "body": fake.sentence(nb_words=12),
    }
    payload.update(overrides)
    return payload
