import re
import sys



class response:
    def __init__(self, time):
        self.time_start = time
        self.time_end = None
        self.message = ""
        self.user = None

    def set_user(self, user):
        self.user = user
    
    def add_message(self, message, time):
        self.message += message + '\n'
        self.time_end = time
    
    def __str__(self):
        return f"{self.user}:\n {self.time_start} - {self.time_end}:\n {self.message}"

class user_data:
    def __init__(self, name):
        self.name = name
        self.count = 0
        self.len = 0
        self.pure_non_text_reply_count = 0
        self.accumulated_response_time = 0
    
    def add_response(self, response, prev_time):
        self.count += 1
        self.len += len(response.message)
        if response.message == '[表情]\n':
            self.pure_non_text_reply_count += 1
        if prev_time is not None:
            self.accumulated_response_time += calculate_time_difference(prev_time, response.time_start)

    def __str__(self):
        return f"User: {self.name}\n" \
               f"Response Count: {self.count}\n" \
               f"Average Response Time: {self.calculate_average_response_time():.2f}\n" \
               f"Average Response Length: {self.calculate_average_response_length():.2f}\n" \
               f"Pure Non-Text Reply Frequency: {self.calculate_pure_non_text_reply_frequency():.2f}\n"

    def calculate_average_response_time(self):
        if self.count > 1:
            return self.accumulated_response_time / (self.count - 1)
        else:
            return 0

    def calculate_average_response_length(self):
        if self.count > 0:
            return self.len / (self.count)
        else:
            return 0

    def calculate_pure_non_text_reply_frequency(self):
        if self.count > 0:
            return self.pure_non_text_reply_count / (self.count)
        else:
            return 0

output_name = None

def set_output(name : str):
    global output_name
    output_name = name + '.txt'
    with open(output_name, 'w') as file:
        pass  # This opens the file in write mode and immediately closes it, effectively clearing its content


def print_file(x):
    # Open a text file for writing
    with open(output_name, 'a') as f:
        # Redirect standard output (stdout) to the text file
        sys.stdout = f
        
        # Now, all print statements will be directed to the file
        print(x)
        
        # Don't forget to reset stdout to its default value when you're done
        sys.stdout = sys.__stdout__


responses = []
users = {}


def load_chat_log(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines if line.strip() != ""]
    return lines

def calculate_time_difference(time1, time2):
    h1, m1 = map(int, time1.split(':'))
    h2, m2 = map(int, time2.split(':'))
    return (h2 - h1) * 60 + (m2 - m1)

def process_chat_log(lines, longest_pause):
    current_user = None
    current_time = None
    current_message = ""

    for i, line in enumerate(lines):
        # Use regular expression to match lines like 'mike 17:06' or 'johndoe 17:09'
        match = re.match(r'(\w+) (\d{2}:\d{2})', line)
        if match:
            current_message = lines[i+1]
            user, time = match.groups()
            if user == current_user and (current_time == None or calculate_time_difference(current_time, time) <= longest_pause):
                responses[-1].add_message(current_message, time) 
            else:
                responses.append(response(time))
                responses[-1].set_user(user)
                responses[-1].add_message(current_message, time)

            current_user = user
            current_time = time
    return

def calculate_users():
    p_time = None
    for response in responses:
        if response.user not in users:
            users[response.user] = user_data(response.user)
        users[response.user].add_response(response, p_time)
        p_time = response.time_end


if __name__ == "__main__":
    file_path = "conversation.txt"
    set_output("output")
    longest_pause = 1  # Longest pause between messages to be considered a new response

    lines = load_chat_log(file_path)
    #print(lines)

    process_chat_log(lines, longest_pause)
    for x in responses:
        print_file(x)

    # Calculate and print indices
    print()
    calculate_users()
    for user in users.values():
        print_file(user)