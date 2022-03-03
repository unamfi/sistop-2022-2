#include<stdio.h>
#include<unistd.h>
main(void){
	int pid, estado;
	pid = fork();
	if(pid==0){
		sleep(1);
		printf("[Hijo] Pid del padre = %5d Mi pid = %5d\n", getppid(), getpid());
	}
	else{
		printf("[Padre] Mi padre = %5d Mi pid = %5d Pid de mi hijo = %5d\n", getppid(),getpid(),pid);
		pid = wait(&estado);
		printf("[Padre] Termino el hijo %d con estado %d\n", pid, estado);
	}
}
