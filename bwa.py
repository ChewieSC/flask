#!/usr/bin/env python

import os
import shlex
import subprocess

from distutils.spawn import find_executable

# XXX Think about moving handling of tempfiles in here
class BWA(object):

  def __init__(self, executable=''):
    self.executable = self._get_executable(executable)
    self.version, self.release = self._get_version()

  @staticmethod
  def _get_executable(bwa_executable):

    def is_exe(fpath):
      return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    if not bwa_executable or not is_exe(bwa_executable):
      bwa_executable = find_executable(os.path.expanduser(bwa_executable))
    return bwa_executable

  def _get_version(self):

    if not self.executable:
      return ('', 0)

    bwa = subprocess.Popen(self.executable, stderr=subprocess.PIPE)
    stdout, stderr = bwa.communicate()

    for line in stderr.splitlines():
      if line.startswith("Version"):
        version, release = line.split()[1].split('-r')
        return str(version), int(release)

    return ('', 0)

  def run(self, command):
    bwa_process = subprocess.Popen(shlex.split(command))
    return bwa_process.wait()


if __name__ == '__main__':
  bwa = BWA()
