#include <stdio.h>
#include <time.h> 
#include <stdlib.h> 
#include <math.h>
#include <stdint.h>

#define SIZE 5

int proposal_index[SIZE];

void rand_perm(
    int arr[SIZE] )
{
    for (int i = SIZE-1; i >= 0; --i)
    {
        //generate a random number [0, SIZE-1]
        int j = rand() % (i+1);
        int tmp = arr[i];
        arr[i] = arr[j];
        arr[j] = tmp;
    }
}

void init_data(
    int *m_status, 
    int *w_status, 
    int **m_pref,
    int **w_pref )
{
    srand(time(0)); 
    for(int i = 0; i < SIZE; ++i)
    {
        m_status[i] = w_status[i] = -1;
        proposal_index[i] = 0;
        for(int j = 0; j < SIZE; ++j)
        {
            m_pref[i][j] = (w_pref[i])[j] = j;
        }
        rand_perm(m_pref[i]);
        rand_perm(w_pref[i]);
    }
}

int arr_min(
    int *arr )
{
    int min = arr[0];
    for(int i = 1; i < SIZE; ++i)
        if(arr[i] < min)
            min = arr[i];
    return min;
}

void propose(
    int *m_status, 
    int *w_status, 
    int **m_pref, 
    int **w_pref, 
    int man, 
    int woman )
{

}

int index(
    int *arr, 
    int value )
{
    for(int i = 0; i < SIZE; ++i)
    {
        if(arr[i] == value)
            return i;
    }
    return -1;
}

void find_wife(
    int *m_status, 
    int *w_status, 
    int **m_pref, 
    int **w_pref, 
    int *proposals)
{
    for(int man = 0; man < SIZE; ++man)
    {
        if(m_status[man] != -1)
        {
            proposals[man] = -1;
        }
        else
        {
            proposals[man] = index(m_pref[man], SIZE-1-proposal_index[man]);
            ++proposal_index[man];
        }
    }
}

void manage_proposals(
    int* m_status, 
    int* w_status, 
    int** m_pref, 
    int** w_pref, 
    int* proposals) 
{
    for(int man = 0; man < SIZE; ++man)
        propose(m_pref, w_pref, m_status, w_status, man, proposals[man]);
}

int main(void)
{
    int m_status[SIZE], w_status[SIZE], m_pref[SIZE][SIZE], w_pref[SIZE][SIZE];
    init_data(m_status, w_status, m_pref, w_pref);

    while(arr_min(m_status) == -1)
    {
        int proposals[SIZE];
        find_wife(m_status, w_status, m_pref, w_pref, proposals);
        manage_proposals(m_status, w_status, m_pref, w_pref, proposals);
    }

    return 0;
}