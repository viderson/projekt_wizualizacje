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

////////////////////////////////////////
// Headers
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#if WINDOWS
# include <Windows.h>
#elif LINUX
# include <unistd.h>
# include <signal.h>
# include <sys/types.h>
# include <sys/wait.h>
#elif MACOS
# include <unistd.h>
# include <signal.h>
# include <sys/types.h>
# include <sys/wait.h>
# include <mach-o/dyld.h>
# include <limits.h>
#endif


////////////////////////////////////////
// Command to start browser
#if WINDOWS
# define OPEN_BROWSER "start"
#elif LINUX
# define OPEN_BROWSER "xdg-open"
#elif MACOS
# define OPEN_BROWSER "open"
#endif

////////////////////////////////////////
// Binary location
#if WINDOWS
char*
get_binary_location(void)
{
    char *result = malloc(MAX_PATH * sizeof(char));
    GetModuleFileName(0, result, MAX_PATH);
    return(result);
}
#elif LINUX
char*
get_binary_location(void)
{
    char *result = malloc(2048);
    int len = readlink("/proc/self/exe", result, 2048-1);
    result[len] = '\0';
    return(result);
}
#elif MACOS
char*
get_binary_location(void)
{
    char *result = malloc(PATH_MAX);
    unsigned int result_size = PATH_MAX;
    _NSGetExecutablePath(result, &result_size);
    return(result);
}
#endif

////////////////////////////////////////
// Killing child
#if WINDOWS
PROCESS_INFORMATION processInfo = {0};
STARTUPINFO startupInfo = {0};
void kill_child(void)
{
    TerminateProcess(processInfo.hProcess, 0);
    CloseHandle(processInfo.hProcess);
    CloseHandle(processInfo.hThread);
}
#elif LINUX || MACOS
pid_t process_id = 0;
void kill_child(void)
{
    kill(process_id, SIGINT);
}
#endif

////////////////////////////////////////
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
    sprintf(command, "py -3 %s/%s", binary_location, "main.py");

    ////////////////////////////////////////
    // Install python
#ifdef SETUP

    int python_instaled = (system("py -3 --version > nul") == 0);
    if(!python_instaled)
    {
        printf("Installing python3");
#if WINDOWS
        system("winget install -e --id Python.Python.3.12");
#elif MACOS
        // install brew
        system("/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"");
        system("brew install python");
#elif LINUX
        // TODO(Pawel Hermansdorfer): Which package manager???
#endif
        system("py -3 -m ensurepip --upgrade");
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
        line[strcspn(line, "\n")] = 0;


        // Check if the package is already installed
#if WINDOWS
        char installed_command[1024];
        sprintf(installed_command, "pip show %s 2> nul", line);
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
        sprintf(installed_command, "pip show %s > /dev/null 2>&1", line);
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
            sprintf(install_command, "pip install %s", line);
            system(install_command);
            printf("Installing package: %s\n", line);
        }
    }
#else // SETUP
    ////////////////////////////////////////
    // Let's kill child :D
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
