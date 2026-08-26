#include "executor.h"
#include <string.h>

// Function that passes the command to the next level
void execute_command(const char *command) {
    // Validate command is not NULL before passing to next layer
    if (command == NULL || strlen(command) == 0) {
        return;
    }
    process_command(command);
}
