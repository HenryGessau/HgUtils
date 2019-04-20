import argparse
import tqdm


def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)


def remove_dups(history):
    from_end = 1
    total_dups = 0
    print(f"Checking {len(history)} commands for duplicates...")
    with tqdm.tqdm(total=len(history)-1) as progress:
        while from_end < len(history):
            target = len(history) - from_end
            command = history[target][0]
            dups = 0
            for i in range(target - 1, -1, -1):
                if history[i][0] == command:
                    del history[i]
                    dups += 1
                    progress.update()
            total_dups += dups
            from_end += 1
            progress.update()
    print(f"Removed {total_dups} duplicates")
    return total_dups


def save_to_file(history, filename):
    filename += '.deduped'
    with open(filename, 'w') as f:
        for command, date in history:
            f.write(f'{date}\n{command}\n')
    print("Wrote to", filename)


def main(filename, minlen):
    with open(filename) as f:
        lines = f.read().splitlines()
        history = [(command.strip(), date)
                   for date, command in pairwise(lines)]
    print(f"Processing {filename} with {len(history)} commands")
    if minlen:
        shorts = 0
        print(f"Removing commands shorter than {minlen} characters...")
        for i in range(len(history) - 1, -1, -1):
            if len(history[i][0]) < minlen:
                del history[i]
                shorts += 1
        print(f"Removed {shorts} commands {minlen-1} chars or shorter.")
    remove_dups(history)
    print(f"De-duplicated history has {len(history)} commands.")
    save_to_file(history, filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Bash history file de-duplicator')
    parser.add_argument('-m', action="store", dest="minlen", type=int,
                        default=0, help='Minimum command length to save')
    parser.add_argument('history_file', action="store",
                        type=argparse.FileType('rt'))
    results = parser.parse_args()
    main(results.history_file.name, results.minlen)
