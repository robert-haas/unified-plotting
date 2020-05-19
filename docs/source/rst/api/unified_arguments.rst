Unified argument values
=======================



.. _marker-styles:

marker_style
------------

The :code:`marker_style` argument is currently unified across
all plots with Matplotlib and Plotly
that use markers to represent data values.

List of accepted formats
^^^^^^^^^^^^^^^^^^^^^^^^

- **Explicit name**

  - Example: :code:`"circle"`

- **Shortcut symbol**

  - Example: :code:`"o"`

List of accepted values
^^^^^^^^^^^^^^^^^^^^^^^

- :code:`"o"`, :code:`"circle"`
- :code:`"."`, :code:`"point"`, :code:`"dot"`
- :code:`"t"`, :code:`"3"`, :code:`"triangle"`
- :code:`"s"`, :code:`"4"`, :code:`"square"`
- :code:`"p"`, :code:`"5"`, :code:`"pentagon"`
- :code:`"h"`, :code:`"6"`, :code:`"hexagon"`
- :code:`"8"`, :code:`"octagon"`
- :code:`"*"`, :code:`"star"`
- :code:`"+"`, :code:`"plus"`
- :code:`"x"`, :code:`"cross"`
- :code:`"d"`, :code:`"diamond"`
- :code:`"-"`, :code:`"_"`, :code:`"horizontal_line"`
- :code:`"|"`, :code:`"vertical_line"`
- :code:`"^"`, :code:`"triangle_up"`
- :code:`"v"`, :code:`"triangle_down"`
- :code:`"<"`, :code:`"triangle_left"`
- :code:`">"`, :code:`"triangle_right"`

Exception: 3D plots in Plotly accept only a reduced list of values:

- :code:`"o"`, :code:`"circle"`
- :code:`"s"`, :code:`"4"`, :code:`"square"`
- :code:`"+"`, :code:`"plus"`
- :code:`"x"`, :code:`"cross"`
- :code:`"d"`, :code:`"diamond"`



.. _line-styles:

line_style
----------

The :code:`line_style` argument is currently unified across
all plots with Matplotlib and Plotly
that use lines to represent data values.

List of accepted formats
^^^^^^^^^^^^^^^^^^^^^^^^

- **Explicit name**

  - Example: :code:`"solid"`

- **Shortcut symbol**

  - Example: :code:`"-"`

List of accepted values
^^^^^^^^^^^^^^^^^^^^^^^

- :code:`"solid"`, :code:`"-"`
- :code:`"dash"`, :code:`"--"`
- :code:`"dashdot"`, :code:`"-."`, :code:`".-"`
- :code:`"dot"`, :code:`"."`, :code:`":"`, :code:`".."`



.. _colormaps:

colormap
--------

The :code:`colormap` argument is currently unified across
all plots with Matplotlib and Plotly
that use a color spectrum to represent numerical data values.

List of accepted values
^^^^^^^^^^^^^^^^^^^^^^^^

:ref:`colormap-list`

References
^^^^^^^^^^

- Built-in colormaps

  - `Matplotlib <https://matplotlib.org/tutorials/colors/colormaps.html>`_
  - `Plotly <https://plot.ly/python/builtin-colorscales>`_

- External colormaps that are provided in this package

  - `Colorcet <https://colorcet.holoviz.org>`_,
    `Peter Kovesi: CET Perceptually Uniform Colour Maps <https://peterkovesi.com/projects/colourmaps>`_,
    `GitHub: colorcet <here https://github.com/holoviz/colorcet>`_
  - `CMasher <https://cmasher.readthedocs.io>`_
  - `cmocean <https://matplotlib.org/cmocean>`_
  - `SciVisColor <https://sciviscolor.org/home/colormaps>`_

