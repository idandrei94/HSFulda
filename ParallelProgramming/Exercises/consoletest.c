#include <stdio.h>
#include <conio.h>
#include <stdlib.h>
#include <windows.h>

#define KNRM  "\x1B[0m"
#define KRED  "\x1B[31m"
#define KGRN  "\x1B[32m"
#define KYEL  "\x1B[33m"
#define KBLU  "\x1B[34m"
#define KMAG  "\x1B[35m"
#define KCYN  "\x1B[36m"
#define KWHT  "\x1B[37m"

void set_console_to_default()
{
    HANDLE  hConsole;
    hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleTextAttribute(hConsole, FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_RED);
}

void set_console_xy(int x, int y)
{
    COORD coord;
    coord.X = 8;
    coord.Y = 8;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
}

int main(void)
{
    set_console_to_default();
    getchar();  // wait
    return EXIT_SUCCESS;
}