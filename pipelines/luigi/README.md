# LUIGI
## In this example a docker container will be built for using Luigi as an orchestrator
## CLI

1) Build an image with human readable name:  
```
docker build -t luigi_image --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .
```
2) Run a container (Start Luigi's visualizer at port 1111):  
```
docker run -d -v $(pwd)/volume:/home/new_user/volume -p 1111:1111 --name luigi_container luigi_image
```
At this point, you should be able to visit Luigi's visualizer at 0.0.0.0:1111

I've developed a pipeline.py which downloads {TICKER} for each date since {START_DATE} using #{WORKERS} of your machine.

If you want to start the pipeline, firstly, enter the running container in -it mode:
```
docker exec -it luigi_container bash
```
And then type:
```
cd volume && python pipeline.py --workers 14 --ticker_name AAPL --start_date 2020-10-10
```
In this case an AAPL (Apple) ticker data will be download for each date since 2020-10-10 and plots with previous 7days values will be created. 

Once you've done it, files are being collected at /volume/data/{DATE} and you can see Luigi's pipeline visualization at 0.0.0.0:1111 like:

<p style="text-align:center;">Go to 0.0.0.0:1111, select Pipeline (1) and click on the icon (2):</p>
<img src="img/visualizer.png"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />

<p style="text-align:center;"> Pipeline visualization</p>
<img src="img/pipeline.png"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />
     
Don't forget to stop|kill the container, once you've finished Luigi's investigation)
