# preparecleanup.py
#
# Copyright (C) 2018 Red Hat Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Jakub Mazanek <jmazanek@redhat.com>

import json
import os
import shutil
import subprocess
import platform
from redhat_upgrade_tool.util import mkdir_p
from redhat_upgrade_tool.rollback.bootloader import _SNAP_BOOT_FILES


def create_cleanup_script():
    rollback_dst = '/boot/rollback'
    if not os.path.isdir('/boot/manualcleanup'):
        mkdir_p('/boot/manualcleanup')

    rollback_path = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(rollback_dst):
        shutil.rmtree(rollback_dst)
    shutil.copytree(rollback_path, rollback_dst)

    with open(os.path.join(rollback_dst, '.active-kernel'), 'w') as active_kernel:
        active_kernel.write(platform.release())

    with open(os.path.join(rollback_dst, '.all-kernels'), 'w') as all_kernels:
        all_kernels.write(subprocess.Popen(["rpm", "-qa", "kernel"], stdout=subprocess.PIPE).communicate()[0])

    dump_snapshot_boot_files()


def dump_snapshot_boot_files():
    _SNAP_BOOT_PATHS = []
    for fmt in _SNAP_BOOT_FILES:
        path = os.path.join("/boot", fmt.format("snapshot"))
        _SNAP_BOOT_PATHS.append(path)
        dump_vars(_SNAP_BOOT_PATHS, '/boot/manualcleanup/snap_boot_files')


def dump_vars(variables, out_file):
    with open(out_file, 'w+') as outfile:
        json.dump(variables, outfile)
