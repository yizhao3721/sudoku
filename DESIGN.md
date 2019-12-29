1. Solve.py

Solve.py encodes our algorithm for solving partially (or fully!) unsolved sudoku grids.  There are a few functions to
consider here.  First, take a look at solveDoku(), which receives a grid as an input and eventually spits out True (if a
solution exists) or False (if no solution exists).  If a solution does indeed exist, we return the solved grid as well.
The grid is passed in as a 9x9 list of lists in Python.  solveDoku() first calls the helper function validate_input(),
which returns whether True or False based on whether the initial input is valid.  For example, if two 1s exist in a row,
validate_input(grid) will return False, which prevents our program from trying to go through the entire backtracking
algorithm even if the input is obviously wrong.  solveDoku() then calls the next_blank_cell(grid) helper function, which
returns the row and column of the next blank cell.  If no blank cells exist, then the puzzle is already solved, and we
return (-1,-1) for (row, col).  Otherwise, we get the row and cell as a tuple (row, cell).

The next part of our algorithm is the backtracking algorithm.  In pseudocode, roughly, the backtracking algorithm works as follows:
    If 1 is a valid input:
        Find next blank cell, try numbers from 1 to 9 in that cell (i.e. call solveDoku() again)
        Keep trying numbers in next blank cell until all cells have been solved
        If a certain box can take no valid inputs:
        Backtrack to last spot where not all inputs were tried and try a different input
    Else:
    Try 2 as a valid input
        Same algorithm as under (1)
    If all values have been tried in a box and none work as a solution:
        Return false
	Note that validate_input() is also called from application.py when the user wishes to “check” his or her solution.

2. Database (puzzles.db)

We first chose to use a database so that multiple people could enjoy our sudoku website and sudoku-solving services
without impacting the experience and sudoku puzzles of others. To do so, we maintained multiple databases with linked
IDs, with users having unique IDs and puzzle_id’s that belonged to them. This allowed all the information to be stored
in one place (so it is easier to access), but to also allow it to keep different users separate from one another.
    [Table] collection
        This stores a list of all the puzzles created, beginning with the first three sample ones (easy, medium, hard).
        It stores the puzzle_id, puzzle_name, the user_id of the user who the puzzle belongs too, as well as the date
        and time it was created.
        We chose to use a database to keep track of the various puzzles and key information about them that would not be
        convenient to store outside. In addition, it makes it easier to access the information about each puzzle with
        regards to the puzzle or user ID.

    [Table] grid
        SQL databases are meant to hold one value in each entry (not store an entire list as an entry). I also did some
        research and from what I saw, the general consensus online said it wasn’t really possible. As a result, each
        value had to be stored separately. While I could store them in the stack or heap memory, it would be harder to find
        and edit specific puzzles as needed (which is definitely the case).
        The grid stores, for each value, the of the row and col of the cell in the grid, the value stored in the cell (1:9),
        a Boolean “orig” which notes whether the value is part of the problem or a user-inputted solution, and the puzzle_id.
        This allows us to easily access any specific cell and edit the value as needed (i.e. saving their progress towards
        the puzzle), which would have been much harder to do and keep track of if it was not in a database. In addition, it
        also allows us to easily know vital information (i.e. whether it was an original value or user-inputted value) for
        displaying.

    [Table] users
        This table keeps track of the user_id (which is used to differentiate all users from each other), as well as
        login information (like the password hash and username) and the current puzzle_id of the puzzle they’re working
        on. We added the final field of currPID (current puzzle_id) to allow easier access to what puzzle is being worked on.
        While for our cases we did not use it very often, it is very useful should we have other more complex methods which
        cannot be directly linked through.

3. Application.py
    We had a few main pages for the sudoku (beyond the login, register, etc.): “/” which was generally associated with
        “index.html,” “/create,” “/solve,” and “solved.” We implemented it in this way as it’s easier to work on things
        in divided parts. In addition, each route can only take either a “GET” or “POST” method, which means that in some
        cases, it was easier to just link to another page which could carry many of the other work. In addition, it also
        meant there were no super long lines of code for any individual route.

    For the routes specifically, we felt it was a good idea to have a linking page to access each sudoku puzzle, and then
        a generic page which displayed the chosen puzzle (which brought about “/” or “index.html” and “/solve”). For solve,
        because it had three routes it could go towards (“Save,” “Check,” and “Solve”), we wanted to use as many of the
        elements we’d made already. We decided to somewhat combine “Save” and “Check” as both uploaded the values onto the
        database, with “check” only having a couple extra actions. In addition, because both of those routes seemed like it
        could remain stationary on the page, we had both reroute to “solve.html” (the same html page as it was originally)
        with a few variable differences. In this way, people could keep checking or keep saving as needed, and it also meant
        less unnecessary routing from here and there.

    For “Solve,” however, we felt it was best to move that to a different route as it needed to do more calculations and
        the structure was fundamentally different (especially in how we wanted it to appear) from “solve.html.” We instead
        redirected it to “/solved” with template “solved.html,” where we then processed the results and whether the puzzle
        had a solution (in which case we displayed the solution) or not (whereupon we redirected it back to “/solve” with
        an error message).

    For “Create,” that was just an extra feature we had to allow people to create their own sudoku puzzles (or upload ones
        they found in paper/ in person).

    Note: one additional feature we had that was interesting was the copying of the three sample puzzles into the user’s
    puzzles when they were registering.
        First, we felt like this would be a useful tool to have.
        In order to accomplish this, we just accessed the puzzles under “user_id=0” (as the sample ones are under that),
            and proceeded to select all those values from the grid and reinsert except under different ID’s. This way,
            the user could begin with a few sample puzzles to understand more about how it worked.

    In some cases, we did a lot of checking on javascript to check fields were filled or matched, as it looks nicer.
        Though even in those cases, we still had server-side checking in case of disabled javascript.

    In addition, we also brought in the Masonry library as it allowed for dynamic shifting and placement of items
        (such as Bootstrap cards), which is useful as we didn’t know how many puzzles a person would make, and having
        a dynamic grid would allow us to maintain a good-looking design, regardless of the number of puzzles.

