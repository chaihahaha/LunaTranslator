from qtsymbols import *
import functools, importlib
from traceback import print_exc
import gobject
from myutils.config import globalconfig, _TRL, static_data
from myutils.utils import nowisdark
from gui.usefulwidget import (
    D_getsimplecombobox,
    D_getspinbox,
    D_getcolorbutton,
    getIconButton,
    selectcolor,
    FocusFontCombo,
)


def changeHorizontal(self):

    globalconfig["transparent"] = self.horizontal_slider.value()
    try:
        self.horizontal_slider_label.setText("{}%".format(globalconfig["transparent"]))
    except:
        pass
    #
    gobject.baseobject.translation_ui.set_color_transparency()


def createhorizontal_slider(self):

    self.horizontal_slider = QSlider()
    self.horizontal_slider.setMaximum(100)
    self.horizontal_slider.setMinimum(1)
    self.horizontal_slider.setOrientation(Qt.Orientation.Horizontal)
    self.horizontal_slider.setValue(0)
    self.horizontal_slider.setValue(globalconfig["transparent"])
    self.horizontal_slider.valueChanged.connect(
        functools.partial(changeHorizontal, self)
    )
    return self.horizontal_slider


def createhorizontal_slider_label(self):
    self.horizontal_slider_label = QLabel()
    self.horizontal_slider_label.setText("{}%".format(globalconfig["transparent"]))
    return self.horizontal_slider_label


def changeHorizontal_tool(self):

    globalconfig["transparent_tool"] = self.horizontal_slider_tool.value()
    try:
        self.horizontal_slider_tool_label.setText(
            "{}%".format(globalconfig["transparent_tool"])
        )
    except:
        pass
    #
    gobject.baseobject.translation_ui.set_color_transparency()


def createhorizontal_slider_tool(self):

    self.horizontal_slider_tool = QSlider()
    self.horizontal_slider_tool.setMaximum(100)
    self.horizontal_slider_tool.setMinimum(1)
    self.horizontal_slider_tool.setOrientation(Qt.Orientation.Horizontal)
    self.horizontal_slider_tool.setValue(0)
    self.horizontal_slider_tool.setValue(globalconfig["transparent_tool"])
    self.horizontal_slider_tool.valueChanged.connect(
        functools.partial(changeHorizontal_tool, self)
    )
    return self.horizontal_slider_tool


def createhorizontal_slider_tool_label(self):

    self.horizontal_slider_tool_label = QLabel()
    self.horizontal_slider_tool_label.setText(
        "{}%".format(globalconfig["transparent_tool"])
    )
    return self.horizontal_slider_tool_label


def createfontcombo():

    sfont_comboBox = FocusFontCombo()

    def callback(x):
        globalconfig.__setitem__("settingfonttype", x)
        gobject.baseobject.setcommonstylesheet()

    sfont_comboBox.setCurrentFont(QFont(globalconfig["settingfonttype"]))
    sfont_comboBox.currentTextChanged.connect(callback)
    return sfont_comboBox


def maybesetstyle(_dark):
    if _dark == nowisdark():
        gobject.baseobject.setcommonstylesheet()


def wrapedsetstylecallback(_dark, self, func):
    try:
        func(self, functools.partial(maybesetstyle, _dark))
    except:
        print_exc()


def checkthemeissetable(self, dark: bool):
    try:
        darklight = ["light", "dark"][dark]
        idx = globalconfig[darklight + "theme"] - int(not dark)
        if idx == -1:
            return None
        _fn = static_data["themes"][darklight][idx]["file"]

        if _fn.endswith(".py"):
            try:
                return functools.partial(
                    wrapedsetstylecallback,
                    dark,
                    self,
                    importlib.import_module(
                        "files.themes." + _fn[:-3].replace("/", ".")
                    ).get_setting_window,
                )
            except:
                return None
        elif _fn.endswith(".qss"):
            return None
    except:
        print_exc()
        return None


def checkthemesettingvisandapply_1(self, _dark):
    try:
        if _dark:

            darksetting = checkthemeissetable(self, True)
            self.darksetting = darksetting
            if not self.darksetting:
                self.btnthemedark.hide()
            else:
                self.btnthemedark.show()
                self.btnthemedark.clicked.disconnect()
                self.btnthemedark.clicked.connect(self.darksetting)
        else:

            lightsetting = checkthemeissetable(self, False)
            self.lightsetting = lightsetting
            if not self.lightsetting:
                self.btnthemelight.hide()
            else:
                self.btnthemelight.show()
                self.btnthemelight.clicked.disconnect()
                self.btnthemelight.clicked.connect(self.lightsetting)

    except:
        print_exc()


