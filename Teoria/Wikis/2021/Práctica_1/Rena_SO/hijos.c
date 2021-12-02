//Rana Abadi
#include <sys/shm.h>
#include <sys/ipc.h>
#include <sys/wait.h>
#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    //Si los arguementos no son 3, mostramos error
    if (argc != 3)
    {
        printf("Usage: ./hijos [x] [y]\nTienes que pasar 3 argumentos!!!\n");
        return 1;
    }
    {
        int x = atoi(argv[1]);
        int y = atoi(argv[2]);

        int childrenProc[x + 1];

        int abuelo;
        int e;
        if (fork() == 0)
            abuelo = getppid();
        else
        {
            wait(&e);
            exit(0);
        }
        //Iteramos sobre la altura
        for (int j = 1; j < x; j++)
        {
            if (fork() == 0)
            {
                if (j != 1)
                {
                    childrenProc[j] = getpid();
                }
                else
                {
                    childrenProc[1] = getpid();
                    childrenProc[2] = getppid();
                }
            }
            else
            {
                wait(&e);
                exit(0);
            }
        }

        //Iteramos sobre la "anchura"
        for (int i = 0; i < y; i++)
        {
            if (fork() == 0)
            {
                //Caso superpadre
                if (i == 0)
                {
                    printf("Soy el superpadre(%d): mis hijos finales son: ", abuelo);
                }
                else
                {
                    int procHijo = getpid();

                    printf("%d ", procHijo);

                    if (i == y - 1)
                    {
                        int subProc = procHijo - y + 1;
                        printf(".\nSoy el subhijo %d, mis padres son: ", subProc);
                    }
                    exit(0);
                }
            }
            else
            {
                wait(&e);
            }
        }

        //Children Proc Print
        for (int h = 0; h < x; h++)
        {
            printf(" %d", childrenProc[1]);
        }
        printf(".\n");
    }
}
