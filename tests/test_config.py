import filecmp
import json
import os

import unified_plotting as up


def test_config(capsys, my_outdir):
    # Export defaults
    filepath1 = os.path.join(my_outdir, 'config_defaults.json')
    filepath2 = os.path.join(my_outdir, 'config_defaults_reformatted.json')
    filepath3 = os.path.join(my_outdir, 'config_manually_changed.json')
    up.config.save_defaults_to_json(filepath1)
    up.config.save_to_json(filepath2)
    assert not filecmp.cmp(filepath1, filepath2)
    with open(filepath1) as file_handle1, open(filepath2) as file_handle2:
        data1 = json.load(file_handle1)
        data2 = json.load(file_handle2)
    assert data1 == data2
    data1['title'] = 42
    assert data1 != data2

    # Change settings and see it in representations
    up.config.settings.title = 'nice!'
    up.config.settings.x_labels_color = 'greenish'

    assert 'nice!' in str(up.config.settings)
    assert 'greenish' in str(up.config.settings)
    up.config.report()

    shell_log = capsys.readouterr()
    stdout_text = shell_log.out
    assert 'nice!' in stdout_text
    assert 'greenish' in stdout_text

    # Export new settings
    up.config.save_to_json(filepath3)
    with open(filepath3) as f:
        external_text = f.read()
    assert 'nice!' in external_text
    assert 'greenish' in external_text

    # Load defaults again
    up.config.load_defaults()
    assert 'nice!' not in str(up.config.settings)
    assert 'greenish' not in str(up.config.settings)

    # Load new settings from previously exported file
    up.config.load_from_json(filepath3)
    assert 'nice!' in str(up.config.settings)
    assert 'greenish' in str(up.config.settings)

    # Reset to defaults again (otherwise it might have influence on other tests)
    up.config.load_defaults()
