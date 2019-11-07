# -*- coding: utf-8 -*-
#
#  2019-11-07 Cornelius Kölbel <cornelius.koelbel@netknights.it>
#             initial code for writing audit information to a file
#
# This code is free software; you can redistribute it and/or
# modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
# License as published by the Free Software Foundation; either
# version 3 of the License, or any later version.
#
# This code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU AFFERO GENERAL PUBLIC LICENSE for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
__doc__ = """The Container Audit Module is used to write audit entries to the Python logging module.

The Logger Audit Module is configured like this:

    PI_AUDIT_MODULE = 'privacyidea.lib.auditmodules.containeraudit'
    PI_AUDIT_CONTAINER_WRITE = ['privacyidea.lib.auditmodules.sqlaudit','privacyidea.lib.auditmodules.loggeraudit']
    PI_AUDIT_CONTAINER_READ = 'privacyidea.lib.auditmodules.sqlaudit'

You also have to provide the configuration parameters for the referenced audit modules.

"""

import logging
from privacyidea.lib.auditmodules.base import (Audit as AuditBase)
from privacyidea.lib.utils import get_module_class


log = logging.getLogger(__name__)


class Audit(AuditBase):
    """
    This is the ContainerAudit module, which writes the audit entries
    to a list of audit modules.
    """

    def __init__(self, config=None):
        self.name = "containeraudit"
        self.audit_data = {}
        self.config = config or {}
        write_conf = self.config.get('PI_AUDIT_CONTAINER_WRITE')
        read_conf = self.config.get('PI_AUDIT_CONTAINER_READ')
        # Initialize all modules
        self.write_modules = [get_module_class(audit_module, "Audit", "log")(config) for audit_module in write_conf]
        self.read_module = get_module_class(read_conf, "Audit", "log")(config)

    def log(self, param):
        """
        Call the log method for all writeable modules
        """
        for module in self.write_modules:
            module.log(param)

    def search(self, param, display_error=True, rp_dict=None, timelimit=None):
        """
        Call the search method for the one readable module
        """
        return self.read_module.search(param, display_error=display_error,
                                       rp_dict=rp_dict, timelimit=timelimit)

    def get_count(self, search_dict, timedelta=None, success=None):
        """
        Call the count method for the one readable module
        """
        return self.read_module.get_count(search_dict, timedelta=timedelta, success=success)

    def get_total(self, param, AND=True, display_error=True):
        """
        Call the total method for the one readable module
        """
        return self.read_module.get_total(param, AND=AND, display_error=display_error)

    def finalize_log(self):
        """
        Call the finalize method of all writeable audit modules
        """
        for module in self.write_modules:
            module.finalize()

