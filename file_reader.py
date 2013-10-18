import re
import string

class FileReader:
  def __init__(self, file_name):
    with open(file_name, 'r') as _file: self.lines = _file.readlines()

  def all(self):
    lowers = string.ascii_lowercase + ' '
    uppers = string.ascii_uppercase + ' '
    digits = string.digits

    letter_set = frozenset(lowers + uppers + digits)

    deletions = ''.join(ch for ch in map(chr,range(256)) if ch not in letter_set)

    tab = string.maketrans(
      lowers + uppers + digits + deletions,
      (lowers * 2) + digits + (' ' * len(deletions))
    )

    _ts = string.translate
    return ((split[0], set(split[1:])) for split in (_ts(line, tab).split() for line in self.lines))
