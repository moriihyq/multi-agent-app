# main.py

from agent_factory import create_agent_executor

def main():
    """
    The main application loop.
    """
    while True:
        print("\n--- Welcome to Your Personal Research Agent ---")
        print("Please choose your desired agent mode:")
        print("1: AI Technology Analyst (Specialized for AI topics)")
        print("2: General Evidence-Driven Analyst (For any topic)")
        print("3: Exit")
        
        choice = input("> ")

        if choice == "1":
            # AI Analyst Mode
            topic = input("What AI topic would you like to research today?\n> ")
            print(f"\nReceived! Launching AI Analyst for topic: '{topic}'...")
            
            agent_executor = create_agent_executor(mode="ai")
            result = agent_executor.invoke({"input": topic})
            
            print("\n\n===== AI Analyst's Research Brief =====")
            print(result['output'])

        elif choice == "2":
            # General Analyst Mode
            topic = input("What topic would you like to research today?\n> ")
            user_profile = input("What is your academic/professional background? (e.g., SCUT AI Sophomore)\n> ")
            print(f"\nReceived! Launching General Analyst for topic: '{topic}'...")

            agent_executor = create_agent_executor(mode="general")
            result = agent_executor.invoke({
                "input": topic,
                "user_profile": user_profile
            })

            print("\n\n===== General Analyst's Research Brief =====")
            print(result['output'])

        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()