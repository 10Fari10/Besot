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
- For testing purposes, solution is r1->r2->r3->r4
   
### Deployment
- App is deployed at [billsoftrails.com](https://billsoftrails.com)

## Notes
- Secret key was accidentally committed to repository  
- Secret key has since been changed and a placeholder value is in the docker compose file  
- Private key and self signed certs are placeholders 

- Django handles the prepared SQL statements to protect against sql injection  
- Django's login framework handles the storing of hashed passwords and usernames
