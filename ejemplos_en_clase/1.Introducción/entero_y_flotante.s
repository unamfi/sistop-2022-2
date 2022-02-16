	.file	"entero_y_flotante.c"
	.text
	.globl	main
	.type	main, @function
main:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	$1, -4(%rbp)
	movl	$2, -8(%rbp)
	movl	-4(%rbp), %edx
	movl	-8(%rbp), %eax
	addl	%edx, %eax
	movl	%eax, -12(%rbp)
	movss	.LC0(%rip), %xmm0
	movss	%xmm0, -16(%rbp)
	movss	.LC1(%rip), %xmm0
	movss	%xmm0, -20(%rbp)
	movss	-16(%rbp), %xmm0
	addss	-20(%rbp), %xmm0
	movss	%xmm0, -24(%rbp)
	nop
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.section	.rodata
	.align 4
.LC0:
	.long	1065353216
	.align 4
.LC1:
	.long	1073741824
	.ident	"GCC: (Debian 11.2.0-14) 11.2.0"
	.section	.note.GNU-stack,"",@progbits
