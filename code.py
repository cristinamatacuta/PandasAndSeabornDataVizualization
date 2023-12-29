# importing the necessary libraries
import pandas as pd
import seaborn as sb
from matplotlib import pyplot as plt
import seaborn as sns
import re
import sys


def read_book(file_path):
    """Read the content of a text file.

    Args:
        file_path (str): The path to the text file.

    Returns:
        str: The content of the text file.

    Raises:
        FileNotFoundError: If the file is not found.
    """
    try:
        with open(file_path, "r") as text_file:
            return text_file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        sys.exit(1)





def read_stop_words():
    """
    Reads stop words from the file and removes trailing spaces

    Returns:
        list: A list of stop words.
    """
    with open("stopwordlist.txt", "r") as filename3:
        # Save the stop words into a variable
        # Remove trailing spaces
        my_file3 = [line.strip() for line in filename3.readlines()]
        # Return the stop words
        return my_file3


def get_sentences(text):
    """
    Split the text into sentences using regular expressions

    Args:
        text(str): The text to be split into sentences.

    Returns:
        list: A list of sentences
    """
    # Split the text using regex and save in a variable
    sentences = re.split(r"[.?!]", text)
    # Return the list of sentences
    return sentences


def get_words(text):
    """
    Split the text into words using regular expressions

    Args:
       text(str): The text to be split into sentences.

    Returns:
       list: A list of words
    """
    # Reused function to get the sentences
    sentences = get_sentences(text)
    # Initialize an empty list to save the words
    words = []
    # For loop that iterates through each
    # sentence from the sentence list
    for sentence in sentences:
        # List of words containing all the strings
        # that match the pattern
        sentence_words = re.findall(r"\b\w+(?:[-]\w+)*\b", sentence)
        # Add the list to the ealier initialize list
        words.extend(sentence_words)
        # Return the list of words
    return words


def stop_words_removed(text):
    """
    Removes stop words from a list of words and returns a list of clean words

    Args:
       text(str):The text to be cleaned.

    Returns:
       list: A list of clean words

    """
    # Saved the words into a variable
    words = get_words(text)
    # Saved the stop words that were read earlier
    stop_words = read_stop_words()
    # List comprehension. For each word from list of words
    # If word.lower not in stop word,
    # add the word to the list of clean words

    clean_words = [word for word in words if word.lower() not in stop_words]
    # Return a list of word that contain no stop words
    return clean_words


def ten_most_used_words(text):
    """
    Finds the ten most used words in a text, along with their frequency

    Args:
       text(str):The text from where the words are extracted

    Returns:
       dict: A dictionary with the ten most frequent words and their frequency, sorted by value

    """
    # Saved the clean words in a variable
    words = stop_words_removed(text)
    # Initialize a dictionary to store word frequencies
    word_frequency = {}
    # Iterating through each word from the list of words
    for word in words:
        word_lower = word.lower()  # Convert word to lowercase
        # Check if the word is in the dictionary
        if word_lower in word_frequency:
            # If yes, increment its value by one
            word_frequency[word_lower] += 1
        else:
            # Else, add the key to the dictionary
            word_frequency[word_lower] = 1
    # Sort the dictionary by value
    word_frequency_order = sorted(
        word_frequency.items(), key=lambda x: x[1], reverse=True
    )
    # Get the top 10 by taking the first
    # 10 elements of the sorted dictionary
    top_ten_words = dict(word_frequency_order[:10])
    # Return the 10 top words
    return top_ten_words


def complete_data_top_10_words(text, chapter_number):
    """
    Collects the rest of the data needed for the CSV as per assginmenet desctiption, lenght, and chapter from where they come

    Args:
       text (str): The text to analyze.
       chapter_number (int): The chapter number to which the text belongs.

    Returns:
        list of dict: A list of dictionaries, each containing word, frequency, length, and chapter number.
    """
    # Called the function to get the top 10 words
    # Saved the words into a dictionary
    top_10_word = ten_most_used_words(text)
    # Initialized an empty list
    word_lst = []

    # Loop that iterates through each tuple pair
    # and creates a new dictionry for each key value pair
    # containing additional information
    for key, value in top_10_word.items():
        new_dict = {
            "Word": key,
            "Frequency": value,
            "Length": len(key),
            "Chapter": chapter_number,
        }
        # Add each dictionary to the empty list
        word_lst.append(new_dict)
        # Return the list of dictionaries
    return word_lst


def write_data_cvs(text, chapter_number):
    """
    Create a CSV file containing top 10 words in each file, together with their frequency, lenght and the number of the chapter their are coming from

    Args:
       text (str): The text to analyze.
        chapter_number (int): The chapter number to which the text belongs.

    Returns:
    str: The path to the CSV file.

    """

    # Save the top 10 words together with
    # all the data in a variable
    word_dict = complete_data_top_10_words(text, chapter_number)

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(word_dict)
    # Declare the file path  that will be used for the CSV
    # Use chapter_number in the file name
    file_name = f"chapter{chapter_number}_data.csv"
    # Convert the DataFrame to a CSV
    df.to_csv(file_name, index=False)
    # Return the path to the CSV file
    return file_name


