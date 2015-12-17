#!/usr/bin/python
# Copyright 2013 Tomas Popela <tpopela@redhat.com>
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import re

if __name__ == "__main__":
  path = "%s/ffmpeg_generated.gypi" % sys.argv[1]
  arch_only_x86 = False if sys.argv[2] == "0" else True
  with open(path, "r") as input_file:
    content = input_file.read().replace('\n', '')

  brandings = ['Chromium', 'linux']
  output_duplicates = []
  sections = re.findall('\[([^\}]*)\]', content)
  for section in sections:
    condition = re.findall("'([^']*)'", section)
    if (arch_only_x86):
      if ('OS == "linux" and target_arch == "x64" and ffmpeg_branding == "Chromium"' or
          'OS == "linux" and target_arch == "ia32" and ffmpeg_branding == "Chromium"') in condition[0]:
        for source_file in condition[1:]:
          output_duplicates.append(source_file)
    elif ('OS == "linux"' and 'ffmpeg_branding == "Chromium"') in condition[0]:
      for source_file in condition[1:]:
        output_duplicates.append(source_file)

  output = list(set(output_duplicates))
  output.remove('c_sources')
  output.remove('asm_sources')
  print ' '.join(output)
