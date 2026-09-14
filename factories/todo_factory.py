from factories import fake


def build_todo_payload(**overrides) -> dict:
    payload = {
        "title": fake.sentence(nb_words=5),
        "due_on": fake.future_date().isoformat() + "T00:00:00.000+05:30",
        "status": fake.random_element(elements=("pending", "completed")),
    }
    payload.update(overrides)
    return payload
