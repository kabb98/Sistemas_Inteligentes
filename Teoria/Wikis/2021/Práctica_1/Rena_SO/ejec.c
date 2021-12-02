//Rana Abadi
#include <sys/wait.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <signal.h>

void alarma();

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./ejec [segundos]\nTienes que pasar 2 argumentos!!!\n");
    }
    else
    {
        //Almacenamos aqui los proc hijos
        int childrenProc[4];
        int seg = atoi(argv[1]);
        int e;

        //Se declara aqui para luego usarlo para matar los distintos procesos
        int i;
        int padre;

        //Proceso abuelo
        int pid = getpid();
        printf("Soy el proceso ejec: Mi pid es: %d\n", getpid());
        int pid1 = fork();
        int abuelo = getpid();
        if (pid1 == 0)
        {
            printf("Soy el proceso A: Mi pid es: %d. Mi padre es: %d\n", getpid(), getppid());
            int pid2 = fork();
            padre = getpid();
            if (pid2 == 0)
            {
                printf("Soy el proceso B: Mi pid es: %d. Mi padre es: %d, mi abuelo es: %d\n", getpid(), getppid(), pid);
                for (i = 0; i < 3; i++)
                {
                    int pidHijos = fork();
                    if (pidHijos == 0)
                    {
                        switch (i)
                        {
                        case 0:
                            printf("Soy el proceso X: Mi pid es: %d. Mi padre es %d, abuelo %d, mi bisabuelo es: %d\n", getpid(), getppid(), abuelo, pid);
                            wait(NULL);
                            break;

                        case 1:
                            printf("Soy el proceso Y: Mi pid es: %d. Mi padre es %d, abuelo %d, mi bisabuelo es: %d\n", getpid(), getppid(), abuelo, pid);
                            wait(NULL);
                            break;

                        case 2:
                            printf("Soy el proceso Z: Mi pid es: %d. Mi padre es %d, abuelo %d, mi bisabuelo es: %d\n", getpid(), getppid(), abuelo, pid);
                            signal(SIGALRM, alarma);
                            alarm(seg);
                            pause();
                            execlp("pstree", "pptree", "-la", NULL);
                        }
                        break;
                    }
                    else
                    {
                        childrenProc[i] = wait(&e);
                        if (i == 2)
                        {
                            printf("Soy Z (%d) y muero\n", childrenProc[2]);
                            kill(childrenProc[1], SIGKILL);
                            printf("Soy Y (%d) y muero\n", childrenProc[1]);
                            kill(childrenProc[0], SIGKILL);
                            printf("Soy X (%d) y muero\n", childrenProc[0]);
                        }
                    }
                }
            }
            else
            {
                wait(&e);
                kill((pid_t)padre, SIGKILL);
            }
        }
        else
        {
            wait(&e);
        }

        if (i == 3)
        {
            printf("Soy B(%d) y muero\n", padre);
            printf("Soy A(%d) y muero\n", abuelo);
            kill((pid_t)abuelo, SIGKILL);
            printf("Soy ejec(%d) y muero\n", pid);
            exit(0);
        }
    }
}

void alarma()
{
    signal(SIGALRM, SIG_IGN);
    printf("Alarm!!!!\n");
}
