from .library.Event import Event, EventCategory


def main():
    e = Event("title", "description", EventCategory.CONCERT, 10, 10, False, [])

    print(e.get())


if __name__ == "__main__":
    main()
