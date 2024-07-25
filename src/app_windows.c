#ifndef APP_WINDOWS_H
#define APP_WINDOWS_H


#include <Windows.h>


#define OPEN_BROWSER "start"
#define PYTHON "py -3"
#define PIP "pip"



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

#ifdef _WIN32
# define WINDOWS 1
#else
# define WINDOWS 0
#endif

#ifdef __APPLE__
# define MACOS 1
#else
#define MACOS 0
#endif

#ifdef __linux__
# define LINUX 1
#else
# define LINUX 0
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#if WINDOWS
# include "app_windows.c"
#elif LINUX
# include "app_windows.c"
#elif MACOS
# include "app_macos.c"
#endif


int
main(int argc, char **argv)
{
    ////////////////////////////////////////
    // Find path to main.py
    char *binary_location = get_binary_location();
    char *last_slash_pos = binary_location;
    for(char *p = binary_location; *p; ++p)
    {
        if(*p == '/' || *p == '\\')
        {
            last_slash_pos = p;
        }
    }
    *last_slash_pos = '\0';

    // Sprintf command together
    char* command = malloc(2048);
    sprintf(command, PYTHON " %s/%s", binary_location, "main.py");

    ////////////////////////////////////////
    // Install python
#ifdef SETUP

    int python_instaled = (system(PYTHON " --version > nul") == 0);
    if(!python_instaled)
    {
        printf("Installing python3");
#if WINDOWS
        system("curl -o python-3.9.1.exe https://www.python.org/ftp/python/3.9.1/python-3.9.1-amd64.exe");
        system("python-3.9.1.exe /quiet InstallAllUsers=1 PrependPath=1");
        system("setlocal");
        system("setx PATH \"%PATH%\"");
        system("endlocal");
#elif MACOS | LINUX
        system("curl -O https://www.python.org/ftp/python/3.10.0/python-3.10.0-macos11.pkg");
        system("sudo installer -pkg python-3.10.0-macos11.pkg -target /");
        system("exec bash -l");
#endif
        system(PYTHON " -m ensurepip --upgrade");
    }
    else
    {
        printf("Python3 already installed\n");
    }

    ////////////////////////////////////////
    // Install packages
    char *requirements_location = malloc(2048);
    sprintf(requirements_location, "%s/%s", binary_location, "requirements.txt");
    FILE *requirements_file = fopen(requirements_location, "r");
    if(requirements_file == 0) {
        printf("Couldn't find requirements.txt");
        return(0);
    }

    char line[1024];
    long len = 0;
    long read;
    while(fgets(line, sizeof(line), requirements_file))
    {
        // Remove newline character from the end of the line
        // line[strcspn(line, "\n")] = 0;
        for(int i = 0; i < sizeof(line); ++i)
        {
            if(!isalpha(line[i]))
            {
                line[i] = '\0';
                break;
            }
        }


        // Check if the package is already installed
#if WINDOWS
        char installed_command[1024];
        sprintf(installed_command, PIP " show %s 2> nul", line);
        FILE *pipe = _popen(installed_command, "r");
        char buffer[1024];
        int installed = 0;
        while(fgets(buffer, sizeof(buffer), pipe) != 0)
        {
            if(strstr(buffer, "Name: ") == buffer)
            {
                installed = 1;
                break;
            }
        }
        _pclose(pipe);
#elif LINUX || MACOS
        char installed_command[1024];
        sprintf(installed_command, PIP " show %s > /dev/null 2>&1", line);
        int installed = system(installed_command);
#endif
        if(installed)
        {
            printf("Package %s is already installed.\n", line);
        }
        else
        {
            // Install the package if it is not installed
            char install_command[1024];
            sprintf(install_command, PIP " install %s", line);
            system(install_command);
            printf("Installing package: %s\n", line);
        }
    }

#else // RUN
    ////////////////////////////////////////
    atexit(kill_child);

    // Fork to run local server on and start browser with app
#if WINDOWS
    startupInfo.cb = sizeof(startupInfo);
    if(CreateProcess(0, (LPSTR)command, 0, 0, 0, 0, 0, 0, &startupInfo, &processInfo))
    {
        Sleep(1000);
        system(OPEN_BROWSER " http://127.0.0.1:5000");
        for(;;)
        {
            Sleep(1000);
        }

    }
#elif LINUX || MACOS
    if((process_id = fork()) == 0)
    {
        // Child
        system(command);
    }
    else if(process_id > 0)
    {
        // Parent
        sleep(1);
        system(OPEN_BROWSER " http://127.0.0.1:5000");
        pause();
    }
    else
    {
        printf("ERRR Creating child");
    }
#endif
#endif // Setup

    return 0;
}
