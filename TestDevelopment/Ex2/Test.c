#include <stdio.h>
#include <stdlib.h>

#include "TestObject.c"

#define TEST_SUCCESS    1
#define TEST_FAIL       0
#define TEST_COUNT      3

typedef int TEST_RESULT;

TEST_RESULT test1_tempErfassen_validate_input();
TEST_RESULT test2_mittelwert_validate_output();
TEST_RESULT test3_tempTagAusgabe_validate_output();
  

TEST_RESULT test1_tempErfassen_validate_input()
{
    float input[7] = {12, 21, 16, 18, 22, 10, 9};
    float output[7];
    printf("Please input the values 12, 21, 16, 18, 22, 10, 9\n");
    tempErfassen(output, 7);
    for (int i = 0; i < 7; ++i)
        if(input[i] != output[i])
            printf("Test errors, expected %f but received %f\n", input[i], output[i]);
            return TEST_FAIL;
    return TEST_SUCCESS;
}

TEST_RESULT test3_tempTagAusgabe_validate_output()
{
    float input[7] = {12, 21, 16, 18, 22, 10, 9};
    printf("Please input 3 when prompted\n");
    tempTagAusgabe(input);
    printf("Was the output \" Tag 3: 16.00 Grad Celsius\" (input 1 for yes and 0 for no)\n");
    int choice;
    scanf("%d", &choice);
    return choice == 1 ? TEST_SUCCESS : TEST_FAIL;
}


TEST_RESULT test2_mittelwert_validate_output()
{
    float input[7] = {1,2,3,4,5,6,7};
    float output = mittelwert(input, 7);
    //TODO fix float comparison.....
    if ( output == 4.0f)
    {
        return TEST_SUCCESS;
    }
    else
    {
        printf("%s failed, expected 4 but received %f\n", __func__, output);
        return TEST_FAIL;
    }
}

int main(void)
{
    TEST_RESULT results = 0;
    results += test1_tempErfassen_validate_input();
    results += test3_tempTagAusgabe_validate_output();
    results += test2_mittelwert_validate_output();

    printf("Testing complete, %d successful tests out of %d", results, TEST_COUNT);

    return EXIT_SUCCESS;
}