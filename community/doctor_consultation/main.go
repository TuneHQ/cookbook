package main

import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
)

func main() {
	url := "https://proxy.tune.app/chat/completions"
	apiKey := "sk-tune-Hj2Db2cpQZW0gXaTB8n8fAJp7k9XpxgzFs4"

	payload := map[string]interface{}{
		"temperature": 0.8,
		"messages": []map[string]string{
			{"role": "user", "content": "Hi"},
			{"role": "assistant", "content": "Hello, Sidharth! How can I assist you today? If you have any health concerns or symptoms you'd like to discuss, feel free to share."},
			{"role": "user", "content": "I want to book an appointment"},
			{"role": "assistant", "content": "Of course, Sidharth! I can help you with that. Could you please provide me with the following details? ..."},
			{"role": "user", "content": "Sidharth Sasikumar, my mobile number is 7827336442 and I would like to book for 24 Sep 11:30 to 12:30"},
			{"role": "assistant", "content": "Thank you for the details, Sidharth! Just to confirm, here’s what I have for your appointment ..."},
			{"role": "user", "content": "back pain"},
		},
		"model":             "Sid007/doctor-consultation",
		"stream":            false,
		"frequency_penalty": 0,
		"max_tokens":        900,
	}

	payloadBytes, err := json.Marshal(payload)
	if err != nil {
		fmt.Println("Error marshaling payload:", err)
		return
	}

	req, err := http.NewRequest("POST", url, bytes.NewReader(payloadBytes))
	if err != nil {
		fmt.Println("Error creating request:", err)
		return
	}

	req.Header.Add("Authorization", apiKey)
	req.Header.Add("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error sending request:", err)
		return
	}
	defer resp.Body.Close()

	fmt.Println("Response:")
	scanner := bufio.NewScanner(resp.Body)
	for scanner.Scan() {
		line := scanner.Text() // Use Text instead of Bytes for easier parsing
		if line != "[DONE]" {
			var jsonData map[string]interface{}
			err := json.Unmarshal([]byte(line), &jsonData) // Parse the entire line
			if err != nil {
				fmt.Println("Error parsing JSON:", err)
			} else {
				fmt.Println(jsonData)
			}
		}
	}
	if err := scanner.Err(); err != nil {
		fmt.Println("Error reading response:", err)
	}
}
