class CleanupRegistry:
    """Tracks resources created during a test so they can be deleted on teardown.

    GoRest's dataset is shared/public, so tests must not leave orphaned records
    behind across CI runs. Deletion order is last-in-first-out so children
    (comments/posts/todos) are removed before the parent user.
    """

    def __init__(self):
        self._items: list[tuple[str, int]] = []

    def register(self, resource_type: str, resource_id: int) -> None:
        self._items.append((resource_type, resource_id))

    def cleanup(self, clients: dict) -> None:
        while self._items:
            resource_type, resource_id = self._items.pop()
            client = clients[resource_type]
            delete_method = getattr(client, f"delete_{resource_type}")
            delete_method(resource_id)
