"""
Test script for course mentor API
Run: python test_mentor.py
"""
import requests
import json

# Test the mentor endpoint
def test_mentor():
    url = "http://localhost:8000/api/chat/mentor/respond/"
    
    test_cases = [
        {
            "course_id": "mutual-sip",
            "module_id": "m1",
            "question": "What is a SIP?"
        },
        {
            "course_id": "budgeting-saving",
            "module_id": "m1",
            "question": "What is 50/30/20?"
        },
        {
            "course_id": "investing-101",
            "module_id": "m1",
            "question": "Tell me about diversification"
        }
    ]
    
    print("Testing Course Mentor API\n" + "="*50)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['question']}")
        print(f"Course: {test['course_id']}, Module: {test['module_id']}")
        
        try:
            response = requests.post(
                url,
                json=test,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Success")
                print(f"Type: {data.get('type', 'unknown')}")
                print(f"Answer: {data.get('reply', data.get('answer', ''))[:200]}...")
                if data.get('source'):
                    print(f"Source: {data.get('source')}")
            else:
                print(f"✗ Error: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"✗ Exception: {str(e)}")
    
    print("\n" + "="*50)
    print("Test completed!")

if __name__ == "__main__":
    test_mentor()

