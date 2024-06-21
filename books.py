""" Sort books by Library of Congress call number. """


from argparse import ArgumentParser
import re
import sys

class Book:
    """
    Organizes books in a file by call number
    
    Attrubutes:
        callnum (str): the book's call number
        title (str): the book's title
        author (str): the book's author 
    """
    def __init__(self, callnum, title, author):
        self.callnum = callnum 
        self.title = title 
        self.author = author 
            
    def __lt__(self, other):
        """
        Compares self instance call number to other instance call number to
        determine which is less than the other.
        
        Args:
            self (str): instance of Book class
            other (str): other instance of Book class
            
        Return:
            Bool: Returns True if self sorts before other and 
                False if other sorts before self
        """
        self_parts = self.call_num_parse()
        other_parts = other.call_num_parse()
        
        #letter(s) at the beginning 
        if self_parts[0].replace(' ', '') != other_parts[0].replace(' ', ''):
            return self_parts[0].replace(' ', '') < other_parts[0].replace(' ', '')
     
        #number 
        if self_parts[1].replace(' ', '') != other_parts[1].replace(' ', ''):
            return self_parts[1].replace(' ', '') < other_parts[1].replace(' ', '')        
        
        #cutter
        if self_parts[2] != other_parts[2]:
            return self_parts[2] < other_parts[2]
        
        #year
        self_year = int(self_parts[3]) if self_parts[3] else None
        other_year = int(other_parts[3]) if other_parts[3] else None
        
        if self_year is not None and other_year is not None:
            return self_year < other_year
            
        elif self_year is not None and other_year is None:
            return False
        
        elif self_year is None and other_year is not None:
            return True
        else:
            return False


    def call_num_parse(self):
        """
        Parses the call numbers of books using regular expression.
        
        Return:
            returns the class, subject, cutter, and year of the call number for 
            each book 
        
        Side effects:
            prints "invalid call number" if the call number is not in appropriate 
            format
        """
        pattern = r"(?x)^(?P<class>[A-Z]+)(?P<subject>\s*\d{1,4}(?:\.\d{1,4})?\s*\.)\s*(?P<cutter>[A-Z]{1}[\d]+)\s*(?P<extracutter>[A-Z]{1}[\d]+)?\s*(?P<year>\d{4})?$"
        match = re.match(pattern, self.callnum)
        if match:
            class1 = match.group('class')
            subject = match.group('subject').strip()
            cutter = match.group('cutter').strip()
            extracutter = match.group('extracutter').strip() if match.group('extracutter') else None
            cutter = " ".join([cutter, extracutter]) if extracutter else cutter
            year = match.group('year') if match.group('year') else None

            return class1, subject, cutter, year
        else:
            print("invalid call number")
    
    def __repr__(self):
        """
        Formal representation of Book class.
        
        Args:
            self (str): instance of Book class 
        
        Return:
            Returns formal string representation of book's call number, title, and author
        """
        return f"""Book("{self.callnum}", "{self.title}", "{self.author}")"""


def read_books(filepath):
    """
    Opens file with book information and build instances of Book class
    
    Args:
        filepath (str): filepath to file with book information in UTF-8 coding
        
    Return:
        list: a list of the the instances of books
    """
    book_list = []
    with open(filepath, 'r', encoding = 'utf-8') as f:
        for line in f:
            splitting = line.strip().split('\t')
            title = splitting[0]
            author = splitting[1]
            callnum = splitting[2] 
            book_list.append(Book(callnum, title, author))
    return book_list   


def print_books(books):
    """ Print information about each book, in order. """
    for book in sorted(books):
        print(book)


def main(filename):
    """ Read book information from a file, sort the books by call number,
    and print information about each book. """
    books = read_books(filename)
    print_books(books)


def parse_args(arglist):
    """ Parse command-line arguments. """
    parser = ArgumentParser(arglist)
    parser.add_argument("filename", help="file containing book information")
    return parser.parse_args(arglist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.filename)
