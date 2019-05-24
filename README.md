### Dockerized Pizzly Pipeline for Treehouse Fusion Analysis

#### RUN
```
docker run -it -v $PWD:/data  ucsctreehouse/pizzly:0.37.3 --fusion fusion.txt -a abundance.h5
```
