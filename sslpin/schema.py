import base64

def fingerprint_to_base32(fingerprint):
    digest = ''.join(chr(int(x, 16)) for x in fingerprint.split(':'))
    return base64.b32encode(digest)

def base32_to_fingerprint(base32):
    data = base64.b32decode(base32)
    return ':'.join("%02X" % ord(x) for x in data)
