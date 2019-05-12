import argparse
from typing import List, Tuple, Iterable


def pairwise(iterable) -> Iterable[Tuple[str, str]]:
    a = iter(iterable)
    return zip(a, a)


def normalize_history(lines: List[str]) -> List[str]:
    c = 0
    last = len(lines) - 1
    history: List[str] = []
    while c < last:
        if not lines[c].startswith('#'):
            # Multi-line command
            history[-1] += '\n' + lines[c]
            c += 1
            continue
        history.append(lines[c])  # date
        c += 1
        history.append(lines[c])  # command
        c += 1
    return history


def remove_dups(history: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    total_dups = 0
    shistory = sorted(history, key=lambda c: c[0])
    print(f"Removing duplicates ...")
    uhistory: List[Tuple[str, str]] = []
    for i in range(len(shistory) - 1):
        if shistory[i][0] == shistory[i+1][0]:
            total_dups += 1
        else:
            uhistory.append(shistory[i])
    uhistory.append(shistory[-1])
    assert len(uhistory) == len(shistory) - total_dups
    print(f"Removed {total_dups} duplicates")
    dhistory = sorted(uhistory, key=lambda d: d[1])
    return dhistory


def save_to_file(history: List[Tuple[str, str]], filename: str):
    filename += '.deduped'
    with open(filename, 'w') as f:
        for command, date in history:
            f.write(f'{date}\n{command}\n')
    print("Wrote to", filename)


def main(filename: str, minlen: int):
    with open(filename) as f:
        lines = normalize_history(f.read().splitlines())
    commands = list(pairwise(lines))
    commands_before = len(commands)
    print(f"Processing {filename} with {commands_before} commands")
    history: List[Tuple[str, str]] = [(command, date)
                                      for date, command in commands
                                      if len(command) >= minlen]
    if minlen:
        print(f"Removed {commands_before - len(history)} commands "
              f"shorter than {minlen} characters")
    dhistory = remove_dups(history)
    print(f"De-duplicated history has {len(dhistory)} commands.")
    save_to_file(dhistory, filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Bash history file de-duplicator')
    parser.add_argument('-m', action="store", dest="minlen", type=int,
                        default=0, help='Minimum command length to save')
    parser.add_argument('history_file', action="store",
                        type=argparse.FileType('rt'))
    results = parser.parse_args()
    main(results.history_file.name, results.minlen)
