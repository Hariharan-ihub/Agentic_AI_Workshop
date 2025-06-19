from agent import run_travel_agent

def main():
    destination = input('Enter your travel destination: ')
    result = run_travel_agent(destination)
    print(result)

if __name__ == '__main__':
    main() 