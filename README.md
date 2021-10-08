# Epidemic Simulation

The entire world is going through a pandemic right now. This got me thinking about how a particular infection comes to an end and what are the different variables which affect the infection.

## Colour Code:
- **Blue: Susceptible Individuals**
- **Red: Currently Infected Individuals**
- **Grey: Removed Individuals (Deceased or Recovered)**

## Overview:
- We spawn random individuals and assign random 2D vectors which sets them to wander about in a random path.
- We set the probability infection to 5% and the radius of infection as 12 units.
- The simulation goes as follows:

Here is a representation of how the simulation works:
<p align="center">
  <img src="epidemicS.gif" alt="animated" />
</p>

## Implementing quarantine
- Now let us see the difference if we implement quarantine. 
- Here, 1 second = 1 day. We will quarantine infected individuals after a day into a separate location.
- We can clearly see that good quarantine practices can completely hault an epidemic.
- The simulation goes as follows:

Here is a representation of how the simulation works:
<p align="center">
  <img src="quarantine.gif" alt="animated" />
</p>
