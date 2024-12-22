# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'saver_mockupXEQrpG.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QStackedWidget, QTabWidget, QTableWidget,
    QTableWidgetItem, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(958, 800)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(20, -1, 20, 0)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.label.setFont(font)

        self.horizontalLayout.addWidget(self.label, 0, Qt.AlignLeft)

        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.label_user_name = QLabel(Form)
        self.label_user_name.setObjectName(u"label_user_name")

        self.verticalLayout_16.addWidget(self.label_user_name, 0, Qt.AlignRight)

        self.label_project_name = QLabel(Form)
        self.label_project_name.setObjectName(u"label_project_name")

        self.verticalLayout_16.addWidget(self.label_project_name, 0, Qt.AlignRight)


        self.horizontalLayout.addLayout(self.verticalLayout_16)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, -1, -1, 0)
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QSize(50, 50))
        self.pushButton.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_6.addWidget(self.pushButton)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_11)

        self.stackedWidget_path = QStackedWidget(Form)
        self.stackedWidget_path.setObjectName(u"stackedWidget_path")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.stackedWidget_path.sizePolicy().hasHeightForWidth())
        self.stackedWidget_path.setSizePolicy(sizePolicy1)
        self.stackedWidget_path.setMaximumSize(QSize(16777215, 50))
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.horizontalLayout_3 = QHBoxLayout(self.page_5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_12 = QLabel(self.page_5)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_3.addWidget(self.label_12)

        self.label_arrow_1 = QLabel(self.page_5)
        self.label_arrow_1.setObjectName(u"label_arrow_1")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_arrow_1.sizePolicy().hasHeightForWidth())
        self.label_arrow_1.setSizePolicy(sizePolicy2)
        self.label_arrow_1.setMaximumSize(QSize(20, 16777215))

        self.horizontalLayout_3.addWidget(self.label_arrow_1)

        self.label_81 = QLabel(self.page_5)
        self.label_81.setObjectName(u"label_81")

        self.horizontalLayout_3.addWidget(self.label_81)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)

        self.stackedWidget_path.addWidget(self.page_5)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.horizontalLayout_8 = QHBoxLayout(self.page_3)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_asset_type = QLabel(self.page_3)
        self.label_asset_type.setObjectName(u"label_asset_type")

        self.horizontalLayout_8.addWidget(self.label_asset_type)

        self.label_arrow_2 = QLabel(self.page_3)
        self.label_arrow_2.setObjectName(u"label_arrow_2")

        self.horizontalLayout_8.addWidget(self.label_arrow_2)

        self.label_asset = QLabel(self.page_3)
        self.label_asset.setObjectName(u"label_asset")

        self.horizontalLayout_8.addWidget(self.label_asset)

        self.label_arrow_3 = QLabel(self.page_3)
        self.label_arrow_3.setObjectName(u"label_arrow_3")

        self.horizontalLayout_8.addWidget(self.label_arrow_3)

        self.label_asset_task = QLabel(self.page_3)
        self.label_asset_task.setObjectName(u"label_asset_task")

        self.horizontalLayout_8.addWidget(self.label_asset_task)

        self.horizontalSpacer_5 = QSpacerItem(630, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_5)

        self.stackedWidget_path.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.horizontalLayout_9 = QHBoxLayout(self.page_4)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_seq = QLabel(self.page_4)
        self.label_seq.setObjectName(u"label_seq")

        self.horizontalLayout_9.addWidget(self.label_seq)

        self.label_arrow_4 = QLabel(self.page_4)
        self.label_arrow_4.setObjectName(u"label_arrow_4")

        self.horizontalLayout_9.addWidget(self.label_arrow_4)

        self.label_shot = QLabel(self.page_4)
        self.label_shot.setObjectName(u"label_shot")

        self.horizontalLayout_9.addWidget(self.label_shot)

        self.label_arrow_5 = QLabel(self.page_4)
        self.label_arrow_5.setObjectName(u"label_arrow_5")

        self.horizontalLayout_9.addWidget(self.label_arrow_5)

        self.label_shot_task = QLabel(self.page_4)
        self.label_shot_task.setObjectName(u"label_shot_task")

        self.horizontalLayout_9.addWidget(self.label_shot_task)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer)

        self.stackedWidget_path.addWidget(self.page_4)

        self.horizontalLayout_6.addWidget(self.stackedWidget_path)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(-1, -1, -1, 0)
        self.tabWidget_pathtree = QTabWidget(Form)
        self.tabWidget_pathtree.setObjectName(u"tabWidget_pathtree")
        self.tabWidget_pathtree.setMinimumSize(QSize(300, 0))
        self.tabWidget_pathtree.setMaximumSize(QSize(300, 16777215))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_6 = QVBoxLayout(self.tab)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(-1, -1, -1, 0)
        self.comboBox_filter = QComboBox(self.tab)
        self.comboBox_filter.setObjectName(u"comboBox_filter")

        self.horizontalLayout_14.addWidget(self.comboBox_filter)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_7)


        self.verticalLayout_6.addLayout(self.horizontalLayout_14)

        self.lineEdit = QLineEdit(self.tab)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout_6.addWidget(self.lineEdit)

        self.treeWidget_my_tasks = QTreeWidget(self.tab)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget_my_tasks.setHeaderItem(__qtreewidgetitem)
        self.treeWidget_my_tasks.setObjectName(u"treeWidget_my_tasks")
        self.treeWidget_my_tasks.setMinimumSize(QSize(0, 300))
        self.treeWidget_my_tasks.setMaximumSize(QSize(16777215, 480))
        self.treeWidget_my_tasks.header().setVisible(False)

        self.verticalLayout_6.addWidget(self.treeWidget_my_tasks)

        self.tabWidget_pathtree.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_7 = QVBoxLayout(self.tab_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.lineEdit_3 = QLineEdit(self.tab_2)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.verticalLayout_7.addWidget(self.lineEdit_3)

        self.treeWidget_assets = QTreeWidget(self.tab_2)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.treeWidget_assets.setHeaderItem(__qtreewidgetitem1)
        self.treeWidget_assets.setObjectName(u"treeWidget_assets")
        self.treeWidget_assets.header().setVisible(False)

        self.verticalLayout_7.addWidget(self.treeWidget_assets)

        self.frame = QFrame(self.tab_2)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.checkBox_mod = QCheckBox(self.frame)
        self.checkBox_mod.setObjectName(u"checkBox_mod")

        self.verticalLayout_4.addWidget(self.checkBox_mod)

        self.checkBox_texture = QCheckBox(self.frame)
        self.checkBox_texture.setObjectName(u"checkBox_texture")

        self.verticalLayout_4.addWidget(self.checkBox_texture)

        self.checkBox_rig = QCheckBox(self.frame)
        self.checkBox_rig.setObjectName(u"checkBox_rig")

        self.verticalLayout_4.addWidget(self.checkBox_rig)

        self.checkBox_character = QCheckBox(self.frame)
        self.checkBox_character.setObjectName(u"checkBox_character")

        self.verticalLayout_4.addWidget(self.checkBox_character)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(-1, -1, -1, 0)
        self.pushButton_assets_all = QPushButton(self.frame)
        self.pushButton_assets_all.setObjectName(u"pushButton_assets_all")

        self.horizontalLayout_15.addWidget(self.pushButton_assets_all)

        self.pushButton_assets_none = QPushButton(self.frame)
        self.pushButton_assets_none.setObjectName(u"pushButton_assets_none")

        self.horizontalLayout_15.addWidget(self.pushButton_assets_none)


        self.verticalLayout_4.addLayout(self.horizontalLayout_15)


        self.verticalLayout_7.addWidget(self.frame)

        self.tabWidget_pathtree.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_8 = QVBoxLayout(self.tab_3)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.lineEdit_4 = QLineEdit(self.tab_3)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.verticalLayout_8.addWidget(self.lineEdit_4)

        self.treeWidget_shots = QTreeWidget(self.tab_3)
        __qtreewidgetitem2 = QTreeWidgetItem()
        __qtreewidgetitem2.setText(0, u"1");
        self.treeWidget_shots.setHeaderItem(__qtreewidgetitem2)
        self.treeWidget_shots.setObjectName(u"treeWidget_shots")
        self.treeWidget_shots.header().setVisible(False)

        self.verticalLayout_8.addWidget(self.treeWidget_shots)

        self.frame_2 = QFrame(self.tab_3)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.checkBox_ani = QCheckBox(self.frame_2)
        self.checkBox_ani.setObjectName(u"checkBox_ani")

        self.verticalLayout_3.addWidget(self.checkBox_ani)

        self.checkBox_light = QCheckBox(self.frame_2)
        self.checkBox_light.setObjectName(u"checkBox_light")

        self.verticalLayout_3.addWidget(self.checkBox_light)

        self.checkBox_lookdev = QCheckBox(self.frame_2)
        self.checkBox_lookdev.setObjectName(u"checkBox_lookdev")

        self.verticalLayout_3.addWidget(self.checkBox_lookdev)

        self.checkBox_comp = QCheckBox(self.frame_2)
        self.checkBox_comp.setObjectName(u"checkBox_comp")

        self.verticalLayout_3.addWidget(self.checkBox_comp)

        self.checkBox = QCheckBox(self.frame_2)
        self.checkBox.setObjectName(u"checkBox")

        self.verticalLayout_3.addWidget(self.checkBox)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(-1, -1, -1, 0)
        self.pushButton_shots_all = QPushButton(self.frame_2)
        self.pushButton_shots_all.setObjectName(u"pushButton_shots_all")

        self.horizontalLayout_16.addWidget(self.pushButton_shots_all)

        self.pushButton_shots_none = QPushButton(self.frame_2)
        self.pushButton_shots_none.setObjectName(u"pushButton_shots_none")

        self.horizontalLayout_16.addWidget(self.pushButton_shots_none)


        self.verticalLayout_3.addLayout(self.horizontalLayout_16)


        self.verticalLayout_8.addWidget(self.frame_2)

        self.tabWidget_pathtree.addTab(self.tab_3, "")

        self.horizontalLayout_12.addWidget(self.tabWidget_pathtree)

        self.tabWidget_2 = QTabWidget(Form)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_2 = QVBoxLayout(self.tab_4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_2)

        self.lineEdit_2 = QLineEdit(self.tab_4)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_7.addWidget(self.lineEdit_2)

        self.pushButton_2 = QPushButton(self.tab_4)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy3)
        self.pushButton_2.setMinimumSize(QSize(50, 50))
        self.pushButton_2.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_7.addWidget(self.pushButton_2)

        self.pushButton_4 = QPushButton(self.tab_4)
        self.pushButton_4.setObjectName(u"pushButton_4")
        sizePolicy3.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy3)
        self.pushButton_4.setMinimumSize(QSize(50, 50))
        self.pushButton_4.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_7.addWidget(self.pushButton_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.stackedWidget = QStackedWidget(self.tab_4)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_10 = QVBoxLayout(self.page)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.treeWidget_grid_total = QTreeWidget(self.page)
        __qtreewidgetitem3 = QTreeWidgetItem()
        __qtreewidgetitem3.setText(0, u"1");
        self.treeWidget_grid_total.setHeaderItem(__qtreewidgetitem3)
        self.treeWidget_grid_total.setObjectName(u"treeWidget_grid_total")
        self.treeWidget_grid_total.setMinimumSize(QSize(0, 350))
        self.treeWidget_grid_total.setMaximumSize(QSize(16777215, 350))
        self.treeWidget_grid_total.header().setVisible(False)

        self.verticalLayout_10.addWidget(self.treeWidget_grid_total)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout_2.addWidget(self.stackedWidget)

        self.tabWidget_2.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.verticalLayout_5 = QVBoxLayout(self.tab_5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_8)

        self.lineEdit_5 = QLineEdit(self.tab_5)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_17.addWidget(self.lineEdit_5)

        self.pushButton_grid = QPushButton(self.tab_5)
        self.pushButton_grid.setObjectName(u"pushButton_grid")
        sizePolicy3.setHeightForWidth(self.pushButton_grid.sizePolicy().hasHeightForWidth())
        self.pushButton_grid.setSizePolicy(sizePolicy3)
        self.pushButton_grid.setMinimumSize(QSize(50, 50))
        self.pushButton_grid.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_17.addWidget(self.pushButton_grid)

        self.pushButton_3 = QPushButton(self.tab_5)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy3.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy3)
        self.pushButton_3.setMinimumSize(QSize(50, 50))
        self.pushButton_3.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_17.addWidget(self.pushButton_3)


        self.verticalLayout_5.addLayout(self.horizontalLayout_17)

        self.stackedWidget_3 = QStackedWidget(self.tab_5)
        self.stackedWidget_3.setObjectName(u"stackedWidget_3")
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.verticalLayout_11 = QVBoxLayout(self.page_6)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.tableWidget_list_wip = QTableWidget(self.page_6)
        self.tableWidget_list_wip.setObjectName(u"tableWidget_list_wip")
        self.tableWidget_list_wip.setMinimumSize(QSize(0, 350))
        self.tableWidget_list_wip.setMaximumSize(QSize(16777215, 350))
        self.tableWidget_list_wip.horizontalHeader().setVisible(False)
        self.tableWidget_list_wip.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_list_wip.verticalHeader().setVisible(False)

        self.verticalLayout_11.addWidget(self.tableWidget_list_wip)

        self.stackedWidget_3.addWidget(self.page_6)
        self.page_7 = QWidget()
        self.page_7.setObjectName(u"page_7")
        self.stackedWidget_3.addWidget(self.page_7)

        self.verticalLayout_5.addWidget(self.stackedWidget_3)

        self.tabWidget_2.addTab(self.tab_5, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.verticalLayout_9 = QVBoxLayout(self.tab_6)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_9)

        self.lineEdit_6 = QLineEdit(self.tab_6)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_18.addWidget(self.lineEdit_6)

        self.pushButton_5 = QPushButton(self.tab_6)
        self.pushButton_5.setObjectName(u"pushButton_5")
        sizePolicy3.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy3)
        self.pushButton_5.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_18.addWidget(self.pushButton_5)

        self.pushButton_6 = QPushButton(self.tab_6)
        self.pushButton_6.setObjectName(u"pushButton_6")
        sizePolicy3.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy3)
        self.pushButton_6.setMaximumSize(QSize(50, 50))

        self.horizontalLayout_18.addWidget(self.pushButton_6)


        self.verticalLayout_9.addLayout(self.horizontalLayout_18)

        self.stackedWidget_4 = QStackedWidget(self.tab_6)
        self.stackedWidget_4.setObjectName(u"stackedWidget_4")
        self.page_8 = QWidget()
        self.page_8.setObjectName(u"page_8")
        self.verticalLayout_12 = QVBoxLayout(self.page_8)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.tableWidget_list_pub = QTableWidget(self.page_8)
        self.tableWidget_list_pub.setObjectName(u"tableWidget_list_pub")
        self.tableWidget_list_pub.setMinimumSize(QSize(0, 350))
        self.tableWidget_list_pub.setMaximumSize(QSize(16777215, 350))
        self.tableWidget_list_pub.horizontalHeader().setVisible(False)
        self.tableWidget_list_pub.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_list_pub.verticalHeader().setVisible(False)
        self.tableWidget_list_pub.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_12.addWidget(self.tableWidget_list_pub)

        self.stackedWidget_4.addWidget(self.page_8)
        self.page_9 = QWidget()
        self.page_9.setObjectName(u"page_9")
        self.stackedWidget_4.addWidget(self.page_9)

        self.verticalLayout_9.addWidget(self.stackedWidget_4)

        self.tabWidget_2.addTab(self.tab_6, "")

        self.horizontalLayout_12.addWidget(self.tabWidget_2)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(-1, -1, -1, 0)
        self.label_82 = QLabel(Form)
        self.label_82.setObjectName(u"label_82")
        sizePolicy2.setHeightForWidth(self.label_82.sizePolicy().hasHeightForWidth())
        self.label_82.setSizePolicy(sizePolicy2)
        self.label_82.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_6.addWidget(self.label_82, 1, 0, 1, 1)

        self.label_88 = QLabel(Form)
        self.label_88.setObjectName(u"label_88")

        self.gridLayout_6.addWidget(self.label_88, 4, 1, 1, 1)

        self.label_90 = QLabel(Form)
        self.label_90.setObjectName(u"label_90")

        self.gridLayout_6.addWidget(self.label_90, 5, 1, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.spinBox_version = QSpinBox(Form)
        self.spinBox_version.setObjectName(u"spinBox_version")

        self.horizontalLayout_4.addWidget(self.spinBox_version)

        self.checkBox_avaliable_ver = QCheckBox(Form)
        self.checkBox_avaliable_ver.setObjectName(u"checkBox_avaliable_ver")

        self.horizontalLayout_4.addWidget(self.checkBox_avaliable_ver)

        self.horizontalSpacer_3 = QSpacerItem(500, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.gridLayout_6.addLayout(self.horizontalLayout_4, 1, 1, 1, 1)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        sizePolicy2.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy2)
        self.widget.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_6.addWidget(self.widget, 3, 0, 1, 1)

        self.label_89 = QLabel(Form)
        self.label_89.setObjectName(u"label_89")
        sizePolicy2.setHeightForWidth(self.label_89.sizePolicy().hasHeightForWidth())
        self.label_89.setSizePolicy(sizePolicy2)
        self.label_89.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_6.addWidget(self.label_89, 5, 0, 1, 1)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        sizePolicy2.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy2)
        self.label_3.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_6.addWidget(self.label_3, 0, 0, 1, 1)

        self.label_new_file_name = QLabel(Form)
        self.label_new_file_name.setObjectName(u"label_new_file_name")

        self.gridLayout_6.addWidget(self.label_new_file_name, 0, 1, 1, 1)

        self.label_87 = QLabel(Form)
        self.label_87.setObjectName(u"label_87")
        sizePolicy2.setHeightForWidth(self.label_87.sizePolicy().hasHeightForWidth())
        self.label_87.setSizePolicy(sizePolicy2)
        self.label_87.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_6.addWidget(self.label_87, 4, 0, 1, 1)

        self.label_85 = QLabel(Form)
        self.label_85.setObjectName(u"label_85")
        sizePolicy2.setHeightForWidth(self.label_85.sizePolicy().hasHeightForWidth())
        self.label_85.setSizePolicy(sizePolicy2)
        self.label_85.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_6.addWidget(self.label_85, 2, 0, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.comboBox_filetype = QComboBox(Form)
        self.comboBox_filetype.setObjectName(u"comboBox_filetype")

        self.horizontalLayout_11.addWidget(self.comboBox_filetype)

        self.horizontalSpacer_4 = QSpacerItem(600, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_4)


        self.gridLayout_6.addLayout(self.horizontalLayout_11, 2, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_6)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(-1, -1, -1, 0)
        self.label_24 = QLabel(Form)
        self.label_24.setObjectName(u"label_24")

        self.horizontalLayout_19.addWidget(self.label_24)

        self.label_23 = QLabel(Form)
        self.label_23.setObjectName(u"label_23")

        self.horizontalLayout_19.addWidget(self.label_23)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_10)

        self.pushButton_cancel = QPushButton(Form)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout_19.addWidget(self.pushButton_cancel)

        self.pushButton_7 = QPushButton(Form)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.horizontalLayout_19.addWidget(self.pushButton_7)


        self.verticalLayout.addLayout(self.horizontalLayout_19)


        self.retranslateUi(Form)

        self.stackedWidget_path.setCurrentIndex(1)
        self.tabWidget_pathtree.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(1)
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_3.setCurrentIndex(0)
        self.stackedWidget_4.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"File Save", None))
        self.label_user_name.setText(QCoreApplication.translate("Form", u"User Name", None))
        self.label_project_name.setText(QCoreApplication.translate("Form", u"Project Name", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"home", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"My Tasks", None))
        self.label_arrow_1.setText(QCoreApplication.translate("Form", u"\u25b6", None))
        self.label_81.setText(QCoreApplication.translate("Form", u"Task test", None))
        self.label_asset_type.setText(QCoreApplication.translate("Form", u"Asset Type", None))
        self.label_arrow_2.setText(QCoreApplication.translate("Form", u"\u25b6", None))
        self.label_asset.setText(QCoreApplication.translate("Form", u"Asset", None))
        self.label_arrow_3.setText(QCoreApplication.translate("Form", u"\u25b6", None))
        self.label_asset_task.setText(QCoreApplication.translate("Form", u"Task", None))
        self.label_seq.setText(QCoreApplication.translate("Form", u"Sequence", None))
        self.label_arrow_4.setText(QCoreApplication.translate("Form", u"\u25b6", None))
        self.label_shot.setText(QCoreApplication.translate("Form", u"Shot", None))
        self.label_arrow_5.setText(QCoreApplication.translate("Form", u"\u25b6", None))
        self.label_shot_task.setText(QCoreApplication.translate("Form", u"Task", None))
        self.tabWidget_pathtree.setTabText(self.tabWidget_pathtree.indexOf(self.tab), QCoreApplication.translate("Form", u"My Tasks", None))
        self.checkBox_mod.setText(QCoreApplication.translate("Form", u"Modeling", None))
        self.checkBox_texture.setText(QCoreApplication.translate("Form", u"Texture", None))
        self.checkBox_rig.setText(QCoreApplication.translate("Form", u"Rig", None))
        self.checkBox_character.setText(QCoreApplication.translate("Form", u"Character", None))
        self.pushButton_assets_all.setText(QCoreApplication.translate("Form", u"Select All", None))
        self.pushButton_assets_none.setText(QCoreApplication.translate("Form", u"Select None", None))
        self.tabWidget_pathtree.setTabText(self.tabWidget_pathtree.indexOf(self.tab_2), QCoreApplication.translate("Form", u"Assets", None))
        self.checkBox_ani.setText(QCoreApplication.translate("Form", u"Animation", None))
        self.checkBox_light.setText(QCoreApplication.translate("Form", u"Lighting", None))
        self.checkBox_lookdev.setText(QCoreApplication.translate("Form", u"Lookdev", None))
        self.checkBox_comp.setText(QCoreApplication.translate("Form", u"Compositing", None))
        self.checkBox.setText(QCoreApplication.translate("Form", u"Matchmove", None))
        self.pushButton_shots_all.setText(QCoreApplication.translate("Form", u"Select All", None))
        self.pushButton_shots_none.setText(QCoreApplication.translate("Form", u"Select None", None))
        self.tabWidget_pathtree.setTabText(self.tabWidget_pathtree.indexOf(self.tab_3), QCoreApplication.translate("Form", u"Shots", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"\uadf8\ub9ac\ub4dc", None))
        self.pushButton_4.setText(QCoreApplication.translate("Form", u"\ub9ac\uc2a4\ud2b8", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), QCoreApplication.translate("Form", u"All", None))
        self.pushButton_grid.setText(QCoreApplication.translate("Form", u"\uadf8\ub9ac\ub4dc", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"\ub9ac\uc2a4\ud2b8", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), QCoreApplication.translate("Form", u"Working", None))
        self.pushButton_5.setText(QCoreApplication.translate("Form", u"\uadf8\ub9ac\ub4dc", None))
        self.pushButton_6.setText(QCoreApplication.translate("Form", u"\ub9ac\uc2a4\ud2b8", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), QCoreApplication.translate("Form", u"Publishes", None))
        self.label_82.setText(QCoreApplication.translate("Form", u"Version", None))
        self.label_88.setText("")
        self.label_90.setText("")
        self.checkBox_avaliable_ver.setText(QCoreApplication.translate("Form", u"Use next Avaliable Version number", None))
        self.label_89.setText(QCoreApplication.translate("Form", u"Work Area", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Name", None))
        self.label_new_file_name.setText("")
        self.label_87.setText(QCoreApplication.translate("Form", u"Preview", None))
        self.label_85.setText(QCoreApplication.translate("Form", u"File Type", None))
        self.label_24.setText(QCoreApplication.translate("Form", u"\u25a0", None))
        self.label_23.setText(QCoreApplication.translate("Form", u"One Item discoverd by publisher.", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"Cancel", None))
        self.pushButton_7.setText(QCoreApplication.translate("Form", u"Save", None))
    # retranslateUi

