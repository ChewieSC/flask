<h2>Mitochondria Analysis</h2>
<h4>Creating a basic front end in the python micro-framework Flask</h4><br />
This project currently implements a website to process fastq-files whose species is unknown. 
After the processing the three most likely canditates are presented, giving you a graph and a percentage output to review the species determination yourself.
<br />
The following Python libraries/modules need to be installed first:
<ul>
  <li>flask (including werkzeug  & jinja 2)</li>
  <ul>
    <li>found here: https://pypi.python.org/pypi/Flask</li>
    <li>installation guide here: http://flask.pocoo.org/docs/installation/</li>
  </ul>
  <li>Bio (http://biopython.org/wiki/Download)</li>
  <li>Matplotlib (http://matplotlib.org/downloads.html)</li>
  <li>NumPy (http://sourceforge.net/projects/numpy/files/)</li>
</ul>

If it is necessary for your project, you can then change the specific paths for the computations/reference files in the 'speciesd.cfg'.

=====
Startup:
In the console, type in: <code>python server.py</code>
(it might be necessary to execute the statement as admin).
