#ifndef APP_MACOS_H
#define APP_MACOS_H


# include <unistd.h>
# include <signal.h>
# include <sys/types.h>
# include <sys/wait.h>
# include <mach-o/dyld.h>
# include <limits.h>


#define OPEN_BROWSER "open"
#define PYTHON "python3"
#define PIP "pip3"


char*
get_binary_location(void)
{
    char *result = malloc(PATH_MAX);
    unsigned int result_size = PATH_MAX;
    _NSGetExecutablePath(result, &result_size);
    return(result);
}


pid_t process_id = 0;
void kill_child(void)
{
    kill(process_id, SIGINT);
}

#endif // APP_MACOS_H
