#include<stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    char code[] = "test";
    if (strcmp(argv[1], code) == 0)
    {
        return 0;
    }
    return 1;
}

