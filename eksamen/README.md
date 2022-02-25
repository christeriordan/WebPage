Run application by running appDB.py in the eksamen folder, to make sure the database and tables are created. Also the inserts
from __main__ createDB_table(conn), insert_data(conn)  and conn = sqlite3.connect("Webpage.db")

Then run app.py in the eksamen folder


functionality:

On the index page, you will be notified if you are not logged in with a text saying "you are not logged in".
When you have successfully logged in, you will be notified with a text saying "Welcome" followed by the users username created by the user

You can redirect between the login page, register page and the beer page, by clicking on the icons in the upper
right corner.

register page:

While you are in the register page, you can register a user by typing in a username and a password.
If your username and password is valid, that user will be added to the database, and will be valid
to log in to the webpage.
If you try to register with a username that is already in the database, you will get an error message
If you try to register with a password less then 4 characters, you will also get an error message.

login page:
By successful login, you will get your credentials saved in a session, which will give you a role as user, that will
make you be able to add beers in the beer section
If you try to log in with a username that is not in the database, you will get an error message(I know this is very bad
method, because of safety)

beer page:
On the beer page, you can browse the beers that are in the database, you can add beers if you have logged in,
if you are not logged in, you will not be permitted to add beers to the database.

The select box contains the Brewery table, where you can select which brewery your beer belongs to. (intention is to be able to choose freely which brewery you want to add)

You can also filter the beer table, by inputting text in the filter content input field and by pressing the search
button

If you press the settings button, you can change the appearance of the beer table. You can change the color and font-size.

You can change the name,style and breweryID of beers in the table, by pressing the edit button, on the beer you want to
edit. (you should only be able to edit beers you yourself added, but I did not have time to make that work, same goes for
the delete beer button)

You can delete beers by pressing the delete button.

logout:
when logged in, you can press the logout button up in the right corner, to get logged out, and remove your session.




