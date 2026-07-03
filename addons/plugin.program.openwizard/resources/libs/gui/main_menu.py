################################################################################
#      Copyright (C) 2019 drinfernoo                                           #
#                                                                              #
#  This Program is free software; you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation; either version 2, or (at your option)         #
#  any later version.                                                          #
#                                                                              #
#  This Program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with XBMC; see the file COPYING.  If not, write to                    #
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.       #
#  http://www.gnu.org/copyleft/gpl.html                                        #
################################################################################

import os

from resources.libs.common import directory
from resources.libs.common.config import CONFIG


class MainMenu:

    def get_listing(self):
        from resources.libs import check
        from resources.libs.common import logging
        from resources.libs.common import tools

        errors = int(logging.error_checking(count=True))
        errorsfound = str(errors) + ' Lỗi Được Tìm Thấy' if errors > 0 else 'Không Tìm Thấy'

        if CONFIG.AUTOUPDATE == 'Yes':
            response = tools.open_url(CONFIG.BUILDFILE, check=True)

            if response:
                ver = check.check_wizard('version')
                if ver:
                    if ver > CONFIG.ADDON_VERSION:
                        directory.add_file(
                            '{0} [v{1}] [COLOR red][B][CẬP NHẬT v{2}][/B][/COLOR]'.format(CONFIG.ADDONTITLE,
                                                                                        CONFIG.ADDON_VERSION, ver),
                            {'mode': 'wizardupdate'}, themeit=CONFIG.THEME2)
                    else:
                        directory.add_file('{0} [v{1}]'.format(CONFIG.ADDONTITLE, CONFIG.ADDON_VERSION),
                                           themeit=CONFIG.THEME2)
            else:
                directory.add_file('{0} [v{1}]'.format(CONFIG.ADDONTITLE, CONFIG.ADDON_VERSION),
                                   themeit=CONFIG.THEME2)
        else:
            directory.add_file('{0} [v{1}]'.format(CONFIG.ADDONTITLE, CONFIG.ADDON_VERSION), themeit=CONFIG.THEME2)
        if len(CONFIG.BUILDNAME) > 0:
            version = check.check_build(CONFIG.BUILDNAME, 'version')
            build = '{0} (v{1})'.format(CONFIG.BUILDNAME, CONFIG.BUILDVERSION)
            if version and CONFIG.BUILDVERSION and str(version) > str(CONFIG.BUILDVERSION):
                build = '{0} [COLOR red][B][CẬP NHẬT v{1}][/B][/COLOR]'.format(build, version)
            directory.add_dir(build, {'mode': 'viewbuild', 'name': CONFIG.BUILDNAME}, themeit=CONFIG.THEME4)

            from resources.libs.gui.build_menu import BuildMenu
            themefile = BuildMenu().theme_count(CONFIG.BUILDNAME)
            if themefile:
                directory.add_file('Không Có' if CONFIG.BUILDTHEME == "" else CONFIG.BUILDTHEME, {'mode': 'theme', 'name': CONFIG.BUILDNAME},
                                   themeit=CONFIG.THEME5)
        else:
            directory.add_dir('Không Có', {'mode': 'builds'}, themeit=CONFIG.THEME4)
        directory.add_separator()
        directory.add_dir('[COLOR red]Gói Cài Đặt[/COLOR]', {'mode': 'builds'}, description='Cài đặt và quản lý các gói build Kodi', icon=CONFIG.ICONBUILDS, themeit=CONFIG.THEME1)
        directory.add_dir('Bảo Trì', {'mode': 'maint'}, description='Các công cụ dọn dẹp, quản lý addon, sao lưu và khôi phục hệ thống', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
        if (tools.platform() == 'android' or CONFIG.DEVELOPER == 'true'):
            directory.add_dir('Cài Đặt APK', {'mode': 'apk'}, description='Cài đặt các ứng dụng Android trực tiếp', icon=CONFIG.ICONAPK, themeit=CONFIG.THEME1)
        if tools.open_url(CONFIG.ADDONFILE, check=True) or os.path.exists(os.path.join(CONFIG.ADDON_PATH, 'resources', 'text', 'addons.json')):
            directory.add_dir('Cài Đặt Addon', {'mode': 'addons'}, description='Duyệt và cài đặt các addon bổ sung cho Kodi', icon=CONFIG.ICONADDONS, themeit=CONFIG.THEME1)
        if tools.open_url(CONFIG.YOUTUBEFILE, check=True) and not CONFIG.YOUTUBETITLE == '':
            directory.add_dir(CONFIG.YOUTUBETITLE, {'mode': 'youtube'}, description='Xem các video hướng dẫn và giới thiệu', icon=CONFIG.ICONYOUTUBE, themeit=CONFIG.THEME1)
        directory.add_dir('Lưu Dữ Liệu', {'mode': 'savedata'}, description='Sao lưu và khôi phục các dữ liệu quan trọng của hệ thống', icon=CONFIG.ICONSAVE, themeit=CONFIG.THEME1)
        if CONFIG.HIDECONTACT == 'No':
            directory.add_file('Liên Hệ', {'mode': 'contact'}, description='Liên hệ với nhà phát triển addon', icon=CONFIG.ICONCONTACT, themeit=CONFIG.THEME1)
        directory.add_separator()
        directory.add_file('Tải Lên File Log', {'mode': 'uploadlog'}, description='Tải lên file log để giúp sửa lỗi và hỗ trợ', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
        directory.add_file('Xem Lỗi Trong Log: {0}'.format(errorsfound), {'mode': 'viewerrorlog'}, description='Kiểm tra các lỗi được ghi nhận trong file log', icon=CONFIG.ICONMAINT,
                           themeit=CONFIG.THEME1)
        if errors > 0:
            directory.add_file('Xem Lỗi Cuối Cùng Trong Log', {'mode': 'viewerrorlast'}, description='Xem lỗi mới nhất được ghi nhận trong file log', icon=CONFIG.ICONMAINT, themeit=CONFIG.THEME1)
        directory.add_separator()
        directory.add_file('Cài Đặt', {'mode': 'settings', 'name': CONFIG.ADDON_ID}, description='Thay đổi các tùy chỉnh và cài đặt của addon', icon=CONFIG.ICONSETTINGS, themeit=CONFIG.THEME1)
        if CONFIG.DEVELOPER == 'true':
            directory.add_dir('Menu Nhà Phát Triển', {'mode': 'developer'}, description='Các công cụ và tính năng dành cho nhà phát triển', icon=CONFIG.ADDON_ICON, themeit=CONFIG.THEME1)
