# Writeup1: Encryption Mode – ECB vs. CBC

> English version



## 1. Encrypt an image using CBC (Cipher Block Chaining) mode.

When I wanted to encrypt the specified .bmp file in part3 of `Lab2.pdf`, I followed these steps to perform the encryption operation:

* **step1: Obtain .bmp files**

`wget https://www.comp.nus.edu.sg/~hugh/DOTA2023/Labs/Lab2/pic_original.bmp`

* **step2: Encrypt the image using the `aes-128-cbc` cipher type.**

`openssl enc -e -in pic_original.bmp -out cbc_enc.bmp -K 00112233445566778889aabbccddeeff -iv 0102030405060708`

* **step3: Use the `ghex` hexadecimal editor to replace the binary file header of the encrypted image with the header of the original image.**

`ghex pic_original.bmp         //Open the binary file of the original image.`

And record the header information of the original file.

`ghex cbc_enc.bmp             //Open the binary file of the encrypted image.`

Modify the first 56 bytes of the header information of the encrypted image according to the header of the original file.

After modifying and saving, we can now use the image viewer software that comes with Ubuntu to view the encrypted image. The image on the left in the following figure is the original image, and the image on the right is the encrypted image.

![image-20230715172912232]([D:\Desktop\kk\2023NUS暑期研习项目\DOTAfile\Lab_image\cbc_enc.png](https://github.com/kkzka-hoh/Lab-img/blob/main/cbc_enc.png))

As you can see, we cannot see any information about the original image from the encrypted image. In other words, without knowing the encryption key and initialization vector, an attacker cannot recover the image or obtain any information about the original image from the encrypted image.



## 2. Encrypt the image using ECB (Electronic CodeBook) mode.

The steps for encrypting the image using ECB mode are similar to those for CBC, except that the encryption command is changed to:

`openssl enc -e -aes-128-ecb -in pic_original.bmp -out ecb_enc.bmp -K 00112233445566778889aabbccddeeff`

Then, following the header modification process used in the CBC encryption, modify and save the image in the same way. The result can be seen in the image viewer as follows:

![ecb_enc](D:\Desktop\kk\2023NUS暑期研习项目\DOTAfile\Lab_image\ecb_enc.png)

It is evident that we can infer most of the information contained in the original image from the encrypted image, such as the objects and shapes depicted in the image.



## 3. Conclusion

Under ECB mode, the same block of colors will be encrypted into the same ciphertext, so even if we cannot accurately determine all the color information of the original object, we can still infer its shape.

In contrast, CBC mode has greater encryption strength with the same cipher type.
