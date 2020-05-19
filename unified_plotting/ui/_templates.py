"""HTML templates used by the Flask app."""

HTML_BASE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body>
{}
</body>
</html>"""

HTML_MAIN = """    <style>
        body {{
            margin: 0px;
            padding: 0px;
        }}
        #title-container {{
            width: 90vw;
            height: 6vh;
            margin: 0px;
            margin-top: 4vh;
            margin-left: 4vw;
            padding: 0px;
            font-family: mono;
            font-size: 12pt;
            color: #b81118;
        }}
        #main-container {{
            width: 90vw;
            height: 80vh;
            margin-left: 5vw;
            padding: 0px;
            font-family: mono!important;
            color: black!important;
        }}
        .container {{
            width: 31.33333333%;
            height: 100%;
            margin: 0px;
            padding-left: 1%;
            padding-right: 1%;
            float: left;
            overflow: auto;
        }}
        fieldset {{
            width: 99%;
            height: 97%;
            margin: 0px;
            padding: 0px;
            padding-top: 2%;
            padding-left: 2%;
            padding-right: 1px;
            color: #b81118;
            border-color: #111;
            border-width: 1px;
            border-radius: 7px;
            background-color: #fafafa;
            box-shadow: 1.5px 1.5px 3px #bbb;
            font-size: 10pt;
        }}
        #fieldset-right {{
            height: 49%;
        }}
        .inner-container {{
            width: 100%;
            height: 96%;
            margin: 0ex;
            padding: 0ex;
            overflow-x: hidden;
            overflow-y: auto;
        }}
        .vector-data {{
            width: 100%;
            margin: 0px;
            padding: 0px;
            display: block;
        }}
        .graph-data {{
            display: none;
        }}
        #vector-data-left {{
            width: 20%;
            float: left;
        }}
        #vector-data-right {{
            width: 80%;
            float: left;
        }}
        #vector-data-add-sub {{
            float: left;
            margin-top: 1ex;
            text-align:center;
            width:100%;
        }}
        #vector-data-counter {{
            display: none;
        }}
        .vector-name {{
            width: 70%;
            margin: 0px;
            padding: 0px;
        }}
        .vector-entries {{
            width: 91%;
            margin: 0px;
            padding: 0px;
        }}
        p {{
            margin-top: 1px;
            margin-bottom: 0px;
            padding: 0pt;
        }}
        label {{
            margin-left: 1ex;
            font-size: 8pt;
            color: black;
        }}
        input{{
            font-family: mono!important;
            font-size: 8pt;
        }}
        input[type=text]{{
            color: #00864b;
            margin-bottom: 1px;
        }}
        textarea{{
            width: 97%;
            height: 50vh;
            font-size: 7pt;
            color: #00864b;
            resize: vertical;
        }}
        .style-input {{
            width: 95%;
        }}
        #submit-container {{
            width: 100%;
            margin-top: 20%;
            text-align: center;
        }}
        input[type=submit] {{
            color: #b81118;
            background-color: #fbfbfb;
            border-color: #111;
            border-width: 1px;
            border-radius: 7px;
            padding-top: 1ex;
            padding-bottom: 1ex;
            padding-left: 2ex;
            padding-right: 2ex;
            text-decoration: none;
            text-align: center;
            font-size: 10pt;
            box-shadow: 1px 1px 2px #bbb;
            cursor: pointer;
        }}
        input[type=submit]:hover {{
            box-shadow: 2px 2px 3px #bbb, -1px -1px 1px #bbb;
        }}
        select {{
            font-family: mono!important;
            max-width: 90%;
            font-size: 8pt;
        }}
        #matplotlib-container {{
            display: block;
        }}
        #plotly-container {{
            display: none;
        }}
        #javascript-container {{
            display: none;
        }}
    </style>
    <form method="POST" target="_blank">
        <!-- Prevent implicit submission of the form -->
        <button type="submit" disabled style="display: none" aria-hidden="true"></button>
        <div id="title-container">
            Unified plotting
        </div>
        <div id="main-container">
            <div class="container">
                <fieldset>
                    <legend>Data</legend>
                    <div class="inner-container">
                        <div style="margin-bottom:1ex;">
                            <label for="data-type"">Type</label>
                            <br>
                            <select id="data-type" name="data-type" onChange="switchDataType();">
                                <option value="vector" selected>Vector data</option>
                                <option value="graph">Graph data</option>
                            </select>
                        </div>
                        <div class="vector-data">
                            <div>
                                <div id="vector-data-left">
                                    <label for="v1"">Name</label>
                                </div>
                                <div id="vector-data-right">
                                    <label for="v1n"">Entries</label>
                                </div>
                                <input type="text" id="vector-data-counter" value="3" name="num-vectors">
                            </div>
                            <br>
                            <div id="vector-data-add-sub"">
                                <button type="button" onclick="removeInputVector()">-</button>
                                <button type="button" onclick="addInputVector()">+</button>
                            </div>
                            <br>
                            <div style="float:left;margin-top:3ex;">
                                <input type="button" onclick="insertRandomNumbers()" value="Insert random numbers">
                                <input type="text" id="n" value="100" style="width:5ex;">
                            </div>
                        </div>
                        <div class="graph-data">
                            <label for="jgf-text">String in JSON graph format</label>
                            <br>
                            <textarea id="jgf-text" name="jgf-text"></textarea>
                            <br>
                            <div style="float:left;margin-top:3ex;">
                                <label>Insert JGF example</label>
                                <input type="button" onclick="insertGraphExample1()" value="1">
                                <input type="button" onclick="insertGraphExample2()" value="2">
                            </div>
                        </div>
                    </div>
                </fieldset>
            </div>
            <div class="container">
                <fieldset>
                    <legend>Style</legend>
                    <div class="inner-container">
                        <div class="vector-data">
{style_vector}
                        </div>
                        <div class="graph-data">
{style_graph}
                        </div>
                    </div>
                </fieldset>
            </div>
            <div class="container">
                <fieldset id="fieldset-right">
                    <legend>Function</legend>
                    <div class="inner-container">
                        <div class="vector-data">
                            <label for="library">Library</label>
                            <br>
                            <select id="library" name="library" onChange="switchLibrary();">
                                <option value="Matplotlib">Matplotlib</option>
                                <option value="Plotly">Plotly</option>
                                <option value="JavaScript">JavaScript</option>
                            </select>
                            <br>
                            <div id="plotly-container">
                                <label for="plot-type-plotly">Plot type</label>
                                <br>
                                <select id="plot-type-plotly" name="plot-type-plotly">
                                    <option value="bar">bar</option>
                                    <option value="density_2d">density_2d</option>
                                    <option value="density_scatter_histogram_2d">density_scatter_histogram_2d</option>
                                    <option value="histogram_2d">histogram_2d</option>
                                    <option value="scatter">scatter</option>
                                    <option disabled="disabled">---</option>
                                    <option value="contour">contour</option>
                                    <option value="heatmap">heatmap</option>
                                    <option value="scatter_3d">scatter_3d</option>
                                    <option value="surface">surface</option>
                                    <option disabled="disabled">---</option>
                                    <option value="band">band</option>
                                    <option value="box">box</option>
                                    <option value="density">density</option>
                                    <option value="histogram">histogram</option>
                                    <option value="parallel_coordinates">parallel_coordinates</option>
                                    <option value="scatter_matrix">scatter_matrix</option>
                                    <option value="violin">violin</option>
                                </select>
                                <br>
                                <label for="output-format-plotly">Output format</label>
                                <br>
                                <select id="output-format-plotly" name="output-format-plotly">
                                    <option value="html" selected>html</option>
                                    <!-- <option value="eps">eps</option> -->
                                    <option value="jpg">jpg</option>
                                    <option value="pdf">pdf</option>
                                    <option value="png">png</option>
                                    <option value="svg">svg</option>
                                    <option value="webp">webp</option>
                                </select>
                            </div>
                            <div id="matplotlib-container">
                                <label for="plot-type-matplotlib">Plot type</label>
                                <br>
                                <select id="plot-type-matplotlib" name="plot-type-matplotlib">
                                    <option value="hexbin">hexbin</option>
                                    <option value="histogram_2d">histogram_2d</option>
                                    <option value="scatter">scatter</option>
                                    <option disabled="disabled">---</option>
                                    <option value="contour">contour</option>
                                    <option value="scatter_3d">scatter_3d</option>
                                    <option disabled="disabled">---</option>
                                    <option value="box">box</option>
                                    <option value="histogram">histogram</option>
                                    <option value="scatter_matrix">scatter_matrix</option>
                                    <option value="violin">violin</option>
                                </select>
                                <br>
                                <label for="output-format-matplotlib">Output format</label>
                                <br>
                                <select id="output-format-matplotlib" name="output-format-matplotlib">
                                    <!-- <option value="eps">eps</option> -->
                                    <option value="pdf">pdf</option>
                                    <option value="png" selected>png</option>
                                    <!-- <option value="ps">ps</option> -->
                                    <option value="svg">svg</option>
                                </select>
                            </div>
                            <div id="javascript-container">
                                <label for="plot-type-javascript">Plot type</label>
                                <br>
                                <select id="plot-type-javascript" name="plot-type-javascript">
                                    <option value="parallel_coordinates_table">parallel_coordinates_table</option>
                                    <option value="table">table</option>
                                </select>
                                <br>
                                <label for="output-format-javascript">Output format</label>
                                <br>
                                <select id="output-format-javascript" name="output-format-javascript">
                                    <option value="html" selected>html</option>
                                </select>
                            </div>
                        </div>
                        <div class="graph-data">
                            <label for="library">Library</label>
                            <br>
                            <select id="graph-library" name="graph-library" onChange="switchLibrary();">
                                <option value="JavaScript">JavaScript</option>
                            </select>
                            <br>
                            <div id="graph-javascript-container">
                                <label for="graph-plot-type-javascript">Plot type</label>
                                <br>
                                <select id="graph-plot-type-javascript" name="graph-plot-type-javascript">
                                    <option value="network_d3">network_d3</option>
                                    <option value="network_vis">network_vis</option>
                                    <option value="network_webgl">network_webgl</option>
                                </select>
                                <br>
                                <label for="graph-format-javascript">Output format</label>
                                <br>
                                <select id="graph-format-javascript" name="graph-format-javascript" value="html">
                                    <option value="html" selected>html</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </fieldset>
                <br>
                <div id="submit-container">
                    <input type="submit" value="Create plot">
                </div>
            </div>
        </div>
    </form>
    <script>
        function insertRandomNumbers(){{
            function randint(start, end){{
                return Math.floor(Math.random() * (end - start + 1) + start);
            }}
            function randintString(numValues, start, end){{
                let arr = [];
                for (let i=1; i<=numValues; i++) {{
                    arr.push(randint(start, end));
                }}
                return arr.join(",")
            }}
            n = parseInt(document.getElementById("n").value);
            for (var i=1; i<=numVec; i++){{
                document.getElementById("vec" + i).value = randintString(n, 0, 100);
            }}
        }}
        function insertGraphExample1(){{
            const textarea = document.getElementById("jgf-text");
            textarea.value = '{jgf_data1}';
        }}
        function insertGraphExample2(){{
            const textarea = document.getElementById("jgf-text");
            textarea.value = '{jgf_data2}';
        }}
        function switchLibrary(){{
            const chosenLibrary = document.getElementById("library").value,
                matplotlibDiv = document.getElementById("matplotlib-container"),
                plotlyDiv = document.getElementById("plotly-container"),
                javascriptDiv = document.getElementById("javascript-container");
            if(chosenLibrary==="Plotly"){{
                plotlyDiv.style.display = "block";
                matplotlibDiv.style.display = "none";
                javascriptDiv.style.display = "none";
            }} else if(chosenLibrary=="Matplotlib") {{
                plotlyDiv.style.display = "none";
                matplotlibDiv.style.display = "block";
                javascriptDiv.style.display = "none";
            }} else {{
                plotlyDiv.style.display = "none";
                matplotlibDiv.style.display = "none";
                javascriptDiv.style.display = "block";
            }}
        }}
        function setVisibilityOfGroup(group, value){{
            for (let i=0; i<group.length; i++){{
                group[i].style.display = value;
            }}
        }}
        function switchDataType(){{
            const chosenDataType = document.getElementById("data-type").value,
                vectorDivs = document.getElementsByClassName("vector-data");
                graphDivs = document.getElementsByClassName("graph-data");
            if(chosenDataType==="vector"){{
                setVisibilityOfGroup(vectorDivs, "block");
                setVisibilityOfGroup(graphDivs, "none");
            }} else {{
                setVisibilityOfGroup(vectorDivs, "none");
                setVisibilityOfGroup(graphDivs, "block");
            }}
        }}
        function addInputVector(){{
            const left = document.getElementById("vector-data-left"),
                right = document.getElementById("vector-data-right"),
                counter = document.getElementById("vector-data-counter");
            numVec += 1;
            counter.setAttribute("value", numVec);
            const inputName = document.createElement("input");
            inputName.type = "text";
            inputName.id = "vec" + numVec + "-name";
            inputName.className = "vector-name";
            inputName.setAttribute("value", "vec" + numVec);
            inputName.setAttribute("name", inputName.id);
            left.appendChild(inputName);
            const inputData = document.createElement("input");
            inputData.type = "text";
            inputData.id = "vec" + numVec;
            inputData.className = "vector-entries";
            inputData.setAttribute("name", inputData.id);
            right.appendChild(inputData);
        }}
        function removeInputVector(){{
            const left = document.getElementById("vector-data-left"),
                right = document.getElementById("vector-data-right"),
                counter = document.getElementById("vector-data-counter");
            if(numVec > 1){{
                numVec -= 1;
                counter.setAttribute("value", numVec);
                left.removeChild(left.lastChild);
                right.removeChild(right.lastChild);
            }}
        }}
        var numVec = 0;
        addInputVector();
        addInputVector();
        addInputVector();
    </script>
"""
