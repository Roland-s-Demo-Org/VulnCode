<?php

class Class1 {
    private $input;

    public function __construct($input) {
        $this->input = $input;
    }

    public function process() {
        echo "Class1 processing: {$this->input}\n";
        // Potentially unsafe operation
        // Security fix: escapeshellarg() wraps user input to prevent shell injection
        system("echo " . escapeshellarg($this->input));
    }
}
?>
