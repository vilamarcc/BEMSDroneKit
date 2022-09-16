![](https://eetac.upc.edu/ca/noticies/eetac.png)

# Mission generator for building evaluation with UAS

This project belong to the final degree project developed by Marc Vila during his Bsc. Aerospace Engineering at UPC, ....

** link report ** 

## Functions 

- _haversine.py :
- _droneCommands.py :
- _missionCalculation.py :
- _routes.py :
- _plotroutes.py :
- _facadeMission.py :
- _helixMission.py :
- _multifacadeMission.py
- _demo.py :

## Structure

```mermaid
graph LR
E[Vectors] -- x,y,z --> F[Comandos Esc]-- mission.waypoits --> G[dronekit] --> H(Route execution)

E -->I[Haversine] <--> E
F--> A[Visualization]
B[Building Data] --> E

```
## Examples

Various examples developed using BEMS library:

** include photos ** 

© UPC Universitat Politècnica de Catalunya · BarcelonaTech, 2020 ™
