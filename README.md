# PersonalLibrary
A SQL-based book database!

![image](https://user-images.githubusercontent.com/31540553/162500069-a0a6f308-6056-4cb5-a2c0-65c95801bccc.png)

This is a project that uses **Flask** and **SQLAlchemy** to build a persistent list of data and reproduce it in a web-based application. 

It is a great exercise to practice every CRUD operation:

**1 - Create:** Adding Books\
**2 - Read:** Reading Book Entries\
**3 - Update:** Updating Book Ratings\
**4 - Delete:** Deleting Book Entries\

## Creating and Reading Books
![Create](https://user-images.githubusercontent.com/31540553/162501575-8789eefe-c9a0-4e4b-bbfe-729e49150458.gif)

## Updating Book Ratings
![Update](https://user-images.githubusercontent.com/31540553/162501612-abb927d5-7e94-4414-9d22-ba51536fb172.gif)

## Deleting Books
![Delete](https://user-images.githubusercontent.com/31540553/162501631-40ba20d2-b1e8-4bca-88d5-989eba6f492c.gif)


## Challenges
An interesting challenge happened while building the CRUD operations. 
The entries manipulation have to be based on the ID instead of a list order inside the code. Otherwise wrong books will be accessed and modified.
For instance, the first element of a list is always 0, but I can delete the first elements of a Database and the "new first" will have a different ID, which can lead to errors.

## Conclusion
This was a very fun exercise where I learned very important concepts about data operations, databases, flask rendering and even css formatting.

## Important
If you have any doubts, please visit the code as it is very well documented. Feel free to contact me, it will be a pleasure to talk and learn with you!
