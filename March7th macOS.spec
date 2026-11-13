# -*- mode: python ; coding: utf-8 -*-
import os
import sys

from PyInstaller.utils.hooks import collect_data_files

sys.path.append(SPECPATH)
from tools.pyinstaller_openssl import OPENSSL_RUNTIME_HOOKS

block_cipher = None
common_hiddenimports = [
    'selenium.webdriver.chrome.webdriver',
    'selenium.webdriver.chrome.service',
    'selenium.webdriver.chrome.options',
    'selenium.webdriver.chromium.webdriver',
    'selenium.webdriver.chromium.service',
    'selenium.webdriver.chromium.options',
    'selenium.webdriver.remote.webdriver',
    'selenium.webdriver.common.service',
    'selenium.webdriver.common.selenium_manager',
]

def excluded(dest_name):
    dest = dest_name.replace('\\', '/').lower()
    base = dest.rsplit('/', 1)[-1]
    return (
        (dest.startswith('rapidocr/') and base.endswith('_infer.onnx'))
        or 'opencv_videoio_ffmpeg' in base
        or base.startswith('_avif.')
        or dest.startswith('selenium/webdriver/common/windows/')
        or dest.startswith('selenium/webdriver/common/linux/')
    )

launcher = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=collect_data_files('rapidocr'),
    hiddenimports=common_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=OPENSSL_RUNTIME_HOOKS,
    excludes=['openvino', 'openvino_telemetry'],
    noarchive=False,
    optimize=0,
)
launcher.binaries = [item for item in launcher.binaries if not excluded(item[0])]
launcher.datas = [item for item in launcher.datas if not excluded(item[0])]
launcher_pyz = PYZ(launcher.pure)
launcher_exe = EXE(
    launcher_pyz,
    launcher.scripts,
    [],
    exclude_binaries=True,
    name='March7th Launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='arm64',
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/logo/March7th.icns',
)
launcher_coll = COLLECT(
    launcher_exe,
    launcher.binaries,
    launcher.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='March7th Launcher',
)
app = BUNDLE(
    launcher_coll,
    name='March7th Assistant.app',
    icon='assets/logo/March7th.icns',
    bundle_identifier='top.m7a.March7thAssistant',
    info_plist={
        'CFBundleDisplayName': '三月七小助手',
        'CFBundleShortVersionString': '2026.11.8',
        'LSMinimumSystemVersion': '12.6',
        'NSHighResolutionCapable': True,
        'NSAppleEventsUsageDescription': '三月七小助手需要控制游戏和浏览器以执行自动化任务。',
        'NSScreenCaptureUsageDescription': '三月七小助手需要读取游戏画面以识别当前状态。',
        'NSAccessibilityUsageDescription': '三月七小助手需要模拟键鼠操作以执行游戏任务。',
    },
)

cli = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=collect_data_files('rapidocr'),
    hiddenimports=common_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=OPENSSL_RUNTIME_HOOKS,
    excludes=['PySide6', 'openvino', 'openvino_telemetry'],
    noarchive=False,
    optimize=0,
)
cli.binaries = [item for item in cli.binaries if not excluded(item[0])]
cli.datas = [item for item in cli.datas if not excluded(item[0])]
cli_pyz = PYZ(cli.pure)
cli_exe = EXE(
    cli_pyz,
    cli.scripts,
    [],
    exclude_binaries=True,
    name='March7th Assistant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='arm64',
    codesign_identity=None,
    entitlements_file=None,
    contents_directory='libraries',
)
cli_coll = COLLECT(
    cli_exe,
    cli.binaries,
    cli.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='March7th Assistant CLI',
)
