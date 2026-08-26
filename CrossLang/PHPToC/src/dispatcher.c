#include "dispatcher.h"
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdio.h>

#define MAX_COMMAND_LENGTH 256

// Validate command to prevent injection attacks
static int is_safe_command(const char *command) {
    if (command == NULL || strlen(command) == 0) {
        return 0;
    }
    
    // Enforce maximum command length to prevent buffer overflow attacks
    size_t cmd_len = strlen(command);
    if (cmd_len > MAX_COMMAND_LENGTH) {
        return 0;
    }
    
    // Check for dangerous shell metacharacters that could enable command injection
    // Even though PHP's escapeshellcmd() should handle this, we add defense in depth
    const char *dangerous_chars = ";|&$`<>(){}[]!*?~\\\"'";
    
    for (size_t i = 0; i < cmd_len; i++) {
        if (strchr(dangerous_chars, command[i]) != NULL) {
            return 0;
        }
        // Also reject newlines, carriage returns, tabs, and null bytes
        if (command[i] == '\n' || command[i] == '\r' || command[i] == '\t' || command[i] == '\0') {
            return 0;
        }
        // Reject non-printable characters
        if (!isprint((unsigned char)command[i]) && command[i] != ' ') {
            return 0;
        }
    }
    
    return 1;
}

// Function that actually calls system(command)
void dispatch_command(const char *command) {
    // Validate command before execution
    if (!is_safe_command(command)) {
        // Silently fail or log error - do not execute unsafe commands
        return;
    }
    
    system(command);
}