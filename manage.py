#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
#!/usr/bin/env python
#!/usr/bin/env python
#!/usr/bin/env python
import os
import sys
import ssl

# Monkey-patch для Python 3.13, если ssl.wrap_socket отсутствует
if not hasattr(ssl, "wrap_socket"):
    def wrap_socket(sock, certfile=None, keyfile=None, server_side=False, **kwargs):
        # Удаляем аргументы, которые не поддерживаются методом wrap_socket() у SSLContext
        kwargs.pop('ssl_version', None)
        kwargs.pop('cert_reqs', None)
        # Можно также удалить другие параметры, если потребуется.
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        if certfile:
            context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        return context.wrap_socket(sock, server_side=server_side, **kwargs)
    ssl.wrap_socket = wrap_socket

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TaskFlow.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? "
            "Did you forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()


