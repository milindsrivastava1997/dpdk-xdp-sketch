#include <stdio.h>

#include "hash.h"

int main() {
    unsigned char input1[3] = "a\n";
    unsigned char input2[5] = "abc\n";

    printf("%s %x\n", input1, XXHash32::hash(input1, 2, 0));
    printf("%s %x\n", input2, XXHash32::hash(input2, 4, 0));

    return 0;
}
