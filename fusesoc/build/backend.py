import logging
import os.path
import shutil

from fusesoc.edatool import EdaTool
from fusesoc.utils import Launcher, pr_info, pr_warn


logger = logging.getLogger(__name__)

class Backend(EdaTool):

    def __init__(self, system):
        super(Backend, self).__init__(system)

        self.system_root = system.system_root
        self.env['SYSTEM_ROOT'] = os.path.abspath(self.system_root)
        self.env['BACKEND'] = self.TOOL_NAME

    def _get_fileset_files(self, usage):
        incdirs = set()
        src_files = []
        for core_name in self.cores:
            core = self.cm.get_core(core_name)
            basepath = os.path.relpath(os.path.join(self.src_root, core.sanitized_name), self.work_root)
            for fs in core.file_sets:
                if (set(fs.usage) & set(usage)) and ((core_name == self.system.name) or not fs.private):
                    for file in fs.file:
                        if file.is_include_file:
                            incdirs.add(os.path.join(basepath, os.path.dirname(file.name)))
                        else:
                            file.name = os.path.join(basepath, file.name)
                            src_files.append(file)
        return (src_files, incdirs)

    def configure(self, args):
        self.parse_args(args, 'build', ['vlogparam'])
        super(Backend, self).configure(args)
        self._export_backend_files()

    def _export_backend_files(self):
        src_dir = self.system.system_root
        dst_dir = os.path.join(self.src_root, self.system.sanitized_name)

        export_files = self.system.backend.export()
        dirs = list(set(map(os.path.dirname, export_files)))

        for d in dirs:
            if not os.path.exists(os.path.join(dst_dir, d)):
                os.makedirs(os.path.join(dst_dir, d))

        for f in export_files:
            if(os.path.exists(os.path.join(src_dir, f))):
                shutil.copyfile(os.path.join(src_dir, f),
                                os.path.join(dst_dir, f))
            else:
                pr_warn("File " + os.path.join(src_dir, f) + " doesn't exist")

    def build(self, args):
        for script in self.system.pre_build_scripts:
            script = os.path.abspath(os.path.join(self.system_root, script))
            pr_info("Running " + script);
            try:
                Launcher(script, cwd = os.path.abspath(self.build_root), env = self.env, shell=True).run()
            except RuntimeError:
                print("Error: script " + script + " failed")

    def done(self):
        for script in self.system.post_build_scripts:
            script = os.path.abspath(os.path.join(self.system_root, script))
            pr_info("Running " + script);
            try:
                Launcher(script, cwd = os.path.abspath(self.build_root), env = self.env, shell=True).run()
            except RuntimeError:
                print("Error: script " + script + " failed")
