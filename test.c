#include<stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    // if (argc == 1) {
    //     printf("use: ./test <expr>\n");
    //     return 1;
    // }
    
    // printf("%s\n", argv[1]);
    // return 0;
    char code[] = "test";
    if (strcmp(argv[1], code) == 0)
    {
        // printf("%s\n", "hello");
        // printf("%s\n", argv[1]);
        return 0;
    }
    return 1;

}