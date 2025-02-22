import openai

# Function to analyze text bias
def analyze_bias(text, bias_level):
    """
    Analyze the text and determine why it is biased.

    Parameters:
    text (str): The chunk of text to analyze.
    bias_level (dict): A dictionary with keys 'Left', 'Middle', 'Right' and values between 0 and 1.

    Returns:
    str: Explanation of why the text is biased.
    """
    # Prepare the prompt for ChatGPT
    prompt = f"Analyze the following text and explain why it is biased:\n\n{text}\n\nBias levels:\nLeft: {bias_level['Left']}\nMiddle: {bias_level['Middle']}\nRight: {bias_level['Right']}\n\nExplanation:"

    # Call the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )

    # Extract the explanation from the response
    explanation = response.choices[0].text.strip()
    return explanation