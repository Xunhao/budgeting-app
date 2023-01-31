# budgeting-app

## Project Details

### Description
This project utilises OOP concept to create a simple budgeting app containing a handful of basic methods that allows users to interact with such as:
1. Check balances
2. List transactions
3. Add transaction
4. Update transaction
5. Modify transaction
6. Remove transaction

All transactions are then stored in a sqlite database for ease of retrieval and update. For prototype, I chose to use an in-memory database so that it refreshes everytime I run the script.


### Motivation
I started this project with the intent of learning and familiarising myself with Python OOP concepts. Looking at my commit history, you will notice that I have actually built quite a few methods (instance, class, and static) already. However, as I progress I found it increasingly difficult to build methods in a way that makes it easy for an imaginary user to interact with the application without a UI or Primary keys. Hence, I have decided to utilise sqlite as a way to store all transactions within a database. With a database, we can easily retrieve certain records based on the input provided by a user.

### Limitations
1. Does not contain a UI which makes it difficult for user interaction. However, this is by design since this project is meant more for learning

## Credits
1. [Corey Schafer](https://www.youtube.com/watch?v=ZDa-Z5JzLYM&list=PL-osiE80TeTsqhIuOqKhwlXsIBIdSeYtc)
  - I learned most of my OOP concepts from Corey Schafer via his Python OOP Tutorial playlist. He is an amazing teacher and his videos has helped many aspiring developers including myself. I highly recommend watching his videos to learn more about Python where possible.
