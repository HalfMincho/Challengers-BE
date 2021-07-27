import re
import ipaddress

ipv4_prefix = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFF\xFF'


def ipv6ify(addr: str) -> bytes:
    ipv4_pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}$')
    ipv6_pattern = re.compile(r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))')

    if re.fullmatch(ipv4_pattern, addr):
        return ipv4_prefix + ipaddress.IPv4Address(addr).packed
    elif re.fullmatch(ipv6_pattern, addr):
        return ipaddress.IPv6Address(addr).packed
    else:
        raise ValueError('address not valid ipv4 or ipv6 address!')


def ipv4ify(addr: bytes) -> str:
    if addr.startswith(ipv4_prefix):
        return str(ipaddress.IPv4Address(addr[len(ipv4_prefix):]))
    else:
        return str(ipaddress.IPv6Address(addr))


__all__ = ['ipv4ify', 'ipv6ify']
