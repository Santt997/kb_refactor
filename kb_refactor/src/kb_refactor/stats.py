from dataclasses import dataclass, field
from collections import Counter

@dataclass
class Stats:
    ipynbs: int = 0
    md_cells: int = 0
    internal_links: int = 0

    refs: Counter = field(default_factory=Counter)

    def add_reference(self, kbid: str):
        self.internal_links += 1
        self.refs[kbid] += 1

    def report(self) -> None:
        print('\nKB stats\n')
        print(f'IPYNBs:       {self.ipynbs}')
        print(f'Md cells:  {self.md_cells}')
        print(f'Internal links:  {self.internal_links}')

        if self.refs:
            print('\nTop referenced:')
            for kbid, count in self.refs.most_common(20):
                print(f'  {kbid:<40} {count}')