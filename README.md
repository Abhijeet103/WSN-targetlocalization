# WSN-targetlocalization

## Context 
when you don't have GPS or in places where its signal is weak and can't be relied on we can use wireless sensory networks in order to locate a target using a mobile node and 
a lot of anchor or stationary nodes as these sensors do not have a lot of range the signals generally hop from one node to another in order to reach destination. The location of the mobile node is predicted using the anchor node informations by localization algorithms 
## Algorithms 
Algorithms used are 
1) Weighted Centroid Localization algorithm
2) MDS
## Modelling 
1) each  node is concidered as a vertex in a graph
2) sortest path from one node to another node is calculated using dijktra algorithm
3) as mobile nodes keep changin so is the  sortest path making it a dynamic graph  on top of which localization algorithm work
 
![Screenshot 2023-11-04 151836](https://github.com/Abhijeet103/WSN-targetlocalization/assets/93581505/2fe16f4a-0ad6-4bc5-b67f-95ea1169570e)
![Screenshot 2023-11-04 151749](https://github.com/Abhijeet103/WSN-targetlocalization/assets/93581505/2357a326-b84a-4db2-b8f2-df6ed2d1933b)


RMSE: 0.03503814772508335
