# Writeup2: Encryption Mode – Corrupted Cipher Text

> English version



## Exercise steps

1. Create a text file `plaintext.txt` that is 64 bytes long: 

````text
Q4DvO5T4SNKvziIv VQtnXuG7rmspuzeu x9Njydp7DJlkryBp 5GHjDWuATdzxDXrb
````

2. Encrypt the file `plaintext.txt` using ECB, CBC, CFB, and OFB encryption mode and get 4 encrypted files, respectively.

   Below are the commands I used for encryption:

```text
# ECB mode
openssl enc -e -aes-128-ecb -in plaintext.txt -out ecb_enc.txt -K 00112233445566778889aabbccddeeff

# CBC mode
openssl enc -e -aes-128-cbc -in plaintext.txt -out cbc_enc.txt -K 00112233445566778889aabbccddeeff -iv 0102030405060708

# CFB mode
openssl enc -e -aes-128-cfb -in plaintext.txt -out cfb_enc.txt -K 00112233445566778889aabbccddeeff -iv 0102030405060708

# OFB mode
openssl enc -e -aes-128-ofb -in plaintext.txt -out ofb_enc.txt -K 00112233445566778889aabbccddeeff -iv 0102030405060708
```

3. Use `ghex` to corrupt a single bit of the 30th bytes in the 4 encrypted files, respectively.

4. Decrypt 4 corrupted files (encrypted) using correct key and IV.

   Below are the commands I used for decryption:

```text
# ECB mode
openssl enc -d -aes-128-ecb -in ecb_enc.txt -out ecb_dec.txt -K 00112233445566778889aabbccddeeff

# CBC mode
openssl enc -d -aes-128-cbc -in cbc_enc.txt -out cbc_dec.txt -K 00112233445566778889aabbccddeeff -iv 0102030405060708

# CFB mode
openssl enc -d -aes-128-cfb -in cfb_enc.txt -out cfb_dec.txt -K 00112233445566778889aabbccddeeff -iv 0102030405060708

# OFB mode
openssl enc -d -aes-128-ofb -in ofb_enc.txt -out ofb_dec.txt -K 00112233445566778889aabbccddeeff -iv 0102030405060708
```





## Answers to questions

1. Contents of original file and decrypted files.

* ECB mode

  48 bytes recovered

  ``` text
  # plaintext:
  Q4DvO5T4SNKvziIv VQtnXuG7rmspuzeu x9Njydp7DJlkryBp 5GHjDWuATdzxDXrb
  
  # recovered information:
  Q4DvO5T4SNKvziIv ïœm'6E¯4J	® x9Njydp7DJlkryBp 5GHjDWuATdzxDXrb
  ```

* CBC mode

  47 bytes recovered

  ```text
  # plaintext:
  Q4DvO5T4SNKvziIv VQtnXuG7rmspuzeu x9Njydp7DJlkryBp 5GHjDWuATdzxDXrb
  
  # recovered information:
  Q4DvO5T4SNKvziIv 0áCq¬fŒ{Cb	ä x9Njydp7DJlkriBp 5GHjDWuATdzxDXrb
  ```

* CFB mode

  47 bytes recovered

  ```text
  # plaintext:
  Q4DvO5T4SNKvziIv VQtnXuG7rmspuzeu x9Njydp7DJlkryBp 5GHjDWuATdzxDXrb
  
  # recovered information:
  Q4DvO5T4SNKvziIv VQtnXuG7rmspu{eu 1càGŒ AÚØÂ 5GHjDWuATdzxDXrb
  ```

* OFB mode

  63 bytes recovered

  ```text
  # plaintext:
  Q4DvO5T4SNKvziIv VQtnXuG7rmspuzeu x9Njydp7DJlkryBp 5GHjDWuATdzxDXrb
  
  # recovered information:
  Q4DvO5T4SNKvziIv VQtnXuG7rmspu{eu x9Njydp7DJlkryBp 5GHjDWuATdzxDXrb
  ```



2. Causes

* ECB mode

  In ECB mode, each ciphertext block is independently decrypted using the key without any relationship to other blocks to obtain the corresponding plaintext block, so only bytes in the block that corrupted byte belongs to will be affected, i.e. 16 bytes cannot be recovered. Therefore, there are 48 bytes are recovered when the encryption mode is ECB.

* CBC mode

  In CBC mode, each ciphertext block is first decrypted using the key, then XORed with the previous ciphertext block to obtain the corresponding plaintext block, so all bytes in the block following the block that corrupted byte belongs to and the corrupted byte itself will be affected, i.e. 16+1=17 bytes cannot be recovered. Therefore, there are 47 bytes are recovered when the encryption mode is CBC.

* CFB mode

  In CFB mode, each ciphertext block is XORed with the previous encrypted block, and then decrypted using the key to obtain the corresponding plaintext block, all bytes in the block that corrupted byte belongs to and the the byte at the corresponding position in the next block that corrupted bytes belongs to will be affected, i.e. 16+1=17 bytes cannot be recovered. Therefore, there are 47 bytes are recovered when the encryption mode is CFB.

* OFB mode

  In OFB mode, each ciphertext block is XORed with the random key stream generated from the IV and key to obtain the corresponding plaintext block, so only the corrupted byte will be affected, i.e. 1 byte cannot be recovered. Therefore, there are 63 bytes are recovered when the encryption mode is OFB.



3. Implication of these differences

   These differences have implication in terms of security, efficiency and corruption recovery.

   ECB mode is the simplest encryption mode. This mode is fastest but has the worst security. CBC and CFB mode have better security but lower efficiency and the least number of bytes recovered from corruption. OFB mode can recover the most number of bytes recovered from corruption, but it cannot provide authentication.

   Overall, encryption mode should be chosen based on the specific application and security requirements.
