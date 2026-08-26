#include "processor.h"
#include <string.h>

// Function that processes and forwards the command
void process_command(const char *command) {
    // Validate command is not NULL before dispatching
    if (command == NULL || strlen(command) == 0) {
        return;
    }
    dispatch_command(command);
}