#include "command.h"
#include <string.h>

#define MAX_COMMAND_LENGTH 256

// Function to execute a shell command
void run_shell_command(const char *command) {
    // Additional safety check: validate command is not NULL and within bounds
    if (command == NULL || strlen(command) == 0 || strlen(command) > MAX_COMMAND_LENGTH) {
        return;
    }
    execute_command(command);
}

