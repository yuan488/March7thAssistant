from utils.command import subprocess_with_stdout
import subprocess
import sys
import os


def is_windows_terminal_available():
    """
    检查 Windows Terminal (wt.exe) 是否可用。
    """
    return subprocess_with_stdout(["where", "wt.exe"]) is not None


def execute_command_in_new_environment(command, use_windows_terminal=False):
    """
    在新的环境中执行给定的命令。
    """
    if getattr(sys, 'frozen', False):
        executable_name = "March7th Assistant.exe" if sys.platform == "win32" else "March7th Assistant"
        executable_path = os.path.abspath(os.path.join(os.path.dirname(sys.executable), executable_name))
        if not os.path.exists(executable_path):
            raise Exception(f"未找到可执行文件：{executable_name}\n请重新下载并完整解压应用包")
    else:
        executable_path = sys.executable
    main_script = [] if getattr(sys, 'frozen', False) else ["main.py"]

    if sys.platform != "win32":
        subprocess.Popen([executable_path] + main_script + [command])
    elif use_windows_terminal:
        # 尝试使用 Windows Terminal 执行命令
        try:
            subprocess.Popen(["wt", executable_path] + main_script + [command], creationflags=subprocess.DETACHED_PROCESS)
        except Exception:
            # 如果执行失败，则回退到创建新控制台的方式执行
            subprocess.Popen([executable_path] + main_script + [command], creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        # 直接在新的控制台中执行命令
        subprocess.Popen([executable_path] + main_script + [command], creationflags=subprocess.CREATE_NEW_CONSOLE)


def start_task(command):
    """
    通过信号总线启动任务，在日志界面中显示输出。
    """
    from app.common.signal_bus import signalBus
    signalBus.startTaskSignal.emit(command)


def start_task_in_new_window(command):
    """
    根据当前环境，在新窗口中启动任务（旧方式）。
    """
    # 检查 Windows Terminal 的可用性
    wt_available = is_windows_terminal_available()

    # 根据条件执行命令
    execute_command_in_new_environment(command, use_windows_terminal=wt_available)