# for better modularity, function to read the csv file
def read_csv(data_csv):
    """
    Reads a CSV file and returns its data as a DataFrame.

    Args:
        data_csv (str): The filename of the CSV file to read.

    Returns:
        pd.DataFrame: The data read from the CSV file.
    """
    # Read CSV file in a DataFrame
    df = pd.read_csv(data_csv)
    # Return the DataFrame
    return df


def vizualization_seaborn_barchart(data1_cvs, data2_csv):
    """
    Creates and displays a bar chart using Seaborn for the top 10 words' frequency in two chapters.

    Args:
        data1_cvs (str): The filename of the CSV file containing data for the first chapter.
        data2_csv (str): The filename of the CSV file containing data for the second chapter.
    """
    # Read the data from the first chapter
    df1 = read_csv(data1_cvs)
    # Read the data from the second chapter
    df2 = read_csv(data2_csv)

    # Combine the data from both chapters using concatenation
    df_combined = pd.concat([df1, df2], ignore_index=True)

    # Define a color palette for the bars
    custom_palette = ["blue", "red"]

    # Sort the bars based on frequency in descending order
    df_combined = df_combined.sort_values(by="Frequency", ascending=False)

    # Plot the figure with Seaborn
    figure = sns.barplot(
        data=df_combined, x="Word", y="Frequency", hue="Chapter", palette=custom_palette
    )

    # Rotate the labels for better visibility
    figure.set_xticklabels(figure.get_xticklabels(), rotation=90)

    # Set y-axis ticks from 10 to 10
    plt.yticks(range(0, max(df_combined["Frequency"]) + 1, 10))

    # Label the X and Y Axis
    plt.xlabel("Word")
    plt.ylabel("Frequency")
    # Set a title for the figure
    plt.title("Top 10 Words Frequency in Chapters 1 and 2")

    # Adjust the layout
    plt.tight_layout()
    # Save the figure in a png format
    # Increse the Quality of the Image
    plt.savefig("bar.png", dpi=300)
    # Show the figure
    plt.show()


def vizualization_seaborn_bubblechart(data1_csv, data2_csv):
    """
    Creates and displays a bubble chart using Seaborn for the top 10 words' frequency in two chapters.

    Args:
        data1_csv (str): The filename of the CSV file containing data for the first chapter.
        data2_csv (str): The filename of the CSV file containing data for the second chapter.
    """
    # Read the data from the first chapter
    df1 = read_csv(data1_csv)
    # Read the data from the second chapter
    df2 = read_csv(data2_csv)

    # Combine the data from both chapters using concatenation
    df_combined = pd.concat([df1, df2], ignore_index=True)

    # Define a color palette for the bubble chart
    custom_palette = ["blue", "red"]

    # Create the bubble chart with Seaborn
    figure = sns.scatterplot(
        data=df_combined,
        x="Word",
        y="Frequency",
        hue="Chapter",
        palette=custom_palette,
        size="Length",
        sizes=(20, 200),
    )

    # Rotate the labels for better visibility
    figure.set_xticklabels(figure.get_xticklabels(), rotation=90)

    # Set y-axis ticks from 10 to 10
    plt.yticks(range(0, max(df_combined["Frequency"]) + 1, 10))

    # Add labels to X and Y Axis
    plt.xlabel("Word")
    plt.ylabel("Frequency")
    # Add a title
    plt.title("Top 10 Word Frequency - Second Visualization")
    # Adjust the layout
    plt.tight_layout()

    # Save the image as a png
    # Increse the quality of the image
    plt.savefig("bubble.png", dpi=300)

    # Show the plot
    plt.show()


def main():
    # Check if the correct number of command line arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python text_analysis.py <path_to_chapter1_file> <path_to_chapter2_file>")
        sys.exit(1)

    # Read the content of the first chapter
    chapter1 = read_book(sys.argv[1])
    # Read the content of the second chapter
    chapter2 = read_book(sys.argv[2])

    # Define chapter numbers
    chapter_1 = 1
    chapter_2 = 2

    # Write a CSV file containing the top 10 words for the first chapter
    data_chapter1 = write_data_cvs(chapter1, chapter_1)

    # Write a CSV file containing the top 10 words for the second chapter
    data_chapter2 = write_data_cvs(chapter2, chapter_2)

    # Visualize the top 10 words using a bar chart
    vizualization_seaborn_barchart(data_chapter1, data_chapter2)

    # Visualize the top 10 words using a bubble chart
    vizualization_seaborn_bubblechart(data_chapter1, data_chapter2)


if __name__ == "__main__":
    main()




