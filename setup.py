from dotenv import set_key
from pathlib import Path

CURRENT_VERSION: str = "1.0.0"

REQUIRED_KEYS: list[tuple[str, None | str]] = [
    ("client_id", None),
    ("client_secret", None),
    ("client_author", "u/PepitoJuanitodeHuevo"),
    ("platform", "py310"),
    ("app_id", "RMRSSTHPGS"),
    ("ver", CURRENT_VERSION),
    ("author", "u/PepitoJuanitodeHuevo"),
    ("user_agent", "${platform}:${app_id}:${ver} (by ${author})"),
]


def main() -> None:
    env = Path(".env").absolute()
    env.touch()

    print(f"Writing to {env.as_posix()}")
    print("Obtain an id/secret from a personal use script at https://www.reddit.com/prefs/app.")

    for key, default in REQUIRED_KEYS:
        display = f"{key}:{(default and ' (optional)') or ''} "
        value = input(display) or default

        if not value:
            raise ValueError(f"Key '{key}' is required!")

        set_key(env, key, value)
        print(f"Set key '{key}' to '{value}'.")

    print("Done!")


if __name__ == "__main__":
    main()
