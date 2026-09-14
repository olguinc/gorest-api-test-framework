from factories import fake


def build_post_payload(**overrides) -> dict:
    payload = {
        "title": fake.sentence(nb_words=6),
        "body": fake.paragraph(nb_sentences=3),
    }
    payload.update(overrides)
    return payload
