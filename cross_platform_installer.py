import os
import sys
import platform


def is_termux():
    return 'com.termux' in os.environ.get('PREFIX', '')


def is_macos():
    return sys.platform == 'darwin'


def install():
    run = os.system

    if is_termux():
        prefix = os.environ.get('PREFIX')
        bin_path = os.path.join(prefix, 'bin', 'webextractor')
        share_path = os.path.join(prefix, 'share', 'webextractor')

        run('chmod 777 webextractor.py')
        run(f'mkdir -p {share_path}')
        run(f'cp webextractor.py {share_path}/webextractor.py')

        termux_launcher = f'#! /data/data/com.termux/files/usr/bin/sh\nexec python3 {share_path}/webextractor.py "$@"'
        with open(bin_path, 'w') as file:
            file.write(termux_launcher)

        run(f'chmod +x {bin_path} && chmod +x {share_path}/webextractor.py')
        print('\n[+] WebExtractor installed successfully in Termux')
        print('[+] Now just type \x1b[6;30;42mwebextractor\x1b[0m in terminal')

    elif is_macos():
        bin_path = '/usr/local/bin/webextractor'
        share_path = '/usr/local/share/webextractor'

        if os.geteuid() != 0:
            print("Please run as root or with sudo")
            sys.exit(1)

        run('chmod 777 webextractor.py')
        run(f'mkdir -p {share_path}')
        run(f'cp webextractor.py {share_path}/webextractor.py')

        mac_launcher = f'#! /bin/sh\nexec python3 {share_path}/webextractor.py "$@"'
        with open(bin_path, 'w') as file:
            file.write(mac_launcher)

        run(f'chmod +x {bin_path} && chmod +x {share_path}/webextractor.py')
        print('\n[+] WebExtractor installed successfully on macOS')
        print('[+] Now just type \x1b[6;30;42mwebextractor\x1b[0m in terminal')

    else:
        bin_path = '/usr/bin/webextractor'
        share_path = '/usr/share/webextractor'

        if os.geteuid() != 0:
            print("Please run as root or with sudo")
            sys.exit(1)

        run('chmod 777 webextractor.py')
        run(f'mkdir -p {share_path}')
        run(f'cp webextractor.py {share_path}/webextractor.py')

        linux_launcher = f'#! /bin/sh\nexec python3 {share_path}/webextractor.py "$@"'
        with open(bin_path, 'w') as file:
            file.write(linux_launcher)

        run(f'chmod +x {bin_path} && chmod +x {share_path}/webextractor.py')
        print('\n[+] WebExtractor installed successfully on Linux')
        print('[+] Now just type \x1b[6;30;42mwebextractor\x1b[0m in terminal')


def uninstall():
    run = os.system

    if is_termux():
        prefix = os.environ.get('PREFIX')
        run(f'rm -rf {prefix}/share/webextractor')
        run(f'rm -f {prefix}/bin/webextractor')
        print('[!] WebExtractor removed from Termux successfully')

    elif is_macos():
        if os.geteuid() != 0:
            print("Please run as root or with sudo")
            sys.exit(1)
        run('rm -rf /usr/local/share/webextractor')
        run('rm -f /usr/local/bin/webextractor')
        print('[!] WebExtractor removed from macOS successfully')

    else:
        if os.geteuid() != 0:
            print("Please run as root or with sudo")
            sys.exit(1)
        run('rm -rf /usr/share/webextractor')
        run('rm -f /usr/bin/webextractor')
        print('[!] WebExtractor removed from Linux successfully')


if __name__ == "__main__":
    choice = input('[+] To install press (Y) to uninstall press (N) >> ')
    if choice.lower() == 'y':
        install()
    elif choice.lower() == 'n':
        uninstall()
    else:
        print("[!] Invalid input. Exiting...")
