# SSLPin

SSLPin is a collection of tools for implementing ssl pinning by means of self
authenticating URLs.

This means that the address itself includes the SSL fingerprint of the expected
certificate, making it possible to verify the validity of a certificate
independently from certificate authorities.

In other words the URL becomes "self authenticating".

## Scheme

We introduce a new scheme called **httpsv** or HTTPS Verified. The syntax for
it is as follows:

```
httpsv:// < certificate depth > = < base32 encoded sha1 fingerprint of the certificate >; < hostname > / 
```

Where *certificate depth* is an integer telling us at which point in the
certificate chain the pin is referring to. 0 means the peer certificate,
1 means the CA certificate, 2 higher level CA certificate and so on [1]

[1] https://www.openssl.org/docs/ssl/SSL_CTX_set_verify.html
