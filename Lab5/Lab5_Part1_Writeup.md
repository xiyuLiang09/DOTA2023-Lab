# Lab5 Part1 Writeup

> Written by: LIANG XIYU

1. **What is the purpose of the extra information in the (CA) certificate you created?**

In addition to the public key and signature, the certificate also contains the following extra information:

- Version number (Version 3)
- Serial number
- Issuer
- Validity
- Subject identity information
- X509v3 extensions (X509v3 Extensions): such as key usage, key identifier, subject alternative name etc.

The purpose of this extra information is to provide the certificate verifier more detailed information about the certificate. For example, the issuer information can be used to trace back to the issuer's CA for verification , and then, a trusted CA chain establish, the validity indicates the validity period range of the certificate, and the X509v3 also specifies the key usage etc. The verifier can use this extra information to determine whether the certificate is trustworthy and ascertain the intended usage of the certificate.

------

2. **Explain the files you created. What is each file used for?**

```bash
openssl genrsa -out testCA.key 2048
openssl req -x509 -new -nodes -key testCA.key -sha256 -days 365 -out testCA.crt -config localhost.cnf -extensions v3_ca -subj "/CN=DOTA Test CA"
```

* `testCA.key`is a 2048-bit RSA private key file used for the CA to sign a self-signed root certificate to prove the authenticity and reliability of the certificate.

<img src="https://github.com/kkzka-hoh/DOTA2023-Lab/blob/main/Lab5/testCAkey.png" style="zoom: 67%;" />

* `testCA.crt`is a self-signed X.509 certificate file. Generally, a certificate consists of public key information and additional information such as the entity it belongs to, and the encryption/decryption algorithm used, which is used to verify the authenticity of the server's identity. Root certificates are typically pre-installed in operating systems or browsers and are used to verify the authenticity of other certificates. A detailed explanation of the specific information in this file can be found in the answer to the first question in Part 1.

<img src="https://github.com/kkzka-hoh/DOTA2023-Lab/blob/main/Lab5/testCAcrt.png" style="zoom: 50%;" />

* `localhost.cnf`：is an OpenSSL configuration file used to specify the properties and extensions of the root certificate. Here, this file specifies the DN (Distinguished Name) information of the certificate holder, including the country, province, city, organization, and common name, as well as the certificate key, digest algorithm, and certificate extensions properties.

<img src="https://github.com/kkzka-hoh/DOTA2023-Lab/blob/main/Lab5/localhostcnf.png" style="zoom:50%;" />

```bash
openssl genrsa -out localhost.key 2048
openssl req -new -key localhost.key -out localhost.csr -config localhost.cnf -extensions v3_req
openssl x509 -req -in localhost.csr -CA testCA.crt -CAkey testCA.key -CAcreateserial \
-out localhost.crt -days 365 -sha256 -extfile localhost.cnf -extensions v3_req
```

* `localhost.key`is the private key file of the server certificate, 2048 bits, used for the certificate request and certificate generation in the subsequent steps.
* `localhost.csr`is the server certificate request file, which contains the certificate signing request for the web server's public key.
* `localhost.crt`is the generated server certificate used to verify the authenticity of the server. It contains the web server's public key, as well as certificate version number, serial number, signature algorithm, issuer information, validity period, and extension information.

------

3. **Why is the webserver using both the certificate and private key? (What does it use each for?)**

**Certificate:** A certificate is used to verify the authenticity of a server's identity, and includes a public key. The web server uses the certificate to send the public key to the client, which generates a sufficiently long string as a session key, encrypts it with the server's public key, and sends it back to the server. The server then uses its private key to decrypt the encrypted session key, ensuring that only the server has access to the private key and can decrypt the data sent by the client. In simple terms, the client uses the certificate to verify the authenticity of the website being accessed. For example, if you want to deposit money into your Alipay account, which has a website address of [alipay](http://www.alipay.com/), the certificate can ensure that you are accessing the real website and not a malicious server.

**Private Key:** The private key is used to encrypt data sent from the server to the client, ensuring data confidentiality. The web server uses the private key to encrypt data before sending it to the client, which then uses the server's public key to decrypt the data. This ensures that the client receives data only from the server and that the data has not been tampered with during transmission.

Suppose an attacker intercepts the server's certificate issuance process and has the public key, but, based on the principle of asymmetric encryption, such as RSA, cannot calculate the private key and therefore cannot decrypt the message. If the attacker hijacks the server's certificate issuance process and replaces the server's public key with its own, but the certificate is signed by a CA, the client will know that the certificate has been tampered with once it verifies the signature.

Therefore, the web server needs to use both a CA and a private key to ensure communication security.

------

