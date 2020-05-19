:orphan:

Why ...?
########

Why is a high-level plotting API useful?
========================================

A dilemma with plotting libraries is that they try to provide

- much flexibility, so a user can express almost any idea of a visualization in intricate code.
- ease of use, so a user can generate common plot types with simple code.

For this reason, many libraries already provide simplified, high-level APIs, which sit on top of all their detailed plotting capabilities in order to ease the creation of frequently-used plots:

- Matplotlib provides `pyplot <https://matplotlib.org/api/_as_gen/matplotlib.pyplot.html>`__, which originated from the no longer recommended `pylab <https://matplotlib.org/faq/usage_faq.html#matplotlib-pyplot-and-pylab-how-are-they-related>`__.
- Plotly added `plotly.express <https://plot.ly/python-api-reference/plotly.express.html>`__ with `version 4 <https://community.plotly.com/t/introducing-plotly-py-4-0-0/25639>`__.
- D3.js has an ecosystem of `third-party libraries <https://github.com/wbkd/awesome-d3>`__ building on top of it (Plotly is one of them). They provide simpler access to its quite low-level functionality, often focusing on a specific niche. Unified plotting is currently using D3.js and other JavaScript libraries for graph visualization, adding a lot of interactive control elements.

A second dilemma with plotting libraries is that

- Most programming languages already have established visualization libraries. To provide a new one, a certain degree of novelty and uniqueness is needed in order to stick out, which naturally includes the architecture of the package and how a user can interact with it.
- Most users probably do not like to remember multiple ways of achieving comparable outcomes with different libraries, so they stick with what they got used to. Therefore to make a new library more attractive, an alternative strategy can be to design it highly compatible with an already popular package but add novel plot types. An example for that is `Seaborn <https://seaborn.pydata.org/>`__, which provides great statistical plots by tightly integrating with Matplotlib.

In summary, there is evidently an incentive for plotting libraries to build their own high-level API, yet none to extend it beyond their own affairs. Assuming that users of a language may benefit from the same idea taken to a broader scope, from intra to inter library, this package makes a unification attempt to create a simple, consistent API for using multiple plotting libraries for common plot types. Ideally this should result in exaclty one way of access to all those libraries, and while this is largely achieved, it is hard to fully compensate for all non-overlapping functionality. This can result in some ignored arguments, limited subsets of accepted values for an argument, or skipped plotting capabilities. Where this package has such shortcomings, notes can be found in the API documentation and warnings are emitted in the case an ignored argument or an invalid value is passed to a function.


Why has it not been done yet?
=============================

The idea to unify some plotting capabilities available in the Python ecosystem has already been realized a few times, yet not in a way that was suitable for the requirements of my other packages (e.g. interactive 3D and graph visualizations, simple text representations for web-serving). Here are some examples you may want to take a look at:

- `astetik <https://github.com/autonomio/astetik>`__
- `chartpy <https://github.com/cuemacro/chartpy>`__
- `easyplot <https://github.com/HamsterHuey/easyplot>`__
- `easyviz <https://hplgit.github.io/scitools/doc/api/html/easyviz.html>`__
- `uniplot <http://sean1708.github.io/uniplot>`__
