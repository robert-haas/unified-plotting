Graphical user interface
########################

This package comes with a browser-based GUI that can be started from the command line.


1. Start it from the command line
=================================

After installing the Python package there is a new command available on the console. If you installed it in a virtual environment it has to be active. Invoking the command starts a local web server (`Waitress <https://github.com/Pylons/waitress>`__) that serves a simple web app (`Flask <https://flask.palletsprojects.com>`__) for generating plots in a browser of your choice.

.. code-block:: console

   $ unified_plotting

By default the web server uses the address ``127.0.0.1`` (localhost) and a random free port. It is also possible to specify address and port by passing them as optional arguments to the command:

.. code-block:: console

   $ unified_plotting --address 127.0.0.1 --port 42000


2. Access it in a browser
=========================

After starting the GUI on the command line it prints a message that states the address and port where the web app is served. Entering this string in a browser should open the GUI in it. How this looks like and a few things that can be done with it are demonstrated in the video below:

.. raw:: html

   <center>
     <video width="80%" poster="../_static/media/gui_thumbnail.png" controls>
       <source src="../_static/media/gui_screencast.mp4" type="video/mp4">
       Your browser does not support the HTML5 video tag.
     </video>
   </center>

|
