
1. Compiling

Our project is hosted on the CS50 IDE.  As such, you should compile our program through the IDE using a new terminal window on https://ide.cs50.io/yijiang_zhao/ide50.  To do so, open a new terminal, execute cd project, then cd final.  Once in the final folder, execute flask run.  The terminal should give a link to http://ide50-yijiang-zhao.cs50.io:8080/.

2. Registering and Logging In

You will initially be directed to a page requesting you to login.  If you already have a username and password, enter the username and password.  Otherwise, click on “register” in the top navigation pane. You will be prompted to make sure to fill all files, and to choose different usernames if current usernames are taken. Make sure your password has at least one number and at least one letter; otherwise you will be given an error. In addition, for registration, if the password and password confirmation do not match, you will also receive a warning. Once you have registered and/or logged in, you will be taken to the homescreen.

3. Home Screen

Upon logging in, you are directed to your home screen which initially only shows three panes (the number of panes expands as you create sudoku puzzles -) for sample sudoku puzzles (automatically created upon registering), which you can use to access the screen to solve the puzzles by pressing the “Solve” button for each pane. Each pane shows the name of the creation, the “status” (whether complete or incomplete), and the date and timestamp the item was created.

4. Solving

If you select one puzzle by clicking the “Solve” button on the pane, you will be directed to the solve page for that puzzle. Certain boxes are bolded and cannot be edited; these are the numbers of the sudoku puzzle itself. Other boxes, however, are empty and can be filled with numbers from 1-9, whereupon being filled, the text color is gray (to help differentiate the numbers you’ve modified and those you cannot).
To save progress, press the “Save” button at the bottom of the page. It will refresh the page, but remain on the same page; to return back to the home page which lists all puzzles, press the icon on the top left corner or the “Home” button on the navigation bar.
To check your solution (you cannot check if your current answers are correct; only that the final answer is correct--you will be prompted to fill all boxes if they are not all filled), press the “Check” button at the bottom of the page. There will be an alert which tells you that your solution is correct and you’ve solved it, if it is indeed correct; else, it sends an alert telling you the solution is wrong. If correct, the “status” will change to completed and can be seen on the home screen. If you wish, you can continue changing puzzle values even after completion.
If you have reached a complete impasse, press the “Solve” button at the bottom of the page which runs the puzzle through our algorithm which solves the puzzle. However, having us find a solution will not change the “status” of the puzzle to “complete.” In addition, if there are multiple solutions, we will provide one possible solution.

5. Creating Your Own Sudoku

You will also notice another tab in the navigation bar at the top titled “Create.” The link takes you to the create page where you can create your own sudoku puzzle. There will be an empty 9x9 grid where you can enter numbers into the boxes as desired, leaving boxes without values blank.  Once you feel satisfied with your puzzle creation, give the puzzle a name in the top field and hit “Create” at the bottom (you will be prompted if there is no name).  You will be redirected to the homescreen where you should now see your puzzle among the others. To access the puzzle, press the “Solve” button at the bottom of the pane which contains the name of the puzzle you just made. The functions of the page you will be linked to are the same as (4) and you can use them to solve your own puzzle, check if your answer is correct, and if it is solvable.

6. Change Password

If you wish to change your password, you may click the “Change Password” tab at the top. Enter a new password and re-enter it to confirm your new password (you will be prompted if the fields aren’t complete or the passwords don’t match).

7. Logging Out

Hit “Log Out” in the top corner to log out!
