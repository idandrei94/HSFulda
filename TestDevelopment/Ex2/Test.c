/*  Authors
*   Samina Zahid 1156074
*   Dan Iorga    1154111
*/


#include <stdio.h>
#include <stdlib.h>

#include "TestObject.c"

#define TEST_SUCCESS    1
#define TEST_FAIL       0

typedef int TEST_RESULT;

TEST_RESULT test1_tempErfassen_validate_input();
TEST_RESULT test2_mittelwert_validate_output();
TEST_RESULT test3_tempTagAusgabe_validate_output();
TEST_RESULT test4_tempTagAusgabe_validate_short_output();
  

TEST_RESULT test1_tempErfassen_validate_input()
{
    float input[7] = {12, 21, 16, 18, 22, 10, 9};
    float output[7];
    printf("Please input the values 12, 21, 16, 18, 22, 10, 9\n");
    tempErfassen(output, 7);
    for (int i = 0; i < 7; ++i)
        if(input[i] != output[i])
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
    if(choice == 1)
    {
        return TEST_SUCCESS;
    }
    else
    {
        return TEST_FAIL;
    }
}


TEST_RESULT test2_mittelwert_validate_output()
{
    float input[7] = {1,2,3,4,5,6,7};
    float output = mittelwert(input, 7);
    //TODO fix float comparison.....
    if ( output > 3.99f && output < 4.01f)
    {
        return TEST_SUCCESS;
    }
    else
    {
        return TEST_FAIL;
    }
}

TEST_RESULT test4_tempTagAusgabe_validate_short_output()
{
    float input[7] = {1,2,3,4,5,6,7};
    float output = mittelwert(input, 4);
    //TODO fix float comparison.....
    if ( output > 2.49f && output < 2.51)
    {
        return TEST_SUCCESS;
    }
    else
    {
        return TEST_FAIL;
    }
}

int main(void)
{
    printf("Test 1 result was %d\n", test1_tempErfassen_validate_input());
    printf("Test 2 result was %d\n", test2_mittelwert_validate_output());
    printf("Test 3 result was %d\n", test3_tempTagAusgabe_validate_output());
    printf("Test 4 result was %d\n", test4_tempTagAusgabe_validate_short_output());

    return EXIT_SUCCESS;
}