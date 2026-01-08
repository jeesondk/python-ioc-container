"""Example usage of the python-ioc package."""

# ─────────────────────────────────────────────────────────────────────────────
# Example usage
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from abc import ABC, abstractmethod
    from j2_ioc import Container, Lifetime
    from j2_ioc.errors import (
        CircularDependencyError,
        ContainerError,
        MissingDependencyError
    )

    # ── Define abstractions ──────────────────────────────────────────────────

    class Config(ABC):
        @abstractmethod
        def get(self, key: str) -> str: ...

    class UserRepository(ABC):
        @abstractmethod
        def get(self, user_id: int) -> dict: ...

    class EmailSender(ABC):
        @abstractmethod
        def send(self, to: str, body: str) -> None: ...

    class Cache(ABC):
        @abstractmethod
        def get(self, key: str) -> object | None: ...
        @abstractmethod
        def set(self, key: str, value: object) -> None: ...

    # ── Implementations ──────────────────────────────────────────────────────

    class EnvConfig(Config):
        def __init__(self):
            self._values = {"db_url": "postgresql://localhost/app"}

        def get(self, key: str) -> str:
            return self._values.get(key, "")

    class PostgresUserRepository(UserRepository):
        def __init__(self, config: Config):
            self.config = config
            print(f"  [PostgresUserRepository] Connected to {config.get('db_url')}")

        def get(self, user_id: int) -> dict:
            print(f"  [PostgresUserRepository] Fetching user {user_id} from DB")
            return {"id": user_id, "email": f"user{user_id}@example.com"}

    class InMemoryCache(Cache):
        def __init__(self):
            self._store: dict[str, object] = {}

        def get(self, key: str) -> object | None:
            result = self._store.get(key)
            print(f"  [Cache] GET {key} -> {'HIT' if result else 'MISS'}")
            return result

        def set(self, key: str, value: object) -> None:
            print(f"  [Cache] SET {key}")
            self._store[key] = value

    # ── Decorator ────────────────────────────────────────────────────────────

    class CachedUserRepository(UserRepository):
        """Decorator that adds caching to any UserRepository."""

        def __init__(self, inner: UserRepository, cache: Cache):
            self.inner = inner
            self.cache = cache

        def get(self, user_id: int) -> dict:
            key = f"user:{user_id}"
            cached = self.cache.get(key)
            if cached:
                return cached
            result = self.inner.get(user_id)
            self.cache.set(key, result)
            return result

    class SmtpEmailSender(EmailSender):
        def __init__(self, users: UserRepository):
            self.users = users

        def send(self, to: str, body: str) -> None:
            print(f"  [SmtpEmailSender] Sending to {to}: {body}")

    # ── Factory function (dependencies injected via type hints) ────────────

    def create_connection_string(config: Config) -> str:
        """Factory functions can have dependencies injected too."""
        return f"Connection to {config.get('db_url')}"

    # ── Configure container ──────────────────────────────────────────────────

    print("=" * 60)
    print("Setting up container...")
    print("=" * 60)

    container = (
        Container()
        # Singleton config - shared everywhere
        .singleton(Config, EnvConfig)
        # Singleton cache
        .singleton(Cache, InMemoryCache)
        # Scoped repository - one per scope
        .scoped(UserRepository, PostgresUserRepository)
        # Add caching decorator
        .decorate(UserRepository, CachedUserRepository)
        # Transient email sender - new instance each time
        .transient(EmailSender, SmtpEmailSender)
        # Factory example - dependency injection works in factories too
        .factory(
            str,  # Just for demo - normally wouldn't register str
            create_connection_string,
            Lifetime.SINGLETON
        )
    )

    # Validate configuration
    print("\nValidating container configuration...")
    container.validate()
    print("✓ Container configuration is valid")

    # ── Use the container ────────────────────────────────────────────────────

    print("\n" + "=" * 60)
    print("Scope 1: First request")
    print("=" * 60)

    with container.scope() as scope:
        print("\nResolving EmailSender...")
        sender = scope.resolve(EmailSender)

        print("\nFetching user 1 (should hit DB)...")
        user_repo = scope.resolve(UserRepository)
        user = user_repo.get(1)
        print(f"Got user: {user}")

        print("\nFetching user 1 again (should hit cache)...")
        user = user_repo.get(1)
        print(f"Got user: {user}")

    print("\n" + "=" * 60)
    print("Scope 2: Second request (new scope, same singletons)")
    print("=" * 60)

    with container.scope() as scope:
        print("\nResolving UserRepository (new scoped instance)...")
        user_repo = scope.resolve(UserRepository)

        print("\nFetching user 1 (cache is singleton, should still hit)...")
        user = user_repo.get(1)
        print(f"Got user: {user}")

        print("\nFetching user 2 (should hit DB)...")
        user = user_repo.get(2)
        print(f"Got user: {user}")

    # ── Demonstrate validation errors ────────────────────────────────────────

    print("\n" + "=" * 60)
    print("Validation examples")
    print("=" * 60)

    # Missing dependency
    print("\n1. Missing dependency:")
    try:
        class NeedsUnregistered:
            def __init__(self, missing: "UnregisteredService"): ...

        class UnregisteredService: ...

        bad_container = Container().transient(NeedsUnregistered)
        bad_container.validate()
    except MissingDependencyError as e:
        print(f"   ✓ Caught: {e}")

    # Circular dependency
    print("\n2. Circular dependency:")
    try:
        class ServiceA:
            def __init__(self, b: "ServiceB"): ...

        class ServiceB:
            def __init__(self, a: ServiceA): ...

        bad_container = (
            Container()
            .transient(ServiceA)
            .transient(ServiceB)
        )
        bad_container.validate()
    except CircularDependencyError as e:
        print(f"   ✓ Caught: {e}")

    # Lifetime mismatch
    print("\n3. Lifetime mismatch (singleton depending on scoped):")
    try:
        class ScopedService: ...

        class SingletonNeedsScoped:
            def __init__(self, scoped: ScopedService): ...

        bad_container = (
            Container()
            .scoped(ScopedService)
            .singleton(SingletonNeedsScoped)
        )
        bad_container.validate()
    except ContainerError as e:
        print(f"   ✓ Caught: {e}")

    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)