- Other resources, with some focus on color vision deficiencies

  - Containing at least one concrete colormap suggestion

    - Journal articles

      - `Nuñez et al.: Optimizing colormaps with consideration for color vision deficiency to enable accurate interpretation of scientific data <https://doi.org/10.1371/journal.pone.0199239>`_ where "Cividis" was derived from "Viridis", accompanying Python library `cmaputil <https://github.com/pnnl/cmaputil>`_.

        - `Scientific American: End of the Rainbow? New Map Scale Is More Readable by People Who Are Color Blind <https://www.scientificamerican.com/article/end-of-the-rainbow-new-map-scale-is-more-readable-by-people-who-are-color-blind/>`_

      - `Wong: Points of view: Color blindness <https://doi.org/10.1038/nmeth.1618>`_ (see CUD below)

    - Blog articles

      - `Tol: Colour schemes and templates <https://personal.sron.nl/~pault/>`_
      - `Okabe, Ito: Color Universal Design (CUD) <https://jfly.uni-koeln.de/color/>`_
      - `Krzywinski: Color Palettes for Color Blindness <http://mkweb.bcgsc.ca/colorblind/>`_
      - `Nichols: Coloring for Colorblindness <https://davidmathlogic.com/colorblind>`_
      - `Luk: Tips for designing scientific figures for color blind readers <https://www.somersault1824.com/tips-for-designing-scientific-figures-for-color-blind-readers/>`_
      - `Brewer et al.: Colorbrewer 2.0 <https://colorbrewer2.org>`_
      - `Google AI blog: Turbo, An Improved Rainbow Colormap for Visualization <https://ai.googleblog.com/2019/08/turbo-improved-rainbow-colormap-for.html>`_
      - `Kenneth Moreland: Color advice <http://www.kennethmoreland.com/color-advice>`_

  - Guidance on designing new colormaps

    - Journal articles
      - `Stauffer et al.: Somewhere Over the Rainbow: How to Make Effective Use of Colors in Meteorological Visualizations <https://doi.org/10.1175/BAMS-D-13-00155.1>`_ and the online tool `hclwizard <http://www.hclwizard.org/>`_

    - Other

      - `Kulesza et al.: Standardization of Color Palettes for Scientific Visualization <https://doi.org/10.2172/1363736>`_
      - `tableau: 5 tips on designing colorblind-friendly visualizations <https://www.tableau.com/about/blog/2016/4/examining-data-viz-rules-dont-use-red-green-together-53463>`_
      - `Petroff: Discernibility of (Rainbow) Colormaps <https://mpetroff.net/2019/08/discernibility-of-rainbow-colormaps/>`_
      - `VanderPlas: How Bad Is Your Colormap? <https://jakevdp.github.io/blog/2014/10/16/how-bad-is-your-colormap/>`_

  - Simulation of color vision deficiencies

    - `Colblindor <https://www.color-blindness.com/>`_
    - `Coblis (Color Blindness Simulator) <https://www.color-blindness.com/coblis-color-blindness-simulator/>`_
    - `Color Oracle <https://colororacle.org/>`_
    - `Vischeck and Daltonize <http://www.vischeck.com/>`_



.. _colors:

color
-----

The :code:`color` argument is currently unified across
all plots with Matplotlib and Plotly
that use discrete colors to represent data values or entire vectors.

List of accepted formats
^^^^^^^^^^^^^^^^^^^^^^^^

- **Named color**

  - List of accepted values: :ref:`named-color-list`

  - Examples: :code:`"g"`, :code:`"darkseagreen"`, :code:`"tab.green"`, :code:`"xkcd.algae_green"`

- **Hexadecimal triplet**

  - Needs to start with :code:`#` being followed by 6 hexadecimal digits (:code:`0-9` and :code:`A-F`). Letters can be given in lower or upper case.
  - Examples: :code:`"#CC7030"`, :code:`"#00ff00"`

- **Shorthand hexadecimal triplet**

  - Needs to start with :code:`#` being followed by 3 hexadecimal digits (:code:`0-9` and :code:`A-F`). Each digits is doubled automatically, thereby expanding to the 6 digits form. Letters can be given in lower or upper case.
  - Example: :code:`"#0f0"` which is equivalent to :code:`"#00ff00"`

