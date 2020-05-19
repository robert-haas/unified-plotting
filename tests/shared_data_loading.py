import csv
import inspect
import os


def get_path_of_this_file():
    # https://stackoverflow.com/questions/2632199/how-do-i-get-the-path-of-the-current-executed-file-in-python
    return os.path.abspath(inspect.getsourcefile(lambda _: None))


TESTFILE_DIR = os.path.dirname(get_path_of_this_file())
IN_DIR = os.path.join(TESTFILE_DIR, 'in')


def construct_testdata():
    def read_csv(filepath):
        x, y, z = [], [], []
        with open(filepath, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                try:
                    x.append(float(row[0]))
                    y.append(float(row[1]))
                    z.append(float(row[2]))
                except ValueError:
                    pass
        return x, y, z

    # Read all csv files in the test folder and add it as one (x,y,z) data set to testdata
    testdata = []
    for filename in sorted(os.listdir(IN_DIR)):
        if filename.endswith('.csv'):
            filepath = os.path.join(IN_DIR, filename)
            testdata.append([filename] + list(read_csv(filepath)))
    return testdata


def construct_testdata_small():
    x = list(range(12))
    y = list(range(4))*3
    z = list(range(3))*4
    testdata = ['small', x, y, z]
    return [testdata]


def construct_testdata_grid():
    x = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    y = ['Evening', 'Afternoon', 'Morning']
    z = [[0, 1, 2, 4, 5], [2, 3, 4, 5, 6], [0, 1, 2, 3, 4]]
    testdata = ['grid', x, y, z]
    return [testdata]


def construct_testdata_files(extension):
    testdata = []
    for filename in sorted(os.listdir(IN_DIR)):
        if filename.endswith(extension):
            filepath = os.path.abspath(os.path.join(IN_DIR, filename))
            name = os.path.basename(filename)
            testdata.append([name, filepath])
    return testdata


TESTDATA = construct_testdata()
TESTDATA_SMALL = construct_testdata_small()
TESTDATA_GRID = construct_testdata_grid()
TESTDATA_CSV_FILES = construct_testdata_files('.csv')
TESTDATA_JSON_FILES = construct_testdata_files('.json')
TESTDATA_PDF_FILES = construct_testdata_files('.pdf')
TESTDATA_PNG_FILES = construct_testdata_files('.png')
TESTDATA_SVG_FILES = construct_testdata_files('.svg')

MARKER_STYLES = [
    'o', 'circle',
    '.', 'point', 'dot',
    't', '3', 'triangle',
    's', '4', 'square',
    'p', '5', 'pentagon',
    'h', '6', 'hexagon',
    '8', 'octagon',
    '*', 'star',
    '+', 'plus',
    'x', 'cross',
    'd', 'diamond',
    '-', '_', 'horizontal_line',
    '|', 'vertical_line',
    '^', 'triangle_up',
    'v', 'triangle_down',
    '<', 'triangle_left',
    '>', 'triangle_right',
]

LINE_STYLES = [
    'solid', '-',
    'dash', '--',
    'dashdot', '-.', '.-',
    'dot', '.', ':', '..'
]

ALL_COLORMAPS = [
    'accent', 'afmhot', 'autumn', 'binary', 'blues', 'bone', 'brbg', 'brg', 'bugn', 'bupu',
    'bwr', 'cividis', 'cmrmap', 'cool', 'coolwarm', 'copper', 'cubehelix', 'dark2', 'flag',
    'gist_earth', 'gist_gray', 'gist_heat', 'gist_ncar', 'gist_rainbow', 'gist_stern',
    'gist_yarg', 'gnbu', 'gnuplot', 'gnuplot2', 'gray', 'greens', 'greys', 'hot', 'hsv',
    'inferno', 'jet', 'magma', 'nipy_spectral', 'ocean', 'oranges', 'orrd', 'paired',
    'pastel1', 'pastel2', 'pink', 'piyg', 'plasma', 'prgn', 'prism', 'pubu', 'pubugn',
    'puor', 'purd', 'purples', 'rainbow', 'rdbu', 'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'reds',
    'seismic', 'set1', 'set2', 'set3', 'spectral', 'spring', 'summer', 'tab10', 'tab20',
    'tab20b', 'tab20c', 'terrain', 'twilight', 'twilight_shifted', 'viridis', 'winter',
    'wistia', 'ylgn', 'ylgnbu', 'ylorbr', 'ylorrd',

    'aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance', 'blackbody', 'bluered',
    'blugrn', 'bluyl', 'brwnyl', 'burg', 'burgyl', 'curl', 'darkmint', 'deep', 'delta',
    'dense', 'earth', 'edge', 'electric', 'emrld', 'fall',  'geyser', 'haline', 'ice', 'icefire',
    'magenta', 'matter', 'mint', 'mrybm', 'mygbm', 'oryel',  'peach', 'phase', 'picnic', 'pinkyl',
    'plotly3', 'portland', 'purp', 'purpor', 'redor',  'solar', 'speed', 'sunset', 'sunsetdark',
    'teal', 'tealgrn', 'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid'

    'cet.cyclic_grey_15_85_c0', 'cet.cyclic_grey_15_85_c0_s25', 'cet.cyclic_mrybm_35_75_c68',
    'cet.cyclic_mrybm_35_75_c68_s25', 'cet.cyclic_mygbm_30_95_c78',
    'cet.cyclic_mygbm_30_95_c78_s25', 'cet.cyclic_protanopic_deuteranopic_bwyk_16_96_c31',
    'cet.cyclic_protanopic_deuteranopic_wywb_55_96_c33',
    'cet.cyclic_tritanopic_cwrk_40_100_c20', 'cet.cyclic_tritanopic_wrwc_70_100_c20',
    'cet.cyclic_wrwbw_40_90_c42', 'cet.cyclic_wrwbw_40_90_c42_s25', 'cet.diverging_bkr_55_10_c35',
    'cet.diverging_bky_60_10_c30', 'cet.diverging_bwg_20_95_c41', 'cet.diverging_bwr_20_95_c54',
    'cet.diverging_bwr_40_95_c42', 'cet.diverging_bwr_55_98_c37', 'cet.diverging_cwm_80_100_c22',
    'cet.diverging_gkr_60_10_c40', 'cet.diverging_gwr_55_95_c38', 'cet.diverging_gwv_55_95_c39',
    'cet.diverging_isoluminant_cjm_75_c23', 'cet.diverging_isoluminant_cjm_75_c24',
    'cet.diverging_isoluminant_cjo_70_c25', 'cet.diverging_linear_bjr_30_55_c53',
    'cet.diverging_linear_bjy_30_90_c45', 'cet.diverging_protanopic_deuteranopic_bwy_60_95_c32',
    'cet.diverging_rainbow_bgymr_45_85_c67', 'cet.diverging_tritanopic_cwr_75_98_c20',
    'cet.glasbey_bw', 'cet.glasbey_bw_minc_20', 'cet.glasbey_bw_minc_20_hue_150_280',
    'cet.glasbey_bw_minc_20_hue_330_100', 'cet.glasbey_bw_minc_20_maxl_70',
    'cet.glasbey_bw_minc_20_minl_30', 'cet.glasbey_category10', 'cet.glasbey_hv',
    'cet.isoluminant_cgo_70_c39', 'cet.isoluminant_cgo_80_c38', 'cet.isoluminant_cm_70_c39',
    'cet.linear_bgy_10_95_c74', 'cet.linear_bgyw_15_100_c67', 'cet.linear_bgyw_15_100_c68',
    'cet.linear_bgyw_20_98_c66', 'cet.linear_blue_5_95_c73', 'cet.linear_blue_95_50_c20',
    'cet.linear_bmw_5_95_c86', 'cet.linear_bmw_5_95_c89', 'cet.linear_bmy_10_95_c71',
    'cet.linear_bmy_10_95_c78', 'cet.linear_gow_60_85_c27', 'cet.linear_gow_65_90_c35',
    'cet.linear_green_5_95_c69', 'cet.linear_grey_0_100_c0', 'cet.linear_grey_10_95_c0',
    'cet.linear_kbc_5_95_c73', 'cet.linear_kbgyw_5_98_c62', 'cet.linear_kgy_5_95_c69',
    'cet.linear_kry_0_97_c73', 'cet.linear_kry_5_95_c72', 'cet.linear_kry_5_98_c75',
    'cet.linear_kryw_0_100_c71', 'cet.linear_kryw_5_100_c64', 'cet.linear_kryw_5_100_c67',
    'cet.linear_protanopic_deuteranopic_kbjyw_5_95_c25',
    'cet.linear_protanopic_deuteranopic_kbw_5_98_c40', 'cet.linear_ternary_blue_0_44_c57',
    'cet.linear_ternary_green_0_46_c42', 'cet.linear_ternary_red_0_50_c52',
    'cet.linear_tritanopic_krjcw_5_95_c24', 'cet.linear_tritanopic_krjcw_5_98_c46',
    'cet.linear_wcmr_100_45_c42', 'cet.linear_worb_100_25_c53', 'cet.linear_wyor_100_45_c55',
    'cet.rainbow_bgyr_35_85_c72', 'cet.rainbow_bgyr_35_85_c73', 'cet.rainbow_bgyrm_35_85_c69',
    'cet.rainbow_bgyrm_35_85_c71',

    'cmo.algae', 'cmo.amp', 'cmo.balance', 'cmo.curl', 'cmo.deep', 'cmo.delta', 'cmo.dense',
    'cmo.diff', 'cmo.gray', 'cmo.haline', 'cmo.ice', 'cmo.matter', 'cmo.oxy', 'cmo.phase',
    'cmo.rain', 'cmo.solar', 'cmo.speed', 'cmo.tarn', 'cmo.tempo', 'cmo.thermal', 'cmo.topo',
    'cmo.turbid',

    'cmr.amber', 'cmr.apple', 'cmr.arctic', 'cmr.chroma', 'cmr.dusk', 'cmr.eclipse', 'cmr.ember',
    'cmr.flamingo', 'cmr.freeze', 'cmr.fusion', 'cmr.gem', 'cmr.gothic', 'cmr.heat',
    'cmr.horizon', 'cmr.iceburn', 'cmr.jungle', 'cmr.lavender', 'cmr.neutral', 'cmr.nuclear',
    'cmr.ocean', 'cmr.rainforest', 'cmr.redshift', 'cmr.sunburst', 'cmr.voltage', 'cmr.waterlily',

    'svc.3wave-blue-gray-brown', 'svc.3wave-brown-to-green', 'svc.3wave-gray-blue-gray',
    'svc.3wave-gray-green-blue', 'svc.3wave-green-gray-yellow', 'svc.3wave-yellow-gray-blue',
    'svc.4wave-blue-to-gray', 'svc.4wave-blue-to-red', 'svc.4wave-blue-to-yellow',
    'svc.4wave-gray-blue-red', 'svc.4wave-orange-green-gray', 'svc.4wave-red-blue',
    'svc.4wave-yellow-green-gray', 'svc.5wave-blue-red-blue', 'svc.5wave-orange-to-green',
    'svc.5wave-yellow-and-green', 'svc.5wave-yellow-brown-blue', 'svc.5wave-yellow-to-blue',
    'svc.blue1', 'svc.blue10', 'svc.blue11', 'svc.blue2', 'svc.blue3', 'svc.blue4',
    'svc.blue5', 'svc.blue6', 'svc.blue7', 'svc.blue8', 'svc.blue9', 'svc.brown1', 'svc.brown2',
    'svc.brown3', 'svc.brown4', 'svc.brown5', 'svc.brown6', 'svc.brown7', 'svc.brown8',
    'svc.brown9', 'svc.discrete-4-blue-green', 'svc.discrete-4-blue-orange',
    'svc.discrete-4-light', 'svc.discrete-4-van-eyck', 'svc.discrete-5-autumn',
    'svc.discrete-5-dark', 'svc.discrete-7', 'svc.div-blue-orange', 'svc.div-gray-gold',
    'svc.div-green-brown', 'svc.div-orange-blue', 'svc.div-turqoise-olive', 'svc.green1',
    'svc.green2', 'svc.green3', 'svc.green4', 'svc.green5', 'svc.green6', 'svc.green7',
    'svc.green8', 'svc.insert-green-0-10', 'svc.insert-green-0-20', 'svc.insert-green-10-20',
    'svc.insert-green-20-30', 'svc.insert-green-20-40', 'svc.insert-green-30-40',
    'svc.insert-green-40-50', 'svc.insert-green-40-60', 'svc.insert-green-50-60',
    'svc.insert-green-60-70', 'svc.insert-green-60-80', 'svc.insert-green-70-80',
    'svc.insert-green-80-100', 'svc.insert-green-80-90', 'svc.insert-green-90-100',
    'svc.maroon', 'svc.orange1', 'svc.orange2', 'svc.orange3', 'svc.outlier-blue-orange',
    'svc.outlier-blue-red', 'svc.outlier-blue-red-middle', 'svc.outlier-brown-gray-blue',
    'svc.outlier-brown-orange', 'svc.outlier-gray-10', 'svc.outlier-gray-15',
    'svc.outlier-gray-20', 'svc.outlier-gray-25', 'svc.outlier-gray-5', 'svc.outlier-green-blue',
    'svc.outlier-green-blue-2', 'svc.outlier-orange-turqoise', 'svc.purple1', 'svc.purple2',
    'svc.purple3', 'svc.rainbow-blue', 'svc.rainbow-mellow', 'svc.rainbow-mellow-wave',
    'svc.red1', 'svc.red2', 'svc.red3', 'svc.red4', 'svc.yellow1', 'svc.yellow2', 'svc.yellow3',
    'svc.yellow4', 'svc.yellow5',
]

TEST_COLORS = [
    '#00ff00',
    '#0AF73C',
    '#0Af73c',
    '#0F0',
    '#0fa',
    (1, 2, 3),
    (1, 1, 1),
    (1.0, 1.0, 1.0),
    (255, 255, 255),
    (1, 2, 3, 0.1),
    (1, 1, 1, 0.1),
    (1.0, 1.0, 1.0, 0.1),
    (255, 255, 255, 1.0),
    'rgb(1, 2, 3)',
    'rgb(1, 1, 1)',
    'rgb(1.0, 1.0, 1.0)',
    'rgb(255, 255, 255)',
    'rgba(1, 2, 3, 0.1)',
    'rgba(1, 1, 1, 0.1)',
    'rgba(1.0, 1.0, 1.0, 0.1)',
    'rgba(255, 255, 255, 1.0)',
    'g',
    'fuchsia',
    'tab.purple',
    'xkcd.blood_orange',
]

NAMED_COLORS = [
    'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'b', 'beige', 'bisque', 'black',
    'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'c', 'cadetblue', 'chartreuse',
    'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan',
    'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta',
    'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen',
    'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink',
    'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen',
    'fuchsia', 'g', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'green',
    'greenyellow', 'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'k',
    'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral',
    'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink',
    'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey',
    'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'm', 'magenta', 'maroon',
    'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen',
    'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue',
    'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab',
    'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise',
    'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple',
    'r', 'rebeccapurple', 'red', 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown',
    'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey',
    'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise',
    'violet', 'w', 'wheat', 'white', 'whitesmoke',

    'tab.blue', 'tab.brown', 'tab.cyan', 'tab.gray', 'tab.green', 'tab.olive', 'tab.orange',
    'tab.pink', 'tab.purple', 'tab.red',

    'xkcd.acid_green', 'xkcd.adobe', 'xkcd.algae', 'xkcd.algae_green',
    'xkcd.almost_black', 'xkcd.amber', 'xkcd.amethyst', 'xkcd.apple', 'xkcd.apple_green',
    'xkcd.apricot', 'xkcd.aqua', 'xkcd.aqua_blue', 'xkcd.aqua_green', 'xkcd.aqua_marine',
    'xkcd.aquamarine', 'xkcd.army_green', 'xkcd.asparagus', 'xkcd.aubergine', 'xkcd.auburn',
    'xkcd.avocado', 'xkcd.avocado_green', 'xkcd.azul', 'xkcd.azure', 'xkcd.baby_blue',
    'xkcd.baby_green', 'xkcd.baby_pink', 'xkcd.baby_poo', 'xkcd.baby_poop',
    'xkcd.baby_poop_green', 'xkcd.baby_puke_green', 'xkcd.baby_purple',
    'xkcd.baby_shit_brown', 'xkcd.baby_shit_green', 'xkcd.banana', 'xkcd.banana_yellow',
    'xkcd.barbie_pink', 'xkcd.barf_green', 'xkcd.barney', 'xkcd.barney_purple',
    'xkcd.battleship_grey', 'xkcd.beige', 'xkcd.berry', 'xkcd.bile', 'xkcd.black',
    'xkcd.bland', 'xkcd.blood', 'xkcd.blood_orange', 'xkcd.blood_red', 'xkcd.blue',
    'xkcd.blue_blue', 'xkcd.blue_green', 'xkcd.blue_grey', 'xkcd.blue_purple',
    'xkcd.blue_violet', 'xkcd.blue_with_a_hint_of_purple', 'xkcd.blueberry', 'xkcd.bluegreen',
    'xkcd.bluegrey', 'xkcd.bluey_green', 'xkcd.bluey_grey', 'xkcd.bluey_purple', 'xkcd.bluish',
    'xkcd.bluish_green', 'xkcd.bluish_grey', 'xkcd.bluish_purple', 'xkcd.blurple', 'xkcd.blush',
    'xkcd.blush_pink', 'xkcd.booger', 'xkcd.booger_green', 'xkcd.bordeaux', 'xkcd.boring_green',
    'xkcd.bottle_green', 'xkcd.brick', 'xkcd.brick_orange', 'xkcd.brick_red', 'xkcd.bright_aqua',
    'xkcd.bright_blue', 'xkcd.bright_cyan', 'xkcd.bright_green', 'xkcd.bright_lavender',
    'xkcd.bright_light_blue', 'xkcd.bright_light_green', 'xkcd.bright_lilac', 'xkcd.bright_lime',
    'xkcd.bright_lime_green', 'xkcd.bright_magenta', 'xkcd.bright_olive', 'xkcd.bright_orange',
    'xkcd.bright_pink', 'xkcd.bright_purple', 'xkcd.bright_red', 'xkcd.bright_sea_green',
    'xkcd.bright_sky_blue', 'xkcd.bright_teal', 'xkcd.bright_turquoise', 'xkcd.bright_violet',
    'xkcd.bright_yellow', 'xkcd.bright_yellow_green', 'xkcd.british_racing_green', 'xkcd.bronze',
    'xkcd.brown', 'xkcd.brown_green', 'xkcd.brown_grey', 'xkcd.brown_orange', 'xkcd.brown_red',
    'xkcd.brown_yellow', 'xkcd.brownish', 'xkcd.brownish_green', 'xkcd.brownish_grey',
    'xkcd.brownish_orange', 'xkcd.brownish_pink', 'xkcd.brownish_purple', 'xkcd.brownish_red',
    'xkcd.brownish_yellow', 'xkcd.browny_green', 'xkcd.browny_orange', 'xkcd.bruise',
    'xkcd.bubble_gum_pink', 'xkcd.bubblegum', 'xkcd.bubblegum_pink', 'xkcd.buff', 'xkcd.burgundy',
    'xkcd.burnt_orange', 'xkcd.burnt_red', 'xkcd.burnt_siena', 'xkcd.burnt_sienna',
    'xkcd.burnt_umber', 'xkcd.burnt_yellow', 'xkcd.burple', 'xkcd.butter', 'xkcd.butter_yellow',
    'xkcd.butterscotch', 'xkcd.cadet_blue', 'xkcd.camel', 'xkcd.camo', 'xkcd.camo_green',
    'xkcd.camouflage_green', 'xkcd.canary', 'xkcd.canary_yellow', 'xkcd.candy_pink',
    'xkcd.caramel', 'xkcd.carmine', 'xkcd.carnation', 'xkcd.carnation_pink',
    'xkcd.carolina_blue', 'xkcd.celadon', 'xkcd.celery', 'xkcd.cement', 'xkcd.cerise',
    'xkcd.cerulean', 'xkcd.cerulean_blue', 'xkcd.charcoal', 'xkcd.charcoal_grey',
    'xkcd.chartreuse', 'xkcd.cherry', 'xkcd.cherry_red', 'xkcd.chestnut', 'xkcd.chocolate',
    'xkcd.chocolate_brown', 'xkcd.cinnamon', 'xkcd.claret', 'xkcd.clay', 'xkcd.clay_brown',
    'xkcd.clear_blue', 'xkcd.cloudy_blue', 'xkcd.cobalt', 'xkcd.cobalt_blue', 'xkcd.cocoa',
    'xkcd.coffee', 'xkcd.cool_blue', 'xkcd.cool_green', 'xkcd.cool_grey', 'xkcd.copper',
    'xkcd.coral', 'xkcd.coral_pink', 'xkcd.cornflower', 'xkcd.cornflower_blue', 'xkcd.cranberry',
    'xkcd.cream', 'xkcd.creme', 'xkcd.crimson', 'xkcd.custard', 'xkcd.cyan', 'xkcd.dandelion',
    'xkcd.dark', 'xkcd.dark_aqua', 'xkcd.dark_aquamarine', 'xkcd.dark_beige', 'xkcd.dark_blue',
    'xkcd.dark_blue_green', 'xkcd.dark_blue_grey', 'xkcd.dark_brown', 'xkcd.dark_coral',
    'xkcd.dark_cream', 'xkcd.dark_cyan', 'xkcd.dark_forest_green', 'xkcd.dark_fuchsia',
    'xkcd.dark_gold', 'xkcd.dark_grass_green', 'xkcd.dark_green', 'xkcd.dark_green_blue',
    'xkcd.dark_grey', 'xkcd.dark_grey_blue', 'xkcd.dark_hot_pink', 'xkcd.dark_indigo',
    'xkcd.dark_khaki', 'xkcd.dark_lavender', 'xkcd.dark_lilac', 'xkcd.dark_lime',
    'xkcd.dark_lime_green', 'xkcd.dark_magenta', 'xkcd.dark_maroon', 'xkcd.dark_mauve',
    'xkcd.dark_mint', 'xkcd.dark_mint_green', 'xkcd.dark_mustard', 'xkcd.dark_navy',
    'xkcd.dark_navy_blue', 'xkcd.dark_olive', 'xkcd.dark_olive_green', 'xkcd.dark_orange',
    'xkcd.dark_pastel_green', 'xkcd.dark_peach', 'xkcd.dark_periwinkle', 'xkcd.dark_pink',
    'xkcd.dark_plum', 'xkcd.dark_purple', 'xkcd.dark_red', 'xkcd.dark_rose',
    'xkcd.dark_royal_blue', 'xkcd.dark_sage', 'xkcd.dark_salmon', 'xkcd.dark_sand',
    'xkcd.dark_sea_green', 'xkcd.dark_seafoam', 'xkcd.dark_seafoam_green', 'xkcd.dark_sky_blue',
    'xkcd.dark_slate_blue', 'xkcd.dark_tan', 'xkcd.dark_taupe', 'xkcd.dark_teal',
    'xkcd.dark_turquoise', 'xkcd.dark_violet', 'xkcd.dark_yellow', 'xkcd.dark_yellow_green',
    'xkcd.darkblue', 'xkcd.darkgreen', 'xkcd.darkish_blue', 'xkcd.darkish_green',
    'xkcd.darkish_pink', 'xkcd.darkish_purple', 'xkcd.darkish_red', 'xkcd.deep_aqua',
    'xkcd.deep_blue', 'xkcd.deep_brown', 'xkcd.deep_green', 'xkcd.deep_lavender',
    'xkcd.deep_lilac', 'xkcd.deep_magenta', 'xkcd.deep_orange', 'xkcd.deep_pink',
    'xkcd.deep_purple', 'xkcd.deep_red', 'xkcd.deep_rose', 'xkcd.deep_sea_blue',
    'xkcd.deep_sky_blue', 'xkcd.deep_teal', 'xkcd.deep_turquoise', 'xkcd.deep_violet',
    'xkcd.denim', 'xkcd.denim_blue', 'xkcd.desert', 'xkcd.diarrhea', 'xkcd.dirt',
    'xkcd.dirt_brown', 'xkcd.dirty_blue', 'xkcd.dirty_green', 'xkcd.dirty_orange',
    'xkcd.dirty_pink', 'xkcd.dirty_purple', 'xkcd.dirty_yellow', 'xkcd.dodger_blue', 'xkcd.drab',
    'xkcd.drab_green', 'xkcd.dried_blood', 'xkcd.duck_egg_blue', 'xkcd.dull_blue',
    'xkcd.dull_brown', 'xkcd.dull_green', 'xkcd.dull_orange', 'xkcd.dull_pink',
    'xkcd.dull_purple', 'xkcd.dull_red', 'xkcd.dull_teal', 'xkcd.dull_yellow', 'xkcd.dusk',
    'xkcd.dusk_blue', 'xkcd.dusky_blue', 'xkcd.dusky_pink', 'xkcd.dusky_purple',
    'xkcd.dusky_rose', 'xkcd.dust', 'xkcd.dusty_blue', 'xkcd.dusty_green', 'xkcd.dusty_lavender',
    'xkcd.dusty_orange', 'xkcd.dusty_pink', 'xkcd.dusty_purple', 'xkcd.dusty_red',
    'xkcd.dusty_rose', 'xkcd.dusty_teal', 'xkcd.earth', 'xkcd.easter_green', 'xkcd.easter_purple',
    'xkcd.ecru', 'xkcd.egg_shell', 'xkcd.eggplant', 'xkcd.eggplant_purple', 'xkcd.eggshell',
    'xkcd.eggshell_blue', 'xkcd.electric_blue', 'xkcd.electric_green', 'xkcd.electric_lime',
    'xkcd.electric_pink', 'xkcd.electric_purple', 'xkcd.emerald', 'xkcd.emerald_green',
    'xkcd.evergreen', 'xkcd.faded_blue', 'xkcd.faded_green', 'xkcd.faded_orange',
    'xkcd.faded_pink', 'xkcd.faded_purple', 'xkcd.faded_red', 'xkcd.faded_yellow', 'xkcd.fawn',
    'xkcd.fern', 'xkcd.fern_green', 'xkcd.fire_engine_red', 'xkcd.flat_blue', 'xkcd.flat_green',
    'xkcd.fluorescent_green', 'xkcd.fluro_green', 'xkcd.foam_green', 'xkcd.forest',
    'xkcd.forest_green', 'xkcd.forrest_green', 'xkcd.french_blue', 'xkcd.fresh_green',
    'xkcd.frog_green', 'xkcd.fuchsia', 'xkcd.gold', 'xkcd.golden', 'xkcd.golden_brown',
    'xkcd.golden_rod', 'xkcd.golden_yellow', 'xkcd.goldenrod', 'xkcd.grape', 'xkcd.grape_purple',
    'xkcd.grapefruit', 'xkcd.grass', 'xkcd.grass_green', 'xkcd.grassy_green', 'xkcd.green',
    'xkcd.green_apple', 'xkcd.green_blue', 'xkcd.green_brown', 'xkcd.green_grey',
    'xkcd.green_teal', 'xkcd.green_yellow', 'xkcd.greenblue', 'xkcd.greenish',
    'xkcd.greenish_beige', 'xkcd.greenish_blue', 'xkcd.greenish_brown', 'xkcd.greenish_cyan',
    'xkcd.greenish_grey', 'xkcd.greenish_tan', 'xkcd.greenish_teal', 'xkcd.greenish_turquoise',
    'xkcd.greenish_yellow', 'xkcd.greeny_blue', 'xkcd.greeny_brown', 'xkcd.greeny_grey',
    'xkcd.greeny_yellow', 'xkcd.grey', 'xkcd.grey_blue', 'xkcd.grey_brown', 'xkcd.grey_green',
    'xkcd.grey_pink', 'xkcd.grey_purple', 'xkcd.grey_teal', 'xkcd.greyblue', 'xkcd.greyish',
    'xkcd.greyish_blue', 'xkcd.greyish_brown', 'xkcd.greyish_green', 'xkcd.greyish_pink',
    'xkcd.greyish_purple', 'xkcd.greyish_teal', 'xkcd.gross_green', 'xkcd.gunmetal', 'xkcd.hazel',
    'xkcd.heather', 'xkcd.heliotrope', 'xkcd.highlighter_green', 'xkcd.hospital_green',
    'xkcd.hot_green', 'xkcd.hot_magenta', 'xkcd.hot_pink', 'xkcd.hot_purple', 'xkcd.hunter_green',
    'xkcd.ice', 'xkcd.ice_blue', 'xkcd.icky_green', 'xkcd.indian_red', 'xkcd.indigo',
    'xkcd.indigo_blue', 'xkcd.iris', 'xkcd.irish_green', 'xkcd.ivory', 'xkcd.jade',
    'xkcd.jade_green', 'xkcd.jungle_green', 'xkcd.kelley_green', 'xkcd.kelly_green',
    'xkcd.kermit_green', 'xkcd.key_lime', 'xkcd.khaki', 'xkcd.khaki_green', 'xkcd.kiwi',
    'xkcd.kiwi_green', 'xkcd.lavender', 'xkcd.lavender_blue', 'xkcd.lavender_pink',
    'xkcd.lawn_green', 'xkcd.leaf', 'xkcd.leaf_green', 'xkcd.leafy_green', 'xkcd.leather',
    'xkcd.lemon', 'xkcd.lemon_green', 'xkcd.lemon_lime', 'xkcd.lemon_yellow', 'xkcd.lichen',
    'xkcd.light_aqua', 'xkcd.light_aquamarine', 'xkcd.light_beige', 'xkcd.light_blue',
    'xkcd.light_blue_green', 'xkcd.light_blue_grey', 'xkcd.light_bluish_green',
    'xkcd.light_bright_green', 'xkcd.light_brown', 'xkcd.light_burgundy', 'xkcd.light_cyan',
    'xkcd.light_eggplant', 'xkcd.light_forest_green', 'xkcd.light_gold', 'xkcd.light_grass_green',
    'xkcd.light_green', 'xkcd.light_green_blue', 'xkcd.light_greenish_blue', 'xkcd.light_grey',
    'xkcd.light_grey_blue', 'xkcd.light_grey_green', 'xkcd.light_indigo', 'xkcd.light_khaki',
    'xkcd.light_lavendar', 'xkcd.light_lavender', 'xkcd.light_light_blue',
    'xkcd.light_light_green', 'xkcd.light_lilac', 'xkcd.light_lime', 'xkcd.light_lime_green',
    'xkcd.light_magenta', 'xkcd.light_maroon', 'xkcd.light_mauve', 'xkcd.light_mint',
    'xkcd.light_mint_green', 'xkcd.light_moss_green', 'xkcd.light_mustard', 'xkcd.light_navy',
    'xkcd.light_navy_blue', 'xkcd.light_neon_green', 'xkcd.light_olive',
    'xkcd.light_olive_green', 'xkcd.light_orange', 'xkcd.light_pastel_green',
    'xkcd.light_pea_green', 'xkcd.light_peach', 'xkcd.light_periwinkle', 'xkcd.light_pink',
    'xkcd.light_plum', 'xkcd.light_purple', 'xkcd.light_red', 'xkcd.light_rose',
    'xkcd.light_royal_blue', 'xkcd.light_sage', 'xkcd.light_salmon', 'xkcd.light_sea_green',
    'xkcd.light_seafoam', 'xkcd.light_seafoam_green', 'xkcd.light_sky_blue', 'xkcd.light_tan',
    'xkcd.light_teal', 'xkcd.light_turquoise', 'xkcd.light_urple', 'xkcd.light_violet',
    'xkcd.light_yellow', 'xkcd.light_yellow_green', 'xkcd.light_yellowish_green',
    'xkcd.lightblue', 'xkcd.lighter_green', 'xkcd.lighter_purple', 'xkcd.lightgreen',
    'xkcd.lightish_blue', 'xkcd.lightish_green', 'xkcd.lightish_purple', 'xkcd.lightish_red',
    'xkcd.lilac', 'xkcd.liliac', 'xkcd.lime', 'xkcd.lime_green', 'xkcd.lime_yellow',
    'xkcd.lipstick', 'xkcd.lipstick_red', 'xkcd.macaroni_and_cheese', 'xkcd.magenta',
    'xkcd.mahogany', 'xkcd.maize', 'xkcd.mango', 'xkcd.manilla', 'xkcd.marigold', 'xkcd.marine',
    'xkcd.marine_blue', 'xkcd.maroon', 'xkcd.mauve', 'xkcd.medium_blue', 'xkcd.medium_brown',
    'xkcd.medium_green', 'xkcd.medium_grey', 'xkcd.medium_pink', 'xkcd.medium_purple',
    'xkcd.melon', 'xkcd.merlot', 'xkcd.metallic_blue', 'xkcd.mid_blue', 'xkcd.mid_green',
    'xkcd.midnight', 'xkcd.midnight_blue', 'xkcd.midnight_purple', 'xkcd.military_green',
    'xkcd.milk_chocolate', 'xkcd.mint', 'xkcd.mint_green', 'xkcd.minty_green', 'xkcd.mocha',
    'xkcd.moss', 'xkcd.moss_green', 'xkcd.mossy_green', 'xkcd.mud', 'xkcd.mud_brown',
    'xkcd.mud_green', 'xkcd.muddy_brown', 'xkcd.muddy_green', 'xkcd.muddy_yellow',
    'xkcd.mulberry', 'xkcd.murky_green', 'xkcd.mushroom', 'xkcd.mustard', 'xkcd.mustard_brown',
    'xkcd.mustard_green', 'xkcd.mustard_yellow', 'xkcd.muted_blue', 'xkcd.muted_green',
    'xkcd.muted_pink', 'xkcd.muted_purple', 'xkcd.nasty_green', 'xkcd.navy', 'xkcd.navy_blue',
    'xkcd.navy_green', 'xkcd.neon_blue', 'xkcd.neon_green', 'xkcd.neon_pink', 'xkcd.neon_purple',
    'xkcd.neon_red', 'xkcd.neon_yellow', 'xkcd.nice_blue', 'xkcd.night_blue', 'xkcd.ocean',
    'xkcd.ocean_blue', 'xkcd.ocean_green', 'xkcd.ocher', 'xkcd.ochre', 'xkcd.ocre',
    'xkcd.off_blue', 'xkcd.off_green', 'xkcd.off_white', 'xkcd.off_yellow', 'xkcd.old_pink',
    'xkcd.old_rose', 'xkcd.olive', 'xkcd.olive_brown', 'xkcd.olive_drab', 'xkcd.olive_green',
    'xkcd.olive_yellow', 'xkcd.orange', 'xkcd.orange_brown', 'xkcd.orange_pink',
    'xkcd.orange_red', 'xkcd.orange_yellow', 'xkcd.orangeish', 'xkcd.orangered',
    'xkcd.orangey_brown', 'xkcd.orangey_red', 'xkcd.orangey_yellow', 'xkcd.orangish',
    'xkcd.orangish_brown', 'xkcd.orangish_red', 'xkcd.orchid', 'xkcd.pale', 'xkcd.pale_aqua',
    'xkcd.pale_blue', 'xkcd.pale_brown', 'xkcd.pale_cyan', 'xkcd.pale_gold', 'xkcd.pale_green',
    'xkcd.pale_grey', 'xkcd.pale_lavender', 'xkcd.pale_light_green', 'xkcd.pale_lilac',
    'xkcd.pale_lime', 'xkcd.pale_lime_green', 'xkcd.pale_magenta', 'xkcd.pale_mauve',
    'xkcd.pale_olive', 'xkcd.pale_olive_green', 'xkcd.pale_orange', 'xkcd.pale_peach',
    'xkcd.pale_pink', 'xkcd.pale_purple', 'xkcd.pale_red', 'xkcd.pale_rose', 'xkcd.pale_salmon',
    'xkcd.pale_sky_blue', 'xkcd.pale_teal', 'xkcd.pale_turquoise', 'xkcd.pale_violet',
    'xkcd.pale_yellow', 'xkcd.parchment', 'xkcd.pastel_blue', 'xkcd.pastel_green',
    'xkcd.pastel_orange', 'xkcd.pastel_pink', 'xkcd.pastel_purple', 'xkcd.pastel_red',
    'xkcd.pastel_yellow', 'xkcd.pea', 'xkcd.pea_green', 'xkcd.pea_soup', 'xkcd.pea_soup_green',
    'xkcd.peach', 'xkcd.peachy_pink', 'xkcd.peacock_blue', 'xkcd.pear', 'xkcd.periwinkle',
    'xkcd.periwinkle_blue', 'xkcd.perrywinkle', 'xkcd.petrol', 'xkcd.pig_pink', 'xkcd.pine',
    'xkcd.pine_green', 'xkcd.pink', 'xkcd.pink_purple', 'xkcd.pink_red', 'xkcd.pinkish',
    'xkcd.pinkish_brown', 'xkcd.pinkish_grey', 'xkcd.pinkish_orange', 'xkcd.pinkish_purple',
    'xkcd.pinkish_red', 'xkcd.pinkish_tan', 'xkcd.pinky', 'xkcd.pinky_purple', 'xkcd.pinky_red',
    'xkcd.piss_yellow', 'xkcd.pistachio', 'xkcd.plum', 'xkcd.plum_purple', 'xkcd.poison_green',
    'xkcd.poo', 'xkcd.poo_brown', 'xkcd.poop', 'xkcd.poop_brown', 'xkcd.poop_green',
    'xkcd.powder_blue', 'xkcd.powder_pink', 'xkcd.primary_blue', 'xkcd.prussian_blue',
    'xkcd.puce', 'xkcd.puke', 'xkcd.puke_brown', 'xkcd.puke_green', 'xkcd.puke_yellow',
    'xkcd.pumpkin', 'xkcd.pumpkin_orange', 'xkcd.pure_blue', 'xkcd.purple', 'xkcd.purple_blue',
    'xkcd.purple_brown', 'xkcd.purple_grey', 'xkcd.purple_pink', 'xkcd.purple_red',
    'xkcd.purpleish', 'xkcd.purpleish_blue', 'xkcd.purpleish_pink', 'xkcd.purpley',
    'xkcd.purpley_blue', 'xkcd.purpley_grey', 'xkcd.purpley_pink', 'xkcd.purplish',
    'xkcd.purplish_blue', 'xkcd.purplish_brown', 'xkcd.purplish_grey', 'xkcd.purplish_pink',
    'xkcd.purplish_red', 'xkcd.purply', 'xkcd.purply_blue', 'xkcd.purply_pink', 'xkcd.putty',
    'xkcd.racing_green', 'xkcd.radioactive_green', 'xkcd.raspberry', 'xkcd.raw_sienna',
    'xkcd.raw_umber', 'xkcd.really_light_blue', 'xkcd.red', 'xkcd.red_brown', 'xkcd.red_orange',
    'xkcd.red_pink', 'xkcd.red_purple', 'xkcd.red_violet', 'xkcd.red_wine', 'xkcd.reddish',
    'xkcd.reddish_brown', 'xkcd.reddish_grey', 'xkcd.reddish_orange', 'xkcd.reddish_pink',
    'xkcd.reddish_purple', 'xkcd.reddy_brown', 'xkcd.rich_blue', 'xkcd.rich_purple',
    'xkcd.robin_egg_blue', 'xkcd.robins_egg', 'xkcd.robins_egg_blue', 'xkcd.rosa', 'xkcd.rose',
    'xkcd.rose_pink', 'xkcd.rose_red', 'xkcd.rosy_pink', 'xkcd.rouge', 'xkcd.royal',
    'xkcd.royal_blue', 'xkcd.royal_purple', 'xkcd.ruby', 'xkcd.russet', 'xkcd.rust',
    'xkcd.rust_brown', 'xkcd.rust_orange', 'xkcd.rust_red', 'xkcd.rusty_orange',
    'xkcd.rusty_red', 'xkcd.saffron', 'xkcd.sage', 'xkcd.sage_green', 'xkcd.salmon',
    'xkcd.salmon_pink', 'xkcd.sand', 'xkcd.sand_brown', 'xkcd.sand_yellow', 'xkcd.sandstone',
    'xkcd.sandy', 'xkcd.sandy_brown', 'xkcd.sandy_yellow', 'xkcd.sap_green', 'xkcd.sapphire',
    'xkcd.scarlet', 'xkcd.sea', 'xkcd.sea_blue', 'xkcd.sea_green', 'xkcd.seafoam',
    'xkcd.seafoam_blue', 'xkcd.seafoam_green', 'xkcd.seaweed', 'xkcd.seaweed_green',
    'xkcd.sepia', 'xkcd.shamrock', 'xkcd.shamrock_green', 'xkcd.shit', 'xkcd.shit_brown',
    'xkcd.shit_green', 'xkcd.shocking_pink', 'xkcd.sick_green', 'xkcd.sickly_green',
    'xkcd.sickly_yellow', 'xkcd.sienna', 'xkcd.silver', 'xkcd.sky', 'xkcd.sky_blue',
    'xkcd.slate', 'xkcd.slate_blue', 'xkcd.slate_green', 'xkcd.slate_grey', 'xkcd.slime_green',
    'xkcd.snot', 'xkcd.snot_green', 'xkcd.soft_blue', 'xkcd.soft_green', 'xkcd.soft_pink',
    'xkcd.soft_purple', 'xkcd.spearmint', 'xkcd.spring_green', 'xkcd.spruce', 'xkcd.squash',
    'xkcd.steel', 'xkcd.steel_blue', 'xkcd.steel_grey', 'xkcd.stone', 'xkcd.stormy_blue',
    'xkcd.straw', 'xkcd.strawberry', 'xkcd.strong_blue', 'xkcd.strong_pink', 'xkcd.sun_yellow',
    'xkcd.sunflower', 'xkcd.sunflower_yellow', 'xkcd.sunny_yellow', 'xkcd.sunshine_yellow',
    'xkcd.swamp', 'xkcd.swamp_green', 'xkcd.tan', 'xkcd.tan_brown', 'xkcd.tan_green',
    'xkcd.tangerine', 'xkcd.taupe', 'xkcd.tea', 'xkcd.tea_green', 'xkcd.teal', 'xkcd.teal_blue',
    'xkcd.teal_green', 'xkcd.tealish', 'xkcd.tealish_green', 'xkcd.terra_cotta',
    'xkcd.terracota', 'xkcd.terracotta', 'xkcd.tiffany_blue', 'xkcd.tomato',
    'xkcd.tomato_red', 'xkcd.topaz', 'xkcd.toupe', 'xkcd.toxic_green', 'xkcd.tree_green',
    'xkcd.true_blue', 'xkcd.true_green', 'xkcd.turquoise', 'xkcd.turquoise_blue',
    'xkcd.turquoise_green', 'xkcd.turtle_green', 'xkcd.twilight', 'xkcd.twilight_blue',
    'xkcd.ugly_blue', 'xkcd.ugly_brown', 'xkcd.ugly_green', 'xkcd.ugly_pink', 'xkcd.ugly_purple',
    'xkcd.ugly_yellow', 'xkcd.ultramarine', 'xkcd.ultramarine_blue', 'xkcd.umber', 'xkcd.velvet',
    'xkcd.vermillion', 'xkcd.very_dark_blue', 'xkcd.very_dark_brown', 'xkcd.very_dark_green',
    'xkcd.very_dark_purple', 'xkcd.very_light_blue', 'xkcd.very_light_brown',
    'xkcd.very_light_green', 'xkcd.very_light_pink', 'xkcd.very_light_purple',
    'xkcd.very_pale_blue', 'xkcd.very_pale_green', 'xkcd.vibrant_blue', 'xkcd.vibrant_green',
    'xkcd.vibrant_purple', 'xkcd.violet', 'xkcd.violet_blue', 'xkcd.violet_pink',
    'xkcd.violet_red', 'xkcd.viridian', 'xkcd.vivid_blue', 'xkcd.vivid_green',
    'xkcd.vivid_purple', 'xkcd.vomit', 'xkcd.vomit_green', 'xkcd.vomit_yellow', 'xkcd.warm_blue',
    'xkcd.warm_brown', 'xkcd.warm_grey', 'xkcd.warm_pink', 'xkcd.warm_purple',
    'xkcd.washed_out_green', 'xkcd.water_blue', 'xkcd.watermelon', 'xkcd.weird_green',
    'xkcd.wheat', 'xkcd.white', 'xkcd.windows_blue', 'xkcd.wine', 'xkcd.wine_red',
    'xkcd.wintergreen', 'xkcd.wisteria', 'xkcd.yellow', 'xkcd.yellow_brown', 'xkcd.yellow_green',
    'xkcd.yellow_ochre', 'xkcd.yellow_orange', 'xkcd.yellow_tan', 'xkcd.yellowgreen',
    'xkcd.yellowish', 'xkcd.yellowish_brown', 'xkcd.yellowish_green', 'xkcd.yellowish_orange',
    'xkcd.yellowish_tan', 'xkcd.yellowy_brown', 'xkcd.yellowy_green', 'y', 'yellow',
    'yellowgreen'
]

INTERPOLATION_METHODS = [
    'allrounder_linear', 'allrounder_nearest', 'allrounder_cubic',
    'rbf_cubic', 'rbf_gaussian', 'rbf_inverse', 'rbf_linear',
    'rbf_multiquadric', 'rbf_quintic', 'rbf_thin_plate',
    'spline_linear', 'spline_cubic', 'spline_quintic'
]
