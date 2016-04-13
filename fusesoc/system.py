from fusesoc import section
from fusesoc.fusesocconfigparser import FusesocConfigParser
from fusesoc.config import Config
import os
import logging
from fusesoc.utils import splitNameString, sanitizeName

logger = logging.getLogger(__name__)

class System:
    def __init__(self, system_file):
        self.backend_name = None

        self.system_root = os.path.dirname(system_file)
        self.config = FusesocConfigParser(system_file)

        self.vendor = ""
        self.library = ""
        self.systemname = ""
        self.version = ""
        self.name = ""

        self.pre_build_scripts  = self.config.get_list('scripts','pre_build_scripts')
        self.post_build_scripts = self.config.get_list('scripts','post_build_scripts')

        if self.config.has_option('main', 'backend'):
            self.backend_name = self.config.get('main','backend')
            self.backend = section.load_section(self.config, self.backend_name,
                                                file_name=system_file)

        self.main = section.load_section(self.config, "main", file_name=system_file)

        # Extract all parts of the name for the different ways to provide it
        if self.main.name:
            (self.vendor, self.library, self.systemname, self.version) = splitNameString(self.main.name)
        else:
            self.systemname = os.path.basename(system_file).split('.')[0]

        if self.main.vendor:
            if self.vendor:
                utils.pr_warn("vendor was already specified as part of the name, ignoring")
            else:
                self.vendor = self.main.vendor

        if self.main.library:
            if self.library:
                utils.pr_warn("library was already specified as part of the name, ignoring")
            else:
                self.library = self.main.library

        if self.main.version:
            if self.version:
                utils.pr_warn("version was already specified as part of the name, ignoring")
            else:
                self.version = self.main.version

        # Assemble the full name
        if self.vendor:
            self.name += self.vendor + ":"
        if self.library:
            self.name += self.library + ":"
        self.name += self.systemname
        if self.version:
            self.name += "@" + self.version

        self.sanitized_name = sanitizeName(self.name)

    def info(self):
        print("\nSYSTEM INFO")
        print(self.backend)
