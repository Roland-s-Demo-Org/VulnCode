<?php
// Include the SWIG-generated PHP wrapper for C

dl("command.so");

// Start session for CSRF protection
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // CSRF token validation
    if (!isset($_POST['csrf_token']) || !isset($_SESSION['csrf_token']) || 
        !hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'])) {
        http_response_code(403);
        die("CSRF token validation failed");
    }
    
    // Validate that command parameter exists and is a string
    if (!isset($_POST['command']) || !is_string($_POST['command'])) {
        http_response_code(400);
        die("Invalid input");
    }
    
    $command = $_POST['command'];
    
    // Additional input validation: limit length to prevent abuse
    if (strlen($command) > 256) {
        http_response_code(400);
        die("Command too long");
    }
    
    // Ensure command is not empty after trimming
    $command = trim($command);
    if (empty($command)) {
        http_response_code(400);
        die("Empty command");
    }
    
    // Check for null bytes which can be used for injection
    if (strpos($command, "\0") !== false) {
        http_response_code(400);
        die("Invalid characters in command");
    }
    
    $command = sprintf("%s",$command);
    // Sanitize the user input (Important for security)
    $safe_command = escapeshellcmd($command);

    // Call the C function with sanitized input
    run_shell_command($safe_command);

    echo htmlspecialchars("Command executed: $safe_command", ENT_QUOTES, 'UTF-8');

}

// Generate CSRF token for the form
if (!isset($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PHP to C Command Executor</title>
</head>
<body>
    <h2>Execute a Command</h2>
    <form method="POST">
        <input type="hidden" name="csrf_token" value="<?php echo htmlspecialchars($_SESSION['csrf_token'], ENT_QUOTES, 'UTF-8'); ?>">
        <label for="command">Enter Command:</label>
        <input type="text" id="command" name="command" required maxlength="256">
        <button type="submit">Run</button>
    </form>
</body>
</html>
