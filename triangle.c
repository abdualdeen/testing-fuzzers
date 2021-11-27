#include<stdio.h>

int main(int argc, char **argv){
    if (argc == 1) {
        printf("use: ./calc <expr>\n");
        return 0;
    }

   int side1, side2, side3;

   for(int i = 1; i < argc; i++) {
        int err = sscanf(argv[i], "%d,%d,%d",&side1,&side2,&side3);
        if (err != 3) {
                printf("wrong format!\n");
            } 
   }

   if(side1 == side2 && side2 == side3)
      printf("The Given Triangle is equilateral\n");
   else if(side1 == side2 || side2 == side3 || side3 == side1)
      printf("The given Triangle is isosceles\n");
   else
      printf("The given Triangle is scalene\n");
   return 0;
}