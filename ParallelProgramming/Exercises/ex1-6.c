#include <stdio.h>
#include <time.h> 
#include <stdlib.h> 
#include <math.h>
#include <stdint.h>

// Solution to the stable marriage problem. 

// Enable or disable graphics
#define GRAPHICS 0

#ifdef GRAPHICS
#if GRAPHICS
#include <conio.h>
#include <windows.h>
#endif
#endif

// SIZE determines the group size (number of men or women)
#define SIZE 20

// Any available man/woman will have this status
#define STATUS_AVAILABLE -1

/*  Used to keep track of each man's compromise
*   0 means no compromise, the man asks out the woman he prefers most
*   4 means 4 compromises, the man asks out the 5th woman in order of preference
*/
int proposal_index[SIZE];

/*  Shuffles the elements of the given array
*   @param arr          the array to be shuffled
*   @post               the array's elements will be shuffled
*/

#ifdef GRAPHICS 
#if GRAPHICS

/*  Restores console background and foreground colors
*/
void set_console_to_default()
{
    HANDLE  hConsole;
    hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_RED);
}

/*  Sets the console foreground color to green
*/
void set_console_highlight()
{
    HANDLE  hConsole;
    hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, FOREGROUND_INTENSITY | FOREGROUND_GREEN);
}

/*  Sets the console foreground color to red
*/
void set_console_warning()
{
    HANDLE  hConsole;
    hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, FOREGROUND_INTENSITY | FOREGROUND_RED);
}

/*  Clears the screen
*/
void clrscr()
{
    #if defined(__linux__) || defined(__unix__) || defined(__APPLE__)
        system("clear");
    #endif

    #if defined(_WIN32) || defined(_WIN64)
        system("cls");
    #endif
}

/*  Clears the screen and draws the current state.
*   Should be called after each change in status
*   @param m_status     the status of each man, either STATUS_AVAILABLE or the index of a woman ([0..SIZE-1])
*   @param w_status     the status of each woman, either STATUS_AVAILABLE or the index of a man ([0..SIZE-1])
*   @param man          the index of the man who'se status changed
*   @param woman        the index of the woman the man just got engaged to, not needed if she was single prior to proposal
*   @param dumped_man   the index of the man the woman was previously engaged to, -1 if she was single prio to proposal
*/
void draw(
    int m_status[SIZE], 
    int w_status[SIZE],
    int man,
    int woman,
    int dumped_man )
{   
    #ifdef GRAPHICS
        #if GRAPHICS == 0
            return;
        #endif
    #endif
    clrscr();
    for (int i = 0; i < SIZE; ++i)
    {
        if (i == man)
        {
            set_console_highlight();
            printf("Man #%d engaged to Woman #%d.\n", i+1, m_status[i]+1);
            set_console_to_default();
        }
        else if (i == dumped_man)
        {
            set_console_warning();
            printf("Man #%d dumped by Woman #%d.\n", i+1, woman+1);
            set_console_to_default();
        }
        else
        {
            if(m_status[i] != -1)
                printf("Man #%d engaged to Woman #%d.\n", i+1, m_status[i]+1);
            else
                printf("Man #%d is single.\n", i+1);
        }
    }
    getchar();
}
#endif
#endif

/*  Shuffles an array
*   @param arr          the array to be shuffled
*   @pre                the random seed must be initialized prior to calling rand_perm
*   @post               the array will contain a random permutation of the initial array
*/
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

/*  Initializes various initial values
*   @pre                the m_pref and w_pref matrices must be matrices of form [SIZE][SIZE]
*   @post               random seed initialized
*   @post               all spouse statuses are set to available
*   @post               references of each man and woman are random permutations of [0..SIZE-1]
*/
void init_data(
    int m_status[SIZE], 
    int w_status[SIZE], 
    int m_pref[][SIZE],
    int w_pref[][SIZE] )
{
    srand(time(0)); 
    for(int i = 0; i < SIZE; ++i)
    {
        m_status[i] = w_status[i] = STATUS_AVAILABLE;
        proposal_index[i] = 0;
        for(int j = 0; j < SIZE; ++j)
        {
            m_pref[i][j] = w_pref[i][j] = j;
        }
        rand_perm(m_pref[i]);
        rand_perm(w_pref[i]);
    }
}

/*  Finds the minimum value in an array
*   @param arr          the array to search in
*   @return             the minimum value in the arr
*/
int arr_min(
    int arr[SIZE] )
{
    int min = arr[0];
    for(int i = 1; i < SIZE; ++i)
        if(arr[i] < min)
            min = arr[i];
    return min;
}

/*  Make a man propose to a woman
*   @param m_pref       2D square matrix, m_pref[i][j] is "i" man's rating for woman "j"
*   @param w_pref       2D matrix, w_pref[i][j] is "i" woman's rating for man "j"
*   @param m_status     the status of each man, either STATUS_AVAILABLE or the index of a woman ([0..SIZE-1])
*   @param w_status     the status of each woman, either STATUS_AVAILABLE or the index of a man ([0..SIZE-1])
*   @pre                the m_pref and w_pref matrices must be matrices of form [SIZE][SIZE]
*   @post               if proposal successful, statuses will update accordingly
*/
void propose(
    int m_pref[][SIZE], 
    int w_pref[][SIZE], 
    int m_status[SIZE], 
    int w_status[SIZE], 
    int man, 
    int woman )
{
    
    if(woman == -1)                                                  // If the man's already engaged (doesn't want to propose anymore)
        return;
    if(w_status[woman] == -1)                                        // Is the woman available? 
    {
        w_status[woman] = man;                                       // Get engaged
        m_status[man] = woman;
#ifdef GRAPHICS
#if GRAPHICS
        draw(m_status, w_status, man, -1, -1);
#endif
#endif
    }
    else if(w_pref[woman][man] > w_pref[woman][w_status[woman]])     // Cheating gold digger? (likes this man more)
    {
        int dumped_man = w_status[woman];
        m_status[dumped_man] = -1;                                   // Dump the other man first
        w_status[woman] = man;                                       // Get engaged
        m_status[man] = woman;
#ifdef GRAPHICS
#if GRAPHICS
        draw(m_status, w_status, man, woman, dumped_man);
#endif
#endif
    }
}

