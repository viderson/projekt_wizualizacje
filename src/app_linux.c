#ifndef APP_LINUX_H
#define APP_LINUX_H


# include <unistd.h>
# include <signal.h>
# include <sys/types.h>
# include <sys/wait.h>


# define OPEN_BROWSER "xdg-open"


static char*
get_binary_location(void)
{
    char *result = malloc(2048);
    int len = readlink("/proc/self/exe", result, 2048-1);
    result[len] = '\0';
    return(result);
}


pid_t process_id = 0;
void kill_child(void)
{
    kill(process_id, SIGINT);
}

#endif // APP_LINUX_H
