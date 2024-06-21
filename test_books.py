""" Test call number script. """

# in the following import statement, replace books with the name of your
# script, minus the .py extension

from regex_books.books import Book, read_books
import pytest

def test_book_init():
    """ Test whether __init__() method works as expected """
    # create an instance of the Book class
    callnum = "A1 .B2 2020"
    title = "Boring book"
    author = "Joe Author"
    b = Book(callnum, title, author)
    
    # check for expected attributes
    for attr, val in [("callnum", callnum), ("title", title),
                      ("author", author)]:
        assert hasattr(b, attr), \
            f"instance of Book class has no {repr(attr)} attribute"
        assert getattr(b, attr) == val, \
            f"unexpected value for {repr(attr)} attribute"


def test_book_lt():
    """ Test whether __lt__() method works as expected """
    b1 = Book("C42.B17 D4 1950", "Book 1", "")
    b2 = Book("D30.B17 D4 1950", "Book 2", "")
    b3 = Book("DA4.B17 D4 1950", "Book 3", "")
    b4 = Book("D290.B17 D4 1950", "Book 4", "")
    b5 = Book("D290.C83 D4 1950", "Book 5", "") #this one    D290.C83 D4 1950
    b6 = Book("D290.5.C83 D4 1950", "Book 6", "")
    b7 = Book("D290.49.C83 D4 1950", "Book 7", "")
    b8 = Book("D290.C824 D4 1950", "Book 8", "")
    b9 = Book("D290.C83 E4 1950", "Book 9", "")
    b10 = Book("D290.C83 D32 1950", "Book 10", "")
    b11 = Book("D290.C83 1950", "Book 11", "") #this one    D290 .C83 1950
    b12 = Book("D290 .C83 D4", "Book 12", "")
    b13 = Book("D290 .C83 D4 1972", "Book 13", "")
    b14 = Book("DAW290 .C83 D4 1972", "Book 13", "")
    
    assert hasattr(b1, "callnum"), \
        ("this test assumes Book objects have a 'callnum' attribute,"
         " but yours doesn't")
    
    def pos_feedback(a, b):
        return f"{a.callnum} should be considered less than {b.callnum}"
 
    def neg_feedback(c, d):
        return f"{c.callnum} should not be considered less than {d.callnum}"
    
    for x, y in [(b1, b2), (b2, b3), (b4, b3), (b4, b5), (b5, b6), (b7, b6),
                 (b8, b5), (b8, b9), (b10, b5), (b11, b5), (b12, b5),
                 (b5, b13), (b2, b14), (b3, b14)]:
        assert x < y, pos_feedback(x, y)
        assert not (y < x), neg_feedback(y, x)


def test_book_repr():
    """ Test whether __repr__() method works as expected
    
    __repr__() should return a string that can be evaluated as a Python
    statement. That statement should create a Book() object identical to
    the one whose __repr__() method produced the statement.
    """
    b1 = ("A1.B1 2020", "Test", "Georgina Rutherford")
    b2 = ("D2.C1 2020", "Maryland's 61st Governor", "Martin O'Malley")
    b3 = ("F3.D1 2020", r"""History of a computer's C:\Drive""", "")
    for callnum, title, author in [b1, b2, b3]:
        b = Book(callnum, title, author)
        r = repr(b)
        assert r.startswith("Book"), \
            (f"__repr__() should return a string that, if evaluated as"
             f" a Python statement, would produce a Book object"
             f" identical to the object whose __repr__() method was"
             f" called")
        try:
            bb = eval(r)
        except Exception as e:
            raise RuntimeError(f"received {type(e).__name__} when trying"
                               " to evaluate result of __repr__() as a"
                               " Python statement for a Book object with"
                               " the following attributes:\n"
                               f"  author: {b.author}\n"
                               f"  title: {b.title}\n"
                               f"  callnum: {b.callnum}\n"
                               f"  result of __repr__(): {r}")
        for attr, value in [("callnum", callnum), ("author", author),
                            ("title", title)]:
            actual = getattr(bb, attr)
            assert actual == value, \
                (f"result of __repr__() contains unexpected value for"
                 f" {attr} attribute: expected {repr(value)} but"
                 f" received {repr(actual)}")


def test_read_books(tmp_path):
    """ Test whether read_books() works as expected """
    book_info = ("Crankshaft compendium\tJohn Rodgers\tJK102 .R82 1995\n"
                 "Indelible ink : a history\t\tDV815 .T21 2014")
    tmp_file = tmp_path / "books.tsv"
    tmp_file.write_text(book_info, encoding="utf-8")
    try:
        books = read_books(str(tmp_file))
        assert isinstance(books, list), "read_books() should return a list"
        assert isinstance(books[0], Book), \
            "read_books() should return a list of Book objects"
        assert books[0].title == "Crankshaft compendium", \
            "unexpected title of first book returned by read_books()"
        assert books[0].author == "John Rodgers", \
            "unexpected author of first book returned by read_books()"
        assert books[0].callnum == "JK102 .R82 1995", \
            "unexpected call number of first book returned by read_books()"
        assert books[1].title == "Indelible ink : a history", \
            "unexpected title of second book returned by read_books()"
        assert books[1].author == "", \
            "unexpected author of second book returned by read_books()"
        assert books[1].callnum == "DV815 .T21 2014", \
            "unexpected call number of second book returned by read_books()"
    finally:
        tmp_file.unlink()
