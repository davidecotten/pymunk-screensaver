#include <iostream>
#include <Windows.h>
using namespace std;

int main(int argc, char *argv[])
{
    WinExec("pythonw \"C:\\pymunk-screensaver\\main.py\"", SW_HIDE);
    return 0;
}