import re
from typing import Tuple

## -- Task 3 -- ##

month_names = [
    "[Jj]an(?:uary)?", 
    "[Ff]eb(?:ruary)?", 
    "[Mm]ar(?:ch)", 
    "[Aa]pr(?:il)", 
    "[Mm]ay", 
    "[Jj]une",
    "[Jj]uly",
    "[Aa]ug(?:ust)", 
    "[Ss]ep(?:tember)", 
    "[Oo]ct(?:ober)", 
    "[Nn]ov(?:ember)", 
    "[Dd]ec(?:ember)", 
]

def get_date_patterns() -> Tuple[str, str, str]:
    """Returns strings containing regex pattern for year, month, day.
  
    Returns:
        year, month, day (tuple): 
            Containing regular expression patterns for each field
    """

    # 1 followed by 3 digits (0-9) at beginning or 20 followed by digits between (0-2) followed by any digit (0-9) at the end
    year = r"(?:\b1\d{3}|20[0-2]\d\b)"
    # Regular expression for fidning month on form 0[1-9] at beginning or 1[0-2] or month-string at end
    month = rf"(?:\b0\d|1[0-2]|%s\b)" % '|'.join(month_names)
    # 3 followed by digit (0-1) at start or digit (1-2) followed by any digit (0-9) or zero or one occurence of 0 followed by any digit (0-9) at end
    day = r"(?:\b3[01]|[12]\d|0?\d\b)"

    return year, month, day


def convert_month(s: str) -> str:
    """Converts a string month to number (e.g. 'September' -> '09').

    Args:
        month_name (str): 
            month name
    Returns:
        month_number (str): 
            month number as zero-padded string
    """

    if s.isdigit():
        return s

    for i in range(len(month_names)):
        
        if re.search(month_names[i], s):
            month = str(i + 1)

            return zero_pad(month) if len(month) == 1 else month

def zero_pad(n: str) -> str:
    """zero-pad a number string if n is less than 10. 
    E.g. turns '2' into '02'.

    Args:
        n(str): 
            month or day without zeropad
    Returns:
        (str): 
            zeropadded month or day
    """
   
    return "0" + n if len(f"{n}") == 1 else n

def find_dates(text: str, output: str = None) -> list:
    """Finds all dates in a text using reg ex.

    Args:
        text (string): 
            A string containing html text from a website
    Return:
        results (list): 
            A list with all the dates found
    """

    year, month, day = get_date_patterns()

    # Date on format YYYY/MM/DD - ISO
    ISO = rf"{year}\-{month}\-{day}"

    # Date on format DD/MM/YYYY
    DMY = rf"{day}\s{month}\s{year}"

    # Date on format MM/DD/YYYY
    MDY = rf"{month}\s{day},\s{year}"

    # Date on format YYYY/MM/DD
    YMD = rf"{year}\s{month}\s{day}"

    formats = [ISO, DMY, MDY, YMD]
    dates = []

    for format in formats:
        dates_ = re.findall(rf'{format}', text)

        for date in dates_:
            reformatted_date = date
       
            # Based on current format, change into the correct output format
            if format == ISO:
                reformatted_date = re.sub("-", "/", date)
            elif format == DMY:
                reformatted_date = re.sub(rf"({day}) ({month}) ({year})", r"\3/\2/\1", date)
            elif format == MDY:
                reformatted_date = re.sub(rf"({month}) ({day}), ({year})", r"\3/\1/\2", date)
            elif format == YMD:
                reformatted_date = re.sub(rf"({year}) ({month}) ({day})", r"\1/\2/\3", date)
      
            year_, month_, day_ = reformatted_date.split("/")
            month_ = convert_month(month_)
            month_ = zero_pad(month_)
            day_ = zero_pad(day_)

            reformatted_date = "/".join([year_, month_, day_])
            dates.append(reformatted_date)

    if output:
        print(f"Writing to: {output}")
        
        with open(output, 'w') as out:
            out.write(dates)

    return dates
