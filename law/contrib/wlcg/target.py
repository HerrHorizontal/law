# coding: utf-8

"""
WLCG remote file system and targets.
"""


__all__ = ["WLCGFileSystem", "WLCGTarget", "WLCGFileTarget", "WLCGDirectoryTarget"]


import stat
import logging

import six

from law.config import Config
from law.target.remote import (
    RemoteFileSystem, RemoteTarget, RemoteFileTarget, RemoteDirectoryTarget,
)


logger = logging.getLogger(__name__)


class WLCGFileSystem(RemoteFileSystem):

    default_instance = None

    def __init__(self, section=None, **kwargs):
        # default gfal transfer config
        kwargs.setdefault("transfer_config", {})
        kwargs["transfer_config"].setdefault("checksum_check", False)

        # if present, read options from the section in the law config
        cfg = Config.instance()
        if not section:
            section = cfg.get_expanded("target", "default_wlcg_fs")
        if isinstance(section, six.string_types):
            if cfg.has_section(section):
                kwargs = self.parse_config(section, kwargs)
            else:
                raise Exception("law config has no section '{}' to read {} options".format(
                    section, self.__class__.__name__))

        # base path is mandatory
        if not kwargs.get("base"):
            raise Exception("{}.base is missing, set either 'section', 'base', or change the "
                "target.default_wlcg_fs option in your law config".format(self.__class__.__name__))

        base = kwargs.pop("base")
        RemoteFileSystem.__init__(self, base, **kwargs)

    def _s_isdir(self, st_mode):
        # some WLCG file protocols do not return standard st_mode values in stat requests,
        # e.g. srm returns file type bits 0o50000 for directories instead of 0o40000,
        # these differences are rather distinct and can be taken into account here,
        # see http://man7.org/linux/man-pages/man7/inode.7.html for info on st_mode values
        return stat.S_ISDIR(st_mode) or stat.S_IFMT(st_mode) == 0o50000


# try to set the default fs instance
try:
    WLCGFileSystem.default_instance = WLCGFileSystem()
    logger.debug("created default WLCGFileSystem instance '{}'".format(
        WLCGFileSystem.default_instance))
except Exception as e:
    logger.debug("could not create default WLCGFileSystem instance: {}".format(e))


class WLCGTarget(RemoteTarget):

    def __init__(self, path, fs=WLCGFileSystem.default_instance, **kwargs):
        """ __init__(path, fs=WLCGFileSystem.default_instance, **kwargs)
        """
        if isinstance(fs, six.string_types):
            fs = WLCGFileSystem(fs)
        RemoteTarget.__init__(self, path, fs, **kwargs)


class WLCGFileTarget(WLCGTarget, RemoteFileTarget):

    pass


class WLCGDirectoryTarget(WLCGTarget, RemoteDirectoryTarget):

    pass


WLCGTarget.file_class = WLCGFileTarget
WLCGTarget.directory_class = WLCGDirectoryTarget
