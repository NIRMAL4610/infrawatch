from .database import get_recent_metrics


def show_history():
    rows = get_recent_metrics(10)

    print("\nLast 10 measurements\n")
    print("Date         Time         CPU     Memory   Disk")

    for timestamp, cpu, memory, disk in reversed(rows):
        date = timestamp[:10]
        time = timestamp[11:19]
        print(f"{date}   {time}   {cpu:>5}% {memory:>7}% {disk:>6}%")
