# include <unistd.h>
# include <signal.h>
# include <sys/types.h>
# include <sys/wait.h>
# include <mach-o/dyld.h>
# include <limits.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>


char *main_dir = 0;
char *main_py = 0;

char python[PATH_MAX] = {0};
char *python_dir = 0;

char *pip = 0;
char *pip_dir = 0;


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

char *
concat(char *a, char *b)
{
	int full_size = strlen(a) + strlen(b);
    char *result = malloc(full_size + 1);
    sprintf(result, "%s%s", a, b);
	result[full_size] = '\0';
    return(result);
}

char *
dir_from_abs_path(char *file_path)
{
	char *last_slash = strrchr(file_path, '/') - 1;
	int dir_len = last_slash - file_path + 1;
	char *result = malloc(dir_len + 1); // \0
	strncpy(result, file_path, dir_len);
	result[dir_len] = '\0';
	return(result);
}


int // bool
find_python(void)
{
	FILE *python_in_p = popen("which python3", "r");
	int found_python = 0;
	if(fgets((char *)python, sizeof(python), python_in_p))
	{
		char *new_line = strrchr(python, '\n');
		if(new_line)
		{
			python[(int)(new_line - python)] = '\0';
		}
		found_python = 1;
	}
	else
	{
		printf("[ERROR] fgets(python) failed\n");
		exit(1);
	}
	return(found_python);
}

int // bool
find_pip(void)
{
	int result = 0;
	FILE *pip_in_p = popen(concat(python, " -m pip --version"), "r");
	char temp_pip[PATH_MAX * 10];
	if(pip_in_p == 0)
	{
		printf("[ERROR] Searching for pip\n");
		exit(1);
	}
	else
	{
		if(fgets((char *)temp_pip, sizeof(temp_pip), pip_in_p))
		{
			result = 1;
			char *path_start = strstr(temp_pip, "from ");
			if(!path_start)
			{
				result = 0;
				printf("[LOG] pip not installed\n");
			}
			else
			{
				path_start += 5;
				char *path_end = strchr(path_start, ' ');
				*path_end = '\0';
				pip = path_start;
			}
		}
		else
		{
			printf("[ERROR] fgets(pip) failed\n");
			exit(1);
		}
	}
	return(result);
}

int
main(int argc, char **argv)
{
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

    main_dir = binary_location;
    main_py = concat(main_dir, "/main.py");
	

	// Find/install python3
	if(!find_python())
	{
        printf("[LOG] Installing python3");
        system("curl -O https://www.python.org/ftp/python/3.10.0/python-3.10.0-macos11.pkg");
        system("sudo installer -pkg python-3.10.0-macos11.pkg -target /");
		if(!find_python())
		{
			printf("[ERROR] Couldn't install python3\n");
		}
		else
		{
			printf("[LOG] Installed python3: %s\n", python);
		}
	}
	else
	{
		printf("[LOG] Found python3: %s\n", python);
	}
	python_dir = dir_from_abs_path(python);

	// Find/install pip and packages
	if(!find_pip())
	{
		printf("[LOG] Installing pip\n");
		system(concat(python, " -m ensurepip --upgrade"));
		if(!find_pip())
		{
			printf("[ERROR] failed to install pip\n");
			exit(1);
		}
		else
		{
			printf("[LOG] pip installed: %s\n", pip);
		}
    }
	else
	{
		printf("[LOG]: found pip: %s\n", pip);
	}
#if 0

    // Sprintf command together
    char* command = malloc(2048);
    sprintf(command, "python3 %s/%s", binary_location, "main.py");

    ////////////////////////////////////////
    // Install python
    int python_instaled = (system("python3 --version > nul") == 0);
    if(!python_instaled)
    {
    }
    else
    {
        printf("Python3 is already installed\n");
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
        char installed_command[1024];
        sprintf(installed_command, "python3 -m pip show %s > /dev/null 2>&1", line);
        int installed = system(installed_command);
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

    atexit(kill_child);

    // Fork to run local server on and start browser with app
    if((process_id = fork()) == 0)
    {
        // Child
        system(command);
    }
    else if(process_id > 0)
    {
        // Parent
        sleep(1);
        system("open http://127.0.0.1:5000");
        pause();
    }
    else
    {
        printf("ERRR Creating child");
    }
#endif

    return(0);
}
