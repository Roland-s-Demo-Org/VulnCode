<?php
// Simulating tainted input from user
$taintedInput = $_GET['user_input'] ?? '';


class Class1 {
    private $input;

    public function __construct($input) {
        // Sanitize input: remove any characters that could be used for code injection
        // Only allow alphanumeric characters, spaces, and basic punctuation
        $this->input = $this->sanitizeInput($input);
    }

    private function sanitizeInput($input) {
        // Validate input type
        if (!is_string($input)) {
            return '';
        }
        
        // Remove any null bytes
        $input = str_replace("\0", '', $input);
        
        // Limit length to prevent abuse
        $input = substr($input, 0, 200);
        
        // Filter to only allow safe characters (alphanumeric, spaces, and basic punctuation)
        $input = preg_replace('/[^a-zA-Z0-9\s\.\,\!\?\-\_]/', '', $input);
        
        return $input;
    }

    public function processInput() {
        // Use htmlspecialchars to prevent XSS when outputting
        echo "Class1 processing: " . htmlspecialchars($this->input, ENT_QUOTES, 'UTF-8') . "\n";
        
        // SECURITY FIX: Removed eval() - it's unnecessary and dangerous
        // Simply output the sanitized string directly instead of using eval()
        echo "Evaluated in Class1: " . htmlspecialchars($this->input, ENT_QUOTES, 'UTF-8');
    }
}

// Create instances and pass tainted input
$obj1 = new Class1($taintedInput);

// Use the classes
$obj1->processInput();
?>
