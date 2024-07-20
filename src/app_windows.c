#ifndef APP_WINDOWS_H
#define APP_WINDOWS_H


#include <Windows.h>


#define OPEN_BROWSER "start"
#define PYTHON "py -3"



static char*
get_binary_location(void)
{
    char *result = malloc(MAX_PATH * sizeof(char));
    GetModuleFileName(0, result, MAX_PATH);
    return(result);
}

PROCESS_INFORMATION processInfo = {0};
STARTUPINFO startupInfo = {0};
void kill_child(void)
{
    TerminateProcess(processInfo.hProcess, 0);
    CloseHandle(processInfo.hProcess);
    CloseHandle(processInfo.hThread);
}

#endif // APP_WINDOWS_H
