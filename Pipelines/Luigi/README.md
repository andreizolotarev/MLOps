# TASK 4: LUIGI

To run with local scheduler:


<span style="background-color: #FFFF00">python preprocessing.py FullPipeline --local-scheduler</span>

Central scheduler with parallelization (I changed default port in luigi.cfg):

<span style="background-color: #FFFF00">luigid --port 12345</span> or 
<span style="background-color: #FFFF00">luigid --background --logdir tmp --port 12345</span>

<span style="background-color: #FFFF00">python preprocessing.py FullPipeline --workers 20</span>

<p style="text-align:center;">Pipeline(localhost:12345):</p>

<img src="img/Pipeline.png"
     alt="Markdown Monster icon"
     style="float: left; margin-right: 10px;" />
