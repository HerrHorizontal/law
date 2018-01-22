# -*- coding: utf-8 -*-

"""
CMS-related tasks and helpers.
https://home.cern/about/experiments/cms
"""


__all__ = ["BundleCMSSW"]


import os

import luigi

from law.task.base import Task
from law.target.local import LocalFileTarget
from law.parameter import NO_STR
from law.decorator import log
from law.util import rel_path, interruptable_popen


class BundleCMSSW(Task):

    path = luigi.Parameter(description="the path to the CMSSW checkout to bundle")
    exclude = luigi.Parameter(default=NO_STR, description="regular expression for excluding files "
        "or directories, relative to the CMSSW checkout path")

    def __init__(self, *args, **kwargs):
        super(BundleCMSSW, self).__init__(*args, **kwargs)

        self.path = os.path.expandvars(os.path.expanduser(os.path.abspath(self.path)))

    def output(self):
        return LocalFileTarget("{}.tgz".format(os.path.basename(self.path)))

    @log
    def run(self):
        with self.output().localize("w") as tmp:
            cmd = [rel_path(__file__, "bundle_cmssw.sh"), self.path, tmp.path]
            if self.exclude != NO_STR:
                cmd += [self.exclude]

            code = interruptable_popen(cmd)[0]
            if code != 0:
                raise Exception("cmssw bundling failed")