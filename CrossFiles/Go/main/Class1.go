package main

import (
	"fmt"
	"os/exec"
	"regexp"
)

type Class1 struct {
	input string
}

func NewClass1(input string) *Class1 {
	return &Class1{input: input}
}

func (c *Class1) Process() {
	fmt.Printf("Class1 processing: %s\n", c.input)
	validInput := regexp.MustCompile(`^[a-zA-Z0-9_\-\./\\]+$`)
	if !validInput.MatchString(c.input) {
		fmt.Printf("Error executing command: %v\n", fmt.Errorf("invalid input"))
		return
	}
	// Potentially unsafe operation
	cmd := exec.Command("echo", c.input)
	output, err := cmd.Output()
	if err != nil {
		fmt.Printf("Error executing command: %v\n", err)
		return
	}
	fmt.Printf("Command output: %s", output)
}
