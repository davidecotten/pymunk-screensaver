#include <iostream>
#include <Windows.h>
using namespace std;

int main(int argc, char *argv[])
{
    WinExec("python \"C:\\pymunk-screensaver\\main.py\"", SW_HIDE);
    return 0;
}