def createbtnthemelight(self):
    lightsetting = checkthemeissetable(self, False)
    self.lightsetting = lightsetting
    self.btnthemelight = getIconButton(icon="fa.gear")
    try:
        if not self.lightsetting:
            self.btnthemelight.hide()
        else:
            self.btnthemelight.clicked.disconnect()
            self.btnthemelight.clicked.connect(self.lightsetting)
    except:
        pass
    return self.btnthemelight


def createbtnthemedark(self):
    darksetting = checkthemeissetable(self, True)
    self.darksetting = darksetting
    self.btnthemedark = getIconButton(
        icon="fa.gear",
    )
    try:
        if not self.darksetting:
            self.btnthemedark.hide()
        else:
            self.btnthemedark.clicked.disconnect()
            self.btnthemedark.clicked.connect(self.darksetting)
    except:
        pass
    return self.btnthemedark


def checkthemesettingvisandapply(self, _dark, _):
    checkthemesettingvisandapply_1(self, _dark)
    maybesetstyle(_dark)


def uisetting(self):

    def themelist(t):
        return [_["name"] for _ in static_data["themes"][t]]

    uigrid = [
        [
            (
                dict(
                    title="主界面",
                    type="grid",
                    grid=(
                        [
                            (
                                dict(
                                    title="翻译窗口",
                                    type="grid",
                                    grid=(
                                        [
                                            ("不透明度", 4),
                                            (
                                                functools.partial(
                                                    createhorizontal_slider, self
                                                ),
                                                8,
                                            ),
                                            (
                                                functools.partial(
                                                    createhorizontal_slider_label, self
                                                ),
                                                2,
                                            ),
                                        ],
                                        [
                                            ("背景颜色", 4),
                                            D_getcolorbutton(
                                                globalconfig,
                                                "backcolor",
                                                callback=lambda: selectcolor(
                                                    self,
                                                    globalconfig,
                                                    "backcolor",
                                                    self.back_color_button,
                                                    callback=gobject.baseobject.translation_ui.set_color_transparency,
                                                ),
                                                name="back_color_button",
                                                parent=self,
                                            ),
                                            "",
                                            "",
                                            ("圆角_半径", 4),
                                            (
                                                D_getspinbox(
                                                    0,
                                                    100,
                                                    globalconfig,
                                                    "yuanjiao_r",
                                                    callback=lambda _: gobject.baseobject.translation_ui.set_color_transparency(),
                                                ),
                                                2,
                                            ),
                                        ],
                                    ),
                                ),
                                0,
                                "group",
                            )
                        ],
                        [
                            (
                                dict(
                                    title="工具栏",
                                    type="grid",
                                    grid=(
                                        [
                                            ("不透明度", 4),
                                            (
                                                functools.partial(
                                                    createhorizontal_slider_tool, self
                                                ),
                                                8,
                                            ),
                                            (
                                                functools.partial(
                                                    createhorizontal_slider_tool_label,
                                                    self,
                                                ),
                                                2,
                                            ),
                                        ],
                                        [
                                            ("背景颜色", 4),
                                            D_getcolorbutton(
                                                globalconfig,
                                                "backcolor_tool",
                                                callback=lambda: selectcolor(
                                                    self,
                                                    globalconfig,
                                                    "backcolor_tool",
                                                    self.back_color_button_tool,
                                                    callback=gobject.baseobject.translation_ui.set_color_transparency,
                                                ),
                                                name="back_color_button_tool",
                                                parent=self,
                                            ),
                                        ],
                                        [
                                            ("工具按钮颜色", 4),
                                            D_getcolorbutton(
                                                globalconfig,
                                                "buttoncolor",
                                                callback=lambda: selectcolor(
                                                    self,
                                                    globalconfig,
                                                    "buttoncolor",
                                                    self.buttoncolorbutton,
                                                    callback=lambda: gobject.baseobject.translation_ui.refreshtooliconsignal.emit(),
                                                ),
                                                name="buttoncolorbutton",
                                                parent=self,
                                            ),
                                            D_getcolorbutton(
                                                globalconfig,
                                                "buttoncolor_1",
                                                callback=lambda: selectcolor(
                                                    self,
                                                    globalconfig,
                                                    "buttoncolor_1",
                                                    self.buttoncolorbutton_1,
                                                    callback=lambda: gobject.baseobject.translation_ui.refreshtooliconsignal.emit(),
                                                ),
                                                name="buttoncolorbutton_1",
                                                parent=self,
                                            ),
                                            "",
                                            ("工具按钮大小", 4),
                                            (
                                                D_getspinbox(
                                                    5,
                                                    100,
                                                    globalconfig,
                                                    "buttonsize",
                                                    callback=lambda _: gobject.baseobject.translation_ui.refreshtooliconsignal.emit(),
                                                ),
                                                2,
                                            ),
                                        ],
                                    ),
                                ),
                                0,
                                "group",
                            )
                        ],
                    ),
                ),
                0,
                "group",
            )
        ],
        [
            (
                dict(
                    title="设置界面",
                    grid=(
                        ["字体", createfontcombo],
                        [
                            "字体大小",
                            D_getspinbox(
                                1,
                                100,
                                globalconfig,
                                "settingfontsize",
                                callback=lambda _: gobject.baseobject.setcommonstylesheet(),
                            ),
                        ],
                        [
                            "按钮颜色",
                            (
                                D_getcolorbutton(
                                    globalconfig,
                                    "buttoncolor2",
                                    callback=lambda: selectcolor(
                                        self,
                                        globalconfig,
                                        "buttoncolor2",
                                        self.buttoncolorbutton2,
                                    ),
                                    name="buttoncolorbutton2",
                                    parent=self,
                                ),
                                D_getcolorbutton(
                                    globalconfig,
                                    "buttoncolor3",
                                    callback=lambda: selectcolor(
                                        self,
                                        globalconfig,
                                        "buttoncolor3",
                                        self.buttoncolorbutton3,
                                    ),
                                    name="buttoncolorbutton3",
                                    parent=self,
                                ),
                            ),
                        ],
                        [
                            "按钮大小",
                            D_getspinbox(5, 100, globalconfig, "buttonsize2"),
                        ],
                    ),
                ),
                0,
                "group",
            )
        ],
        [
            (
                dict(
                    title="主题",
                    grid=(
                        [
                            "明暗",
                            D_getsimplecombobox(
                                _TRL(["跟随系统", "明亮", "黑暗"]),
                                globalconfig,
                                "darklight2",
                                lambda _: gobject.baseobject.setcommonstylesheet(),
                            ),
                        ],
                        [
                            "明亮主题",
                            (
                                D_getsimplecombobox(
                                    _TRL(["默认"]) + themelist("light"),
                                    globalconfig,
                                    "lighttheme",
                                    functools.partial(
                                        checkthemesettingvisandapply, self, False
                                    ),
                                ),
                                functools.partial(createbtnthemelight, self),
                            ),
                        ],
                        [
                            "黑暗主题",
                            (
                                D_getsimplecombobox(
                                    themelist("dark"),
                                    globalconfig,
                                    "darktheme",
                                    functools.partial(
                                        checkthemesettingvisandapply, self, True
                                    ),
                                ),
                                functools.partial(createbtnthemedark, self),
                            ),
                        ],
                    ),
                ),
                0,
                "group",
            )
        ],
        [
            (
                dict(
                    title="窗口特效",
                    grid=(
                        [
                            "翻译窗口",
                            D_getsimplecombobox(
                                ["Disable", "Acrylic", "Aero"],
                                globalconfig,
                                "WindowEffect",
                                callback=lambda _: [
                                    gobject.baseobject.translation_ui.set_color_transparency(),
                                    gobject.baseobject.translation_ui.seteffect(),
                                ],
                            ),
                        ],
                        [
                            "其他",
                            D_getsimplecombobox(
                                ["Solid", "Acrylic", "Mica", "MicaAlt"],
                                globalconfig,
                                "WindowBackdrop",
                                callback=lambda _: gobject.baseobject.setcommonstylesheet(),
                            ),
                        ],
                    ),
                ),
                0,
                "group",
            )
        ],
    ]
    return uigrid
