import os


def get_environment() -> dict:
    env = os.environ.copy()
    env['WAYLAND_DISPLAY'] = 'wayland-0'
    env['XDG_RUNTIME_DIR'] = '/run/user/1000' # 1000 should be the user id. Beware
    return env
