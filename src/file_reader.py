import re
import string

class FileReader:
  def __init__(self, file_name, should_reverse=False):
    with open(file_name, 'r') as _file:
      self.lines = _file.readlines()
      if should_reverse: self.lines.reverse()

  def all(self):

    tab = string.maketrans(
      string.ascii_uppercase + string.punctuation,
      string.ascii_lowercase + (' ' * len(string.punctuation))
    )

    _ts = string.translate
    return ((int(split[0]), frozenset(split[1:])) for split in (_ts(line, tab).split() for line in self.lines) )
