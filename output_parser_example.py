"""
#Integration with Other Systems:
If the output needs to be fed into another system or application, the parser can format it accordingly. 
For example, if the output is used in a web application, the parser might convert it to HTML.

Example:
Here's a simple Python example of an output parser that formats and extracts relevant information from the LLM's output:

In this example, OutputParser class takes the raw output and performs basic formatting and extraction of relevant information based on keywords.

"""


class OutputParser:
    def __init__(self, output):
        self.output = output

    def format_output(self):
        # Basic formatting like stripping extra whitespace
        self.output = self.output.strip()
        # Other formatting tasks can be added here
        return self.output

    def extract_relevant_info(self):
        # Example: extracting sentences that contain specific keywords
        relevant_info = []
        keywords = ['important', 'note', 'remember']
        for line in self.output.split('.'):
            if any(keyword in line for keyword in keywords):
                relevant_info.append(line.strip())
        return '. '.join(relevant_info)

# Usage:
llm_output = "   This is a raw output from the LLM. It's very important to note this. Some irrelevant information here. Remember to handle special cases.  "
parser = OutputParser(llm_output)
formatted_output = parser.format_output()
relevant_info = parser.extract_relevant_info()

print("Formatted Output:", formatted_output)
print("Relevant Information:", relevant_info)
