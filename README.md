## Inspiration
I wanted to create an app that allowed kids to be as curious as they want and to explore the world as much as possible. I was inspired by how curious my little cousins are about the world and how enthusiastic they are to learn more about it.

## What it does
The app allows the user to take a picture of their surroundings. The app then analyzes the contents of the image for certain object (horses, cats, dogs, trains, etc) that the app then pulls up information about. For example a kid could take a picture of a cat and instructions for taking care of cats would pop up.

## How I built it
The original image is taken using HTML5's ability to interact with webcams and other video peripherals. Then photo is then converted to base64 and sent to the background where I implemented tensorflow's single-shot detector to determine the contents of the photo. Then I find the relevant information on the object which gets passed back to the user.

## Challenges I ran into
Making sure that the camera is properly secured was a bit of a challenge. Also creating certain iframes to display information to the user was difficult and required a work around.

## Accomplishments that I'm proud of
I was happily surprised how successfully the image can be properly encoded and analyzed with tensorflow's model. I was expecting there to be a bigger challenge in that regard.


## What's next for Curiosity Helper
The main thing that can be fixed is the front-end design which has its flaws to say the least. I would also like to see it develop into a fully functioning mobile app.

## How to run
Install requirements in the src/ folder
Run $ python src/main.py
