# Besot Project

## Objectives
### Media uploads
- Users can attach png and jpeg files to their posts 
### Websockets
- Websockets implemented in game page, reached by clicking game link at the main page
  after signing in and choosing lobby alpha
- Game is a race to figure out the correct route by clicking on pins, reading the clue, and determining the next pin in the route
  given the clue
- Once user gets the correct solution, every player in the room is notified live and the leaderboard is updated
- User with the shortest time is at the top of the leaderboard
- For testing purposes, solution is r1->r2->r3->r4->r5->r6->r7->r8
### Timing
- The time the users takes to complete the game is tracked
- The user is shown the top times and live times of other users
   
### Deployment
- App is deployed at [billsoftrails.com](https://billsoftrails.com)

### Bonus Feature
- The user has the ability to add event pins
- This will ask the user for their location and drop a colored pin at their exact location that will expire at a time of their choice
- The pin will delete itself after that time if no other reviews are on it
- If there are, it will revert to the regular color

## Testing Procedure
1. Go the deployed website and register an account
2. Click on a point on the map and type a review
3. Click the event pin button and accept the pop up giving location access
4. Wait for the time slider to pop up
5. Choose a short duration (1 minute)
6. Verify that a pink pin has been added on your current location
7. After the expiration time has passed, verify that the pin is deleted as well as the post
8. Repeat steps 2 to 6 but click on the pin and add a regular review
9. After the expiration time has passed, verify that the pin is back to blue and that the original post has been
    deleted but not the added one

## Notes
- Secret key was accidentally committed to repository  
- Secret key has since been changed and a placeholder value is in the docker compose file  
- Private key and self signed certs are placeholders 

- Django handles the prepared SQL statements to protect against sql injection  
- Django's login framework handles the storing of hashed passwords and usernames