- **RGB**

  - Can be either a string of the form :code:`"rgb(number, number, number)"` or a tuple of the form :code:`(number, number, number)` where number is either an integer from :code:`0 to 255` or a float from :code:`0.0 to 1.0` (gets internally multiplied by 255 and casted to integer).
  - Examples: String :code:`"rgb(51, 51, 255)"`, tuple :code:`(51, 51, 255)` or equivalently string :code:`"rgb(0.2, 0.2, 1.0)"` and tuple :code:`(0.2, 0.2, 1.0)`

- **RGBA**

  - Can be either a string of the form :code:`"rgba(number, number, number, number)"` or a tuple of the form :code:`(number, number, number, number)`. The first three numbers can be either an integer from :code:`0 to 255` or a float from :code:`0.0 to 1.0`. The fourth number needs to be a float from :code:`0.0 to 1.0`.
  - Examples: String :code:`"rgba(0, 255, 0, 0.3)"` or the equivalent tuple :code:`(0, 255, 0, 0.3)`

List of default colors
^^^^^^^^^^^^^^^^^^^^^^

The default colors were chosen in order to be distinguishable by people with different
color vision deficiencies (CVD) and also to work when plots are converted into grayscale
as it may happen in print:

1. "#6059a0"
2. "#df4828"
3. "#69b190"
4. "#ddaa3c"
5. "#d1c1e1"
6. "#4e96bc"
7. "#95211b"
8. "#a6be54"
9. "#e67932"
10. "#9b62a7"
11. "#4e79c5"
12. "#521a13"
13. "#8cbc68"
14. "#e4632d"
15. "#b58fc2"

These colors were selected from Figure 19 of
Paul Tol's `colour schemes and templates <https://personal.sron.nl/~pault/>`_
by checking that the first 6-7 colors are easily distinguishable
with different color vision deficiencies as simulated with 
`Coblis <https://www.color-blindness.com/coblis-color-blindness-simulator/>`_.

.. image:: ../../images/colors/default_colors.png
  :width: 700

Example: A scatter plot that uses colors 1 to 6 to demonstrate their approximate
appearance for people with different CVD.
Regarding the content of the plot, it uses a logarithmic y scale to visualize the
exponential growth of confirmed COVID-19 cases in countries of central europe
during February and March 2020.

- Original

  .. image:: ../../images/colors/covid_original.png
    :width: 350

- Grayscale (converted with `GIMP <https://www.gimp.org>`_)

  .. image:: ../../images/colors/covid_grayscale.png
    :width: 350

- Dichromatic: Protanopia

  .. image:: ../../images/colors/covid_dichromatic_protanopia.png
    :width: 350

- Dichromatic: Deuteranopia

  .. image:: ../../images/colors/covid_dichromatic_deuteranopia.png
    :width: 350

- Dichromatic: Tritanopia

  .. image:: ../../images/colors/covid_dichromatic_tritanopia.png
    :width: 350

- Monochromatic: Blue cone monochromacy

  .. image:: ../../images/colors/covid_monochromatic_blue_cone.png
    :width: 350
  
- Monochromatic: Achromatopsia

  .. image:: ../../images/colors/covid_monochromatic_achromatopsia.png
    :width: 350


References
^^^^^^^^^^

- Wikipedia

  - `Hex triplet <https://en.wikipedia.org/wiki/Web_colors#Hex_triplet>`_
  - `RGB color space <https://en.wikipedia.org/wiki/RGB_color_space>`_
  - `RGBA color space <https://en.wikipedia.org/wiki/RGBA_color_space>`_

- Matplotlib

  - `Specifying colors <https://matplotlib.org/users/colors.html>`_
  - `Colors API <https://matplotlib.org/api/colors_api.html>`_

- xkcd

  - `Color survey <https://xkcd.com/color/rgb/>`_
