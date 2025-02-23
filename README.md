# Polar - The Short-Form Content App That Fights Polarization
## Inspiration
In today's digital landscape, social media platforms amplify political polarization by reinforcing echo chambers. Their recommendation systems often prioritize engagement over balanced perspectives, leading users deeper into their existing political beliefs. We wanted to build Polar, an app that combats this by actively introducing diverse viewpoints into short-form content consumption.

## What it does
Polar is a short-form content app (similar to TikTok) designed specifically for political discourse. The platform empowers users to explore multiple perspectives on political topics without getting trapped in a single ideological bubble.

## Key Features:

Poles (Political Shorts): Users upload Poles, short videos discussing political topics.
Balanced Recommendation System: The algorithm detects content bias in a user’s watch history and adjusts recommendations to ensure exposure to diverse viewpoints.
Swipe for Opposition: Swiping right on a Pole reveals another Pole on the same topic but with an opposing viewpoint, helping users understand different perspectives.
Learn More: Each Pole comes with a Learn More button that:
Identifies the topic being discussed.
Provides an unbiased description of the issue.
Explains why the topic is politically contentious, giving users context to form their own opinions.
## How we built it
We developed Polar as a web app using:

Frontend: React.js & Tailwind CSS for an intuitive UI.
Backend: Flask & FastAPI for handling content recommendations and user interactions.
Database: PostgreSQL for storing user preferences and video metadata.
Machine Learning: A custom-built recommendation model using scikit-learn and TensorFlow, balancing content exposure across political perspectives.
NLP Analysis: We used spaCy and BERT to analyze video transcripts, categorize topics, and detect political sentiment to provide relevant counterpoints.
## Challenges we ran into
Building a Fair Recommendation System: Typical recommendation algorithms reinforce user biases; balancing this while keeping engagement high was a key challenge.
Opposing Viewpoint Matching: Ensuring accurate and contextually relevant counterarguments required deep NLP processing.
Content Moderation: Preventing misinformation while promoting free speech was a delicate balance.
## Accomplishments that we’re proud of
Successfully implemented a bias-aware recommendation algorithm that adapts based on user consumption patterns.
Built an opposing viewpoint matching system that pairs videos intelligently.
Designed an intuitive UI that encourages open political discussions rather than arguments.
## What’s next for Polar?
Expand to mobile: Building a native app for iOS and Android.
Fact-checking integration: Partnering with fact-checking organizations to flag misinformation.
Community features: Adding user discussions and fact-based debates.
More granular political categories: Refining content tagging to offer a nuanced exploration of political issues.
## Try it out!
🔗 [Insert demo link or GitHub repo]

