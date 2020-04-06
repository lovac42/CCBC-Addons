
#
# The files in this addon may have been modified for CCBC, and may not be the same as the original.
# The files in this addon may have been modified for CCBC, and may not be the same as the original.
# The files in this addon may have been modified for CCBC, and may not be the same as the original.
#


from PyQt4.QtGui import QDialog, QDialogButtonBox, QLabel, QVBoxLayout

from aqt import mw

from ._version import __version__

# CSR_GITHUB_URL = "https://github.com/scottgigante/korean-support"
CSR_GITHUB_URL = 'https://github.com/lovac42/CCBC-Addons'


def showAbout():
    dialog = QDialog(mw)

    label = QLabel()
    label.setStyleSheet("QLabel { font-size: 14px; }")

    contributors = [
        "Scott Gigante",
        "Alex Griffin",
        "Chris Hatch",
        "Roland Sieker",
        "Thomas TEMPÉ",
        "Luo Li-Yan",
        "Scott Gigante",
    ]

    text = """
<div style="font-weight: bold">Korean Support (for CCBC) v%s</div><br>
<div>This is a modified version for the CCBC project.<br>
Bugs and problems may not be related to the original code.<br>
No support is given, but feel free to ask.</div><br>
<div><span style="font-weight: bold">
    Maintainer</span>: lovac42</div>
<div><span style="font-weight: bold">Contributors</span>: %s</div>
<div><span style="font-weight: bold">Website</span>: <a href="%s">%s</a></div>
<div style="font-size: 12px">
    <br>Based on the Chinese Support add-on by Thomas TEMPÉ and many others.
    <br>If your name is missing from here, please open an issue on GitHub.
</div>
""" % (
        __version__,
        ", ".join(contributors),
        CSR_GITHUB_URL,
        CSR_GITHUB_URL,
    )

    label.setText(text)
    label.setOpenExternalLinks(True)

    buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
    buttonBox.accepted.connect(dialog.accept)

    layout = QVBoxLayout()
    layout.addWidget(label)
    layout.addWidget(buttonBox)

    dialog.setLayout(layout)
    dialog.setWindowTitle("About")
    dialog.exec_()
