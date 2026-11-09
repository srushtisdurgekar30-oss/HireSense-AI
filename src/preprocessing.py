
import re
import html


def clean_resume(text):
    """
    Clean resume text while preserving important
    technical terms and programming languages.
    """

    if not isinstance(text, str):
        return ""

    # Decode HTML entities
    text = html.unescape(text)

    # Convert to lowercase
    text = text.lower()

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # Remove email addresses
    text = re.sub(
        r"\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b",
        " ",
        text
    )

    # Preserve useful technical symbols:
    # C++, C#, .NET, Node.js, CI/CD
    text = re.sub(r"[^a-z0-9+#./\s-]", " ", text)

    # Remove repeated whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


if __name__ == "__main__":

    sample = """
    Experienced Python Developer with C++, C#,
    Machine Learning, SQL and Node.js skills.
    Email: test@example.com
    Website: https://example.com
    """

    cleaned = clean_resume(sample)

    print("ORIGINAL TEXT:")
    print(sample)

    print("\nCLEANED TEXT:")
    print(cleaned)