/* Searches for a value in an array
*   @param arr          the array to search in
*   @param value        the value to search for
*   @return             the first index where the value is found, -1 if not found
*/
int indexof(
    int arr[SIZE], 
    int value )
{
    for(int i = 0; i < SIZE; ++i)
    {
        if(arr[i] == value)
            return i;
    }
    return -1;
}

/*  Each round single men pick a woman to propose to, engaged men pick -1
*   @param m_pref       2D square matrix, m_pref[i][j] is "i" man's rating for woman "j"
*   @param w_pref       2D matrix, w_pref[i][j] is "i" woman's rating for man "j"
*   @param m_status     the status of each man, either STATUS_AVAILABLE or the index of a woman ([0..SIZE-1])
*   @param w_status     the status of each woman, either STATUS_AVAILABLE or the index of a man ([0..SIZE-1])
*   @pre                the m_pref and w_pref matrices must be matrices of form [SIZE][SIZE]
*/
void find_wife(
    int m_status[SIZE], 
    int w_status[SIZE], 
    int m_pref[][SIZE], 
    int w_pref[][SIZE], 
    int proposals[SIZE] )
{
    for(int man = 0; man < SIZE; ++man)
    {
        if(m_status[man] != -1)                                                 // If engaged, don't propose to anyone
        {
            proposals[man] = -1;
        }
        else
        {
            proposals[man] = indexof(m_pref[man], SIZE-1-proposal_index[man]);  // Ask the next woman in order of preference
            ++proposal_index[man];                                              // Next time will make a bigger compromise
        }
    }
}

/*  Each single man attempts to propose to the chosen woman
*   @param m_pref       2D square matrix, m_pref[i][j] is "i" man's rating for woman "j"
*   @param w_pref       2D matrix, w_pref[i][j] is "i" woman's rating for man "j"
*   @param m_status     the status of each man, either STATUS_AVAILABLE or the index of a woman ([0..SIZE-1])
*   @param w_status     the status of each woman, either STATUS_AVAILABLE or the index of a man ([0..SIZE-1])
*   @pre                the m_pref and w_pref matrices must be matrices of form [SIZE][SIZE]
*   @post               each successful proposal will alter the statuses of those involved
*/
void manage_proposals(
    int m_status[SIZE], 
    int w_status[SIZE], 
    int m_pref[][SIZE], 
    int w_pref[][SIZE], 
    int proposals[SIZE] ) 
{
    for(int man = 0; man < SIZE; ++man)
        propose(m_pref, w_pref, m_status, w_status, man, proposals[man]);
}

/*  Check if all couples are stable
*   @param m_pref       2D square matrix, m_pref[i][j] is "i" man's rating for woman "j"
*   @param w_pref       2D matrix, w_pref[i][j] is "i" woman's rating for man "j"
*   @param m_status     the status of each man, either STATUS_AVAILABLE or the index of a woman ([0..SIZE-1])
*   @param w_status     the status of each woman, either STATUS_AVAILABLE or the index of a man ([0..SIZE-1])
*   @pre                the m_pref and w_pref matrices must be matrices of form [SIZE][SIZE]
*   @return             1 if all pairs are stable, 0 otherwise
*/
int check(
    int m_status[SIZE], 
    int w_status[SIZE], 
    int m_pref[][SIZE], 
    int w_pref[][SIZE] )
{
    for(int i = 0; i < SIZE; ++i)
    {
        if(w_status[m_status[i]] != i)
        {
            printf("Incorrect match\n");
            return 0;
        }
        for(int j = 0; j < SIZE; ++j)
        {
            if(i != j)                  // M1W1 M2W2 
            {
                int M1 = i;
                int M2 = j;
                int W1 = m_status[i];
                int W2 = m_status[j];
                if(w_pref[W2][M1] > w_pref[W2][M2] && m_pref[M1][W2] > m_pref[M1][W1])
                {
                    printf("Woman", W2, "and man", M1, "prefer each other over their spouses");
                    return 0;
                }
                if(w_pref[W1][M2] > w_pref[W1][M1] && m_pref[M2][W1] > m_pref[M2][W2])
                {
                    printf("Woman", W1, "and man", M2, "prefer each other over their spouses");
                    return 0;
                }
            }  
        }
    }
    return 1;
}

int m_status[SIZE], w_status[SIZE], m_pref[SIZE][SIZE], w_pref[SIZE][SIZE];
int main(void)
{
    init_data(m_status, w_status, m_pref, w_pref);

    time_t real_time = time(NULL);
	clock_t cpu_time = clock();

    while(arr_min(m_status) == -1)
    {
        int proposals[SIZE];
        find_wife(m_status, w_status, m_pref, w_pref, proposals);
        manage_proposals(m_status, w_status, m_pref, w_pref, proposals);
    }
    time_t end_real_time = time(NULL);
	clock_t end_cpu_time = clock();
    printf("Calculation complete in %ld seconds and %f seconds CPU time, result is %s", diff_time(end_real_time - real_time), ((float)(end_cpu_time - cpu_time))/CLOCKS_PER_SEC, check(m_status, w_status, m_pref, w_pref) ? "correct.\n" : "incorrect.\n"); 
    return EXIT_SUCCESS;
}
