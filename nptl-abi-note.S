/* Gleaned from glibc, though I suppose it's documented in the specs, too.
   NPTL requires support that isn't in kernels prior to 2.4.20 (or 2.5.36 if
   you're not using a backported TLS implementation in your kernel), but ld.so
   will try to use this library on an insufficiently-new system unless we make
   a note of the required kernel version here.
   We also add in a section which marks the library as not needing an
   executable stack to avoid unintentionally disabling exec-shield and the
   like (thanks Arjan!). */
	.section ".note.ABI-tag", "a"
	.p2align 2
	.long 1f - 0f
	.long 3f - 2f
	.long  1
0:	.asciz "GNU"
1:	.p2align 2
2:	.long 0
	.long 2,4,20
3:	.p2align 2

.section .note.GNU-stack, "", @progbits
.previous
