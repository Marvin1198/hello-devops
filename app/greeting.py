"""Greeting logic, kept separate from the web layer so it is unit-testable."""


def build_greeting(name: str | None = None) -> str:
    """Return a greeting for the given name.

    An empty or whitespace-only name falls back to 'World'.
    """
    if name is None:
        return "Hello, World!"

    cleaned = name.strip()
    if not cleaned:
        return "Hello, World!"

    if len(cleaned) > 50:
        raise ValueError("name must be 50 characters or fewer")

    return f"Hello, {cleaned}!"


def is_healthy(dependencies_ok: bool = True) -> bool:
    """Report readiness.

    Real services check their dependencies here. The point is that the
    health endpoint reports on the *application*, not merely on the
    process being alive.
    """
    return bool(dependencies_ok)